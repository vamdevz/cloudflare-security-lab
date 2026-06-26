#!/usr/bin/env python3
"""Basic security posture check for a Cloudflare zone."""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.cf_client import CloudflareClient

FIREWALL_PHASES = {
    "http_request_firewall_custom",
    "http_request_firewall_managed",
    "http_ratelimit",
}


def audit_zone(client: CloudflareClient, zone_name: str) -> dict:
    zone = client.get_zone_by_name(zone_name)
    if not zone:
        raise ValueError(f"Zone not found: {zone_name}")

    zone_id = zone["id"]
    findings: list[dict] = []
    warnings: list[str] = []

    ssl_mode = None
    settings: dict = {}

    payload, err = client.try_request("GET", f"/zones/{zone_id}/settings/ssl")
    if payload:
        ssl_mode = payload.get("result", {}).get("value")
    else:
        warnings.append(f"SSL setting unavailable: {err}")

    payload, err = client.try_request("GET", f"/zones/{zone_id}/settings")
    if payload:
        settings = {s["id"]: s.get("value") for s in payload.get("result", [])}
        if ssl_mode is None:
            ssl_mode = settings.get("ssl")
    else:
        warnings.append(f"Zone settings unavailable: {err}")

    if ssl_mode and ssl_mode not in ("strict", "full"):
        findings.append(
            {
                "severity": "HIGH",
                "check": "ssl_mode",
                "detail": f"SSL mode is '{ssl_mode}' — prefer 'strict' or 'full' for production.",
            }
        )

    if settings:
        if settings.get("security_level") == "essentially_off":
            findings.append(
                {
                    "severity": "HIGH",
                    "check": "security_level",
                    "detail": "Security level is essentially_off.",
                }
            )
        if settings.get("always_use_https") is not True and settings.get("always_use_https") != "on":
            findings.append(
                {
                    "severity": "MEDIUM",
                    "check": "always_use_https",
                    "detail": "Always Use HTTPS is not enabled.",
                }
            )

    rulesets, err = client.try_request("GET", f"/zones/{zone_id}/rulesets")
    ruleset_list = rulesets.get("result", []) if rulesets else []
    if err:
        warnings.append(f"Rulesets unavailable: {err}")

    waf_rulesets = [r for r in ruleset_list if r.get("phase") in FIREWALL_PHASES]
    custom_rulesets = [r for r in waf_rulesets if r.get("phase") == "http_request_firewall_custom"]
    managed_rulesets = [r for r in waf_rulesets if r.get("phase") == "http_request_firewall_managed"]
    rate_limit_rulesets = [r for r in waf_rulesets if r.get("phase") == "http_ratelimit"]

    custom_rules = []
    managed_rules = []
    rate_limit_rules = []

    for rs in waf_rulesets:
        detail_payload, detail_err = client.try_request(
            "GET", f"/zones/{zone_id}/rulesets/{rs['id']}"
        )
        if not detail_payload:
            warnings.append(f"Ruleset detail skipped ({rs.get('name')}): {detail_err}")
            continue

        detail = detail_payload.get("result", {})
        phase = detail.get("phase")
        rules = detail.get("rules", []) or []
        for rule in rules:
            entry = {
                "ruleset": detail.get("name"),
                "phase": phase,
                "description": rule.get("description"),
                "action": rule.get("action"),
                "enabled": rule.get("enabled", True),
            }
            if phase == "http_request_firewall_custom":
                custom_rules.append(entry)
            elif phase == "http_request_firewall_managed":
                managed_rules.append(entry)
            elif phase == "http_ratelimit":
                rate_limit_rules.append(entry)

    if managed_rulesets and not managed_rules:
        findings.append(
            {
                "severity": "INFO",
                "check": "managed_waf",
                "detail": (
                    f"Managed WAF ruleset present ({managed_rulesets[0].get('name')}) "
                    "but rule details not readable with current token."
                ),
            }
        )
    elif not managed_rulesets:
        findings.append(
            {
                "severity": "MEDIUM",
                "check": "managed_waf",
                "detail": "No managed WAF rulesets detected.",
            }
        )

    if rate_limit_rulesets and not rate_limit_rules:
        findings.append(
            {
                "severity": "INFO",
                "check": "rate_limiting",
                "detail": (
                    f"Rate limit ruleset exists (version {rate_limit_rulesets[0].get('version')}) "
                    "but rule details not readable with current token."
                ),
            }
        )
    elif not rate_limit_rulesets:
        findings.append(
            {
                "severity": "LOW",
                "check": "rate_limiting",
                "detail": "No rate limit ruleset found — consider limits on auth/API paths.",
            }
        )

    dns_summary = {"total": None, "proxied": None, "dns_only": None}
    dns_payload, dns_err = client.try_request("GET", f"/zones/{zone_id}/dns_records")
    if dns_payload:
        dns_records = dns_payload.get("result", [])
        proxied_count = sum(1 for r in dns_records if r.get("proxied"))
        dns_summary = {
            "total": len(dns_records),
            "proxied": proxied_count,
            "dns_only": len(dns_records) - proxied_count,
        }
    else:
        warnings.append(f"DNS records unavailable: {dns_err}")

    if warnings:
        warnings.append(
            "Tip: Account tokens (cfat_) sometimes lack zone read scope. "
            "Create a User API token (cfut_) with Zone Read, DNS Read, "
            "Zone Settings Read, and WAF Read for full audit."
        )

    return {
        "zone": zone_name,
        "zone_id": zone_id,
        "plan": zone.get("plan", {}).get("name"),
        "ssl_mode": ssl_mode,
        "security_level": settings.get("security_level"),
        "always_use_https": settings.get("always_use_https"),
        "dns": dns_summary,
        "waf": {
            "custom_ruleset_count": len(custom_rulesets),
            "managed_ruleset_count": len(managed_rulesets),
            "rate_limit_ruleset_count": len(rate_limit_rulesets),
            "custom_rules": custom_rules[:10],
            "rulesets_summary": [
                {
                    "name": r.get("name"),
                    "phase": r.get("phase"),
                    "kind": r.get("kind"),
                    "version": r.get("version"),
                    "last_updated": r.get("last_updated"),
                }
                for r in waf_rulesets
            ],
        },
        "findings": findings,
        "finding_count": len(findings),
        "warnings": warnings,
    }


def main() -> None:
    zone_name = os.environ.get("CLOUDFLARE_ZONE_NAME")
    if not zone_name:
        print("Set CLOUDFLARE_ZONE_NAME in .env (e.g. your-test-domain.example.com)")
        sys.exit(1)

    client = CloudflareClient()
    report = audit_zone(client, zone_name)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
