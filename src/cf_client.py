"""Minimal Cloudflare API client for security lab scripts."""

from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE = "https://api.cloudflare.com/client/v4"


class CloudflareClient:
    def __init__(self, api_token: str | None = None, account_id: str | None = None) -> None:
        self.api_token = api_token or os.environ.get("CLOUDFLARE_API_TOKEN", "")
        self.account_id = account_id or os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")

        if not self.api_token:
            raise ValueError(
                "CLOUDFLARE_API_TOKEN not set. Copy .env.example to .env and add your token."
            )

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
            }
        )

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        response = self.session.request(method, f"{API_BASE}{path}", timeout=30, **kwargs)
        response.raise_for_status()
        payload = response.json()
        if not payload.get("success", False):
            errors = payload.get("errors", [])
            raise RuntimeError(f"Cloudflare API error: {errors}")
        return payload

    def try_request(self, method: str, path: str, **kwargs: Any) -> tuple[dict[str, Any] | None, str | None]:
        """Return (payload, error_message). Does not raise on HTTP/API errors."""
        try:
            return self._request(method, path, **kwargs), None
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else "unknown"
            return None, f"HTTP {status} on {path}"
        except RuntimeError as exc:
            return None, str(exc)

    def list_zones(self, name: str | None = None) -> list[dict[str, Any]]:
        params: dict[str, str] = {}
        if name:
            params["name"] = name
        payload = self._request("GET", "/zones", params=params)
        return payload.get("result", [])

    def get_zone_by_name(self, zone_name: str) -> dict[str, Any] | None:
        zones = self.list_zones(name=zone_name)
        for zone in zones:
            if zone.get("name") == zone_name:
                return zone
        return None

    def list_dns_records(self, zone_id: str) -> list[dict[str, Any]]:
        payload = self._request("GET", f"/zones/{zone_id}/dns_records")
        return payload.get("result", [])

    def list_rulesets(self, zone_id: str) -> list[dict[str, Any]]:
        payload = self._request("GET", f"/zones/{zone_id}/rulesets")
        return payload.get("result", [])

    def get_ruleset(self, zone_id: str, ruleset_id: str) -> dict[str, Any]:
        payload = self._request("GET", f"/zones/{zone_id}/rulesets/{ruleset_id}")
        return payload.get("result", {})

    def get_zone_settings(self, zone_id: str) -> list[dict[str, Any]]:
        payload = self._request("GET", f"/zones/{zone_id}/settings")
        return payload.get("result", [])

    def get_ssl_setting(self, zone_id: str) -> dict[str, Any]:
        payload = self._request("GET", f"/zones/{zone_id}/settings/ssl")
        return payload.get("result", {})

    def verify_token(self) -> dict[str, Any]:
        payload = self._request("GET", "/user/tokens/verify")
        return payload.get("result", {})
