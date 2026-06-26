#!/usr/bin/env python3
"""Deploy advanced WAF lab rules (fits Free plan 5-rule limit)."""

import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

ZONE_ID = os.environ.get("CLOUDFLARE_ZONE_ID", "")
RULESET_ID = os.environ.get("CLOUDFLARE_CUSTOM_RULESET_ID", "")

# 3 new rules covering 5 attack patterns (2 existing = 5 total on Free plan)
NEW_RULES = [
    {
        "action": "block",
        "description": "LAB block path traversal and SSRF probes on API",
        "enabled": True,
        "expression": (
            '(starts_with(http.request.uri.path, "/api/") and ('
            'http.request.uri.path contains "%2e%2e" or '
            'http.request.uri.path contains ".." or '
            'url_decode(http.request.uri.path, "r") contains ".." or '
            'url_decode(http.request.uri.query, "r") contains "../" or '
            'lower(url_decode(http.request.uri.query, "r")) contains "169.254.169.254" or '
            'lower(url_decode(http.request.uri.query, "r")) contains "metadata.google" or '
            'lower(url_decode(http.request.uri.query, "r")) contains "localhost" or '
            'lower(url_decode(http.request.uri.query, "r")) contains "127.0.0.1"))'
        ),
    },
    {
        "action": "block",
        "description": "LAB block method override and spoofed CDN IP headers",
        "enabled": True,
        "expression": (
            "((starts_with(http.request.uri.path, \"/api/\") and ("
            'len(http.request.headers["x-http-method-override"][0]) > 0 or '
            'len(http.request.headers["x-method-override"][0]) > 0 or '
            'len(http.request.headers["x-http-method"][0]) > 0)) or '
            '(len(http.request.headers["cf-connecting-ip"][0]) > 0 or '
            'len(http.request.headers["true-client-ip"][0]) > 0 or '
            'len(http.request.headers["x-azure-clientip"][0]) > 0))'
        ),
    },
    {
        "action": "block",
        "description": "LAB enforce host allowlist and block X-Forwarded-Host on API",
        "enabled": True,
        "expression": (
            '(starts_with(http.request.uri.path, "/api/") and ('
            'not lower(http.host) in {"mslearn.site" "www.mslearn.site"} or '
            'len(http.request.headers["x-forwarded-host"][0]) > 0))'
        ),
    },
]


def rule_to_payload(rule: dict) -> dict:
    entry = {
        "action": rule["action"],
        "description": rule["description"],
        "enabled": rule["enabled"],
        "expression": rule["expression"],
    }
    if rule.get("action_parameters"):
        entry["action_parameters"] = rule["action_parameters"]
    if rule.get("logging"):
        entry["logging"] = rule["logging"]
    if rule.get("id"):
        entry["id"] = rule["id"]
    return entry


def main() -> None:
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    if not token:
        raise SystemExit("CLOUDFLARE_API_TOKEN not set")
    if not ZONE_ID or not RULESET_ID:
        raise SystemExit(
            "Set CLOUDFLARE_ZONE_ID and CLOUDFLARE_CUSTOM_RULESET_ID in .env "
            "(see .env.example)"
        )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/rulesets/{RULESET_ID}"

    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()["result"]
    existing = data["rules"]

    existing_descs = {r.get("description") for r in existing}
    to_add = [r for r in NEW_RULES if r["description"] not in existing_descs]

    if not to_add:
        print("All advanced rules already deployed.")
        for r in existing:
            print(f"  - {r.get('description')} ({r.get('action')})")
        return

    merged = [rule_to_payload(r) for r in existing]
    merged.extend(rule_to_payload(r) for r in to_add)

    if len(merged) > 5:
        raise SystemExit(f"Would exceed Free plan limit: {len(merged)} rules (max 5)")

    put_body = {
        "name": data["name"],
        "kind": data["kind"],
        "phase": data["phase"],
        "rules": merged,
    }

    put_resp = requests.put(url, headers=headers, json=put_body, timeout=30)
    print(f"Status: {put_resp.status_code}")
    body = put_resp.json()
    if not body.get("success"):
        print(json.dumps(body, indent=2))
        sys.exit(1)

    print(f"Deployed {len(merged)} rules (Free plan max: 5):\n")
    for r in body["result"]["rules"]:
        print(f"  [{r['action']}] {r['description']}")


if __name__ == "__main__":
    main()
