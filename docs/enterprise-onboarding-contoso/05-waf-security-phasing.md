# WAF Security Phasing — Baseline to Advanced

## Philosophy

> **Observe → tune → enforce → extend**

Enterprise engagements fail when teams enable OWASP block mode on cutover day. Contoso rolls out security in **controlled waves** with measurable false-positive budgets.

## Phase map

| Phase | Timing | WAF state | Custom rules |
|-------|--------|-----------|--------------|
| Cutover | Day 0 | Managed: **Off** or Log | None |
| Baseline | Week 1 | Managed: **Log** | Skip good bots only |
| Observation | Weeks 2–5 | Managed: **Log** + weekly review | Document candidates |
| Enforce 1 | Week 6 | Managed: **Block** (OWASP) | None new |
| Enforce 2 | Weeks 7–8 | Block + exceptions tuned | Path traversal API |
| Enforce 3 | Weeks 9–10 | Block | Header spoof, host allowlist |
| Advanced | Week 11+ | Block | Rate limits, API-specific |

---

## Wave 0 — Cutover day (visibility only)

**Enable**

- DDoS protection (automatic)
- Security Events visibility
- Optional: **Log** on Cloudflare Managed Ruleset (Enterprise)

**Disable / defer**

- All custom **block** rules
- Bot Fight Mode on `api.contoso.com`
- IP geo block lists

**Engineering note:** On Free/lab plans, `log` action is unavailable — use **skip** with logging enabled or Security Events only. Enterprise Contoso uses **log** before **block**.

---

## Wave 1 — Managed rules in log mode (Week 1)

Dashboard: **Security → WAF → Managed rules**

| Ruleset | Action | Notes |
|---------|--------|-------|
| Cloudflare Managed Ruleset | Log | Default |
| OWASP Core | Log | High FP on legacy apps — review weekly |
| Exposed Credentials Check | Log | Low risk to enable |

**SOC actions**

- Export daily top 10 triggered rule IDs
- Map each to: true attack / false positive / needs app fix

---

## Wave 2 — Observation & exception design (Weeks 2–5)

### Weekly tuning meeting agenda (60 min)

1. Review Security Events filtered by `action eq log`
2. Top URIs, ASNs, countries — any legitimate traffic?
3. Propose **narrow** skip rules (specific path + method + header)
4. Reject broad exceptions ("skip all POST to /api")

### Exception pattern (good)

```text
(http.request.uri.path eq "/api/v1/legacy/upload" and http.request.method eq "POST"
 and ip.src in {10.0.0.0/8})
```

### Exception pattern (bad)

```text
(http.request.uri.path contains "/api/")
```

### Custom rule candidates (document only — do not block yet)

| Priority | Pattern | Lab reference |
|----------|---------|---------------|
| P1 | Path traversal on `/api/*` | ADVANCED-WAF-RULES #3 |
| P1 | SSRF probes in query | ADVANCED-WAF-RULES #3 |
| P2 | Method override headers | ADVANCED-WAF-RULES #4 |
| P2 | Spoofed CDN IP headers | ADVANCED-WAF-RULES #4 |
| P3 | Host / X-Forwarded-Host on API | ADVANCED-WAF-RULES #5 |
| P3 | Base64-encoded host in query | ADVANCED-WAF-RULES #2 |

---

## Wave 3 — Managed rules to block (Week 6)

**Pre-requisites**

- Signed memo: "Observation complete"
- Rollback: set ruleset back to Log in one click
- CAB ticket approved

**Steps**

1. Change Cloudflare Managed Ruleset: Log → **Block**
2. Monitor 24h — origin 5xx and support tickets
3. OWASP Core: Block with **paranoia level** agreed (start PL2, not PL4 on legacy PHP)
4. Add skip rules only from Wave 2 approved list

---

## Wave 4 — Custom rules (one per change window)

Deploy **one rule group per week** maximum.

### Rule group A — API path abuse

```text
(starts_with(http.request.uri.path, "/api/") and (
  http.request.uri.path contains "%2e%2e" or
  url_decode(http.request.uri.path, "r") contains ".."
))
```

**Action:** Block  
**Validate:** `curl -i "https://api.contoso.com/users/%252e%252e%252fadmin"` → 403  
**Validate legit:** normal API client → 200

### Rule group B — Header integrity

Block `X-HTTP-Method-Override`, spoofed `CF-Connecting-IP` from clients, etc.

### Rule group C — Host allowlist (API only)

Allow `api.contoso.com` only; block foreign `Host` on `/api/*`.

**Warning:** Test mobile apps and partner integrations that use alternate Host headers.

### Rule group D — Rate limiting

Separate **rate limiting rules** (not custom WAF) on:

- `/api/v1/auth/login` — 10 req/min per IP
- `/api/v1/password/reset` — 5 req/min per IP

---

## Free plan vs Enterprise (Contoso)

| Capability | Lab (`mslearn.site`) | Contoso Enterprise |
|------------|----------------------|---------------------|
| Custom WAF rules | 5 max | Higher limits |
| Log action | No | Yes |
| Managed rules simulate | Limited | Full |
| Logpush | Add-on | Standard engagement |
| Account teams / RBAC | No | Yes |

Lab proves **expression syntax**; Contoso adds **process and scale**.

---

## Terraform alignment

After Wave 3, manage rules in Git:

```hcl
# terraform/environments/prod/waf.tf — pattern from lab repo
resource "cloudflare_ruleset" "custom_waf" {
  zone_id = var.zone_id
  name    = "contoso-custom-waf"
  kind    = "zone"
  phase   = "http_request_firewall_custom"
  # rules deployed via PR + plan/apply
}
```

---

## Rollback per wave

| Wave | Rollback |
|------|----------|
| Managed log | Disable ruleset |
| Managed block | Set to Log |
| Custom rule | Disable single rule or delete via API |
| Rate limit | Disable rule |

Document rule IDs in change ticket.

---

Next: [06 — Traffic monitoring & tuning](06-traffic-monitoring-tuning.md)
