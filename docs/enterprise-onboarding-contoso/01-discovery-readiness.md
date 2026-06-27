# Phase 0 — Discovery & Readiness

## Goals

- Build a complete inventory of names, origins, certificates, and dependencies
- Identify cutover risks before any Cloudflare configuration
- Establish rollback contacts and maintenance windows

## Discovery workshops (3 sessions)

| Session | Attendees | Output |
|---------|-----------|--------|
| **DNS & infra** | Network, DNS admin, cloud platform | DNS export, NS TTLs, apex constraints |
| **Applications** | App owners, QA, API team | URL list, auth flows, upload sizes, WebSocket use |
| **Security & compliance** | CISO delegate, SOC | Data residency, logging requirements, PCI scope |

## Inventory template

### Domains and hostnames

| Hostname | Purpose | Origin (IP/FQDN) | Port | Protocol | Criticality |
|----------|---------|------------------|------|----------|-------------|
| `contoso.com` | Marketing apex | `20.x.x.x` (Azure App GW) | 443 | HTTPS | P1 |
| `www.contoso.com` | Marketing | same | 443 | HTTPS | P1 |
| `api.contoso.com` | Public REST API | `api.internal.contoso.com` | 443 | HTTPS | P1 |
| `status.contoso.com` | Status page | SaaS CNAME | 443 | HTTPS | P2 |

### DNS dependencies to flag

- **MX / SPF / DKIM / DMARC** — must be cloned exactly to Cloudflare DNS
- **TXT verification** (Google, Microsoft, ACME) — export before import
- **CAA records** — ensure `letsencrypt.org` or DigiCert allowed if Cloudflare issues certs
- **Wildcard records** — confirm app behavior
- **Internal split-horizon DNS** — corporate users may resolve differently; document

### Origin connectivity

| Check | How | Pass criteria |
|-------|-----|---------------|
| Origin accepts Cloudflare IP ranges | Allow-list on firewall / NSG | [Cloudflare IP lists](https://www.cloudflare.com/ips/) permitted |
| Valid cert on origin | `curl -v https://origin` with SNI | Cert matches host; chain trusted |
| HTTP vs HTTPS on origin | Probe port 80 | Align with SSL mode (redirect or close 80) |
| Real client IP | App reads `CF-Connecting-IP` or `X-Forwarded-For` | App team confirms parsing |
| WebSockets / SSE | Test through CF orange-cloud | Required for live features |
| Large uploads | POST > 100 MB if applicable | Enterprise limits documented |

### Certificate inventory

| Hostname | Issuer | Expiry | Where stored | Action |
|----------|--------|--------|--------------|--------|
| `*.contoso.com` | DigiCert | 2026-12 | Key vault | Edge: Universal SSL; origin: keep or Origin CA |
| `api.contoso.com` | Same | 2026-12 | Key vault | Full (strict) requires valid origin cert |

### Application behaviors that affect WAF

Document for phase 5–6 tuning:

- JSON payloads with encoded content (base64 fields — see lab rule patterns)
- Mobile apps with custom User-Agent
- Partner IP allowlists (prefer Cloudflare IP lists + mTLS later, not hardcoded in app)
- Admin paths (`/admin`, `/wp-admin` if legacy)
- Webhooks inbound (signature validation paths must not be blocked)

## Risk register (starter)

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|------------|--------|------------|
| R1 | Apex NS change breaks email | Medium | High | Clone MX/SPF/DKIM; validate with `dig` |
| R2 | Origin rejects CF IPs | Medium | High | Pre-allow Cloudflare ranges on firewall |
| R3 | WAF blocks legitimate API | High | Medium | Log/simulate 14+ days before block |
| R4 | SSL mode mismatch (525/526) | Medium | High | Pilot subdomain; Full (strict) only when origin cert valid |
| R5 | Cached stale content after cutover | Low | Medium | Purge plan; low TTL during migration |
| R6 | Third-party CNAME chains | Medium | Medium | Document `_acme-challenge`, SaaS CNAMEs |

## Readiness gates (must pass before Phase 2 pilot)

- [ ] Full DNS zone export (BIND or provider API)
- [ ] Stakeholder sign-off on maintenance window
- [ ] Rollback owner assigned ([09-rollback](09-rollback-contingency.md))
- [ ] Cloudflare Enterprise account + SSO + RBAC roles created
- [ ] API token scopes defined ([08-governance](08-governance-operations.md))
- [ ] Origin allows Cloudflare IP ranges

## Tools

```powershell
# From this repo — inventory zones after adding Contoso token to .env
python scripts/list_zones.py
python scripts/zone_security_audit.py
```

Use [discovery checklist](checklists/discovery-checklist.md) for workshop sign-off.

---

Next: [02 — Architecture & design](02-architecture-design.md)
