#!/usr/bin/env python3
"""Add LAB base64 host block rule to Cloudflare WAF custom ruleset."""

import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
load_dotenv()

ZONE_ID = os.environ.get("CLOUDFLARE_ZONE_ID", "")
RULESET_ID = os.environ.get("CLOUDFLARE_CUSTOM_RULESET_ID", "")

EXPRESSION = (
    '(starts_with(http.request.uri.path, "/api/connect") '
    'and len(http.request.uri.args["target"][0]) > 0 '
    "and not lower(decode_base64(url_decode(http.request.uri.args[\"target\"][0]))) "
    'in {"testhost.allowed.local" "lab.mslearn.site"})'
)


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
    base = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/rulesets/{RULESET_ID}"

    resp = requests.get(base, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()["result"]
    existing = data["rules"]

    new_rule = {
        "action": "block",
        "description": "LAB block unknown base64 host on /api/connect",
        "enabled": True,
        "expression": EXPRESSION,
    }

    new_rules = []
    inserted = False
    for rule in existing:
        if rule.get("description") == "LAB block unknown base64 host on /api/connect":
            print("Rule already exists — skipping create.")
            return

        entry = {
            "id": rule["id"],
            "action": rule["action"],
            "description": rule.get("description", ""),
            "enabled": rule.get("enabled", True),
            "expression": rule["expression"],
        }
        if rule.get("action_parameters"):
            entry["action_parameters"] = rule["action_parameters"]
        if rule.get("logging"):
            entry["logging"] = rule["logging"]
        new_rules.append(entry)

        if rule.get("description") == "good bot" and not inserted:
            new_rules.append(new_rule)
            inserted = True

    if not inserted:
        new_rules.insert(0, new_rule)

    put_body = {
        "name": data["name"],
        "kind": data["kind"],
        "phase": data["phase"],
        "rules": new_rules,
    }

    put_resp = requests.put(base, headers=headers, json=put_body, timeout=30)
    print(f"Status: {put_resp.status_code}")
    print(json.dumps(put_resp.json(), indent=2))


if __name__ == "__main__":
    main()
