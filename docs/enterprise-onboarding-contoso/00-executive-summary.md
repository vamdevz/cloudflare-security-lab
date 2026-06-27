# Executive Summary — Contoso Cloudflare Onboarding

## Objective

Onboard Contoso’s public web estate (primary: `contoso.com`, `www.contoso.com`, `api.contoso.com`) to Cloudflare Enterprise for **DDoS protection**, **WAF**, **global CDN**, and **centralized edge security policy** — with **no unplanned outage** during DNS migration and **no big-bang security rollout**.

## Current state (typical)

| Layer | Today |
|-------|--------|
| DNS | Registrar or Azure DNS / Route53 — A/AAAA/CNAME to origin or load balancer |
| TLS | Origin or LB terminates HTTPS; mixed redirect behavior |
| WAF | None at edge, or legacy appliance |
| DDoS | ISP / cloud basic only |
| Observability | Origin logs; limited edge visibility |

## Target state

| Layer | With Cloudflare |
|-------|-----------------|
| DNS | Authoritative on Cloudflare (full setup) or hybrid CNAME setup for apex |
| TLS | Edge termination; **Full (strict)** to origin; optional origin CA |
| WAF | Managed rules (phased) + custom rules (after observation) |
| DDoS | Always-on L3/L7; Enterprise SLA |
| Observability | Security Events, Logpush → SIEM (Sentinel/Splunk) |

## Scope (in)

- Production marketing site and public API gateway hostnames
- SSL/TLS mode, redirect rules, caching policy for static assets
- WAF managed + custom rules (phased)
- Rate limiting on auth/API paths (phase 6)
- Logpush configuration and runbooks

## Scope (out — phase 1)

- Cloudflare Zero Trust (Access) for internal apps — separate workstream
- Workers rewrite of application logic
- Full bot management tuning until traffic baseline exists
- HSTS preload and HTTP/3 until 30+ days stable on Full (strict)

## Success criteria

| Metric | Target |
|--------|--------|
| Cutover downtime | 0 minutes (TTL-bound propagation only) |
| Post-cutover P1 incidents | 0 caused by Cloudflare config |
| WAF false positive rate (after tuning) | < 0.1% of legitimate requests blocked |
| Time to first block mode (managed WAF) | ≥ 14 days after cutover in log/simulate |
| SSL grade (external scan) | A or A+ before HSTS enable |
| Rollback tested | Yes, documented NS revert path |

## Recommended timeline (indicative)

| Phase | Duration | Calendar |
|-------|----------|----------|
| Discovery & design | 2–3 weeks | Weeks 1–3 |
| Pilot subdomain | 1 week | Week 4 |
| Production cutover | 1 change window | Week 5 |
| Baseline + observation | 2–4 weeks | Weeks 5–8 |
| WAF enforce + custom rules | 2–3 weeks | Weeks 9–11 |
| Advanced TLS / HTTP/3 | 1 week | Week 12+ |

## Investment themes (secure by design)

1. **Separate traffic path changes from policy enforcement** — DNS first, security second.
2. **Observe before block** — Enterprise `log` action and managed rules simulation.
3. **Infrastructure as code** — Terraform + PR review for all rule changes after baseline.
4. **Least privilege** — scoped API tokens per environment; no account-wide tokens in CI.
5. **Evidence for auditors** — Logpush, change tickets, rule version history.

## Engineering note

When presenting to Contoso stakeholders, lead with **risk reduction and change control**, not feature lists. The question they care about is: *“Will our checkout/API break when we change nameservers?”* Answer: *Pilot → lower TTL → cutover → validate → then WAF in log mode.*

---

Next: [01 — Discovery & readiness](01-discovery-readiness.md)
