#!/usr/bin/env python3
"""List Cloudflare zones accessible to your API token."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.cf_client import CloudflareClient


def main() -> None:
    client = CloudflareClient()

    print("Verifying API token...")
    try:
        verify = client.verify_token()
        print(f"Token status: {verify.get('status', 'unknown')}")
    except Exception:
        print("Token verify skipped (account tokens may not support /user/tokens/verify)")

    zones = client.list_zones()
    if not zones:
        print("No zones found for this token.")
        return

    summary = [
        {
            "name": z.get("name"),
            "id": z.get("id"),
            "status": z.get("status"),
            "plan": z.get("plan", {}).get("name"),
        }
        for z in zones
    ]
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
