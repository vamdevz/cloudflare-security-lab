# Migration & Cutover — Zero-Downtime DNS

## Strategy summary

**Do not** change nameservers and enable WAF block rules in the same maintenance window.

| Step | Action | User impact |
|------|--------|-------------|
| 1 | Lower TTL at current DNS (300s) | Faster propagation later |
| 2 | Import zone to Cloudflare (identical records) | None — NS unchanged |
| 3 | Validate records in CF dashboard | None |
| 4 | Pre-warm: test via hosts file / resolve override | None for production users |
| 5 | Change NS at registrar to Cloudflare | Propagation 5 min – 48h |
| 6 | Monitor; hypercare 5 days | Possible stale cache at old DNS |
| 7 | Enable WAF **log only** | None if rules in log |

---

## Pre-cutover: TTL lowering (T-72h to T-24h)

At **current** DNS provider (before NS change):

```
contoso.com.    NS    ...    TTL 86400  →  300
www             A     ...    TTL 3600   →  300
api             CNAME ...    TTL 3600   →  300
```

Wait one full previous TTL cycle so caches expire.

---

## Zone import to Cloudflare

### Option A — AXFR / provider import

Cloudflare Dashboard → DNS → Import and export → upload BIND file from discovery.

### Option B — Terraform / API

Use `cloudflare_record` resources for repeatability (recommended for Enterprise).

### Record validation checklist

Compare record-by-record:

```bash
dig NS contoso.com @old-ns
dig NS contoso.com @1.1.1.1   # after cutover

dig MX contoso.com
dig TXT contoso.com
dig A www.contoso.com
dig CNAME api.contoso.com
```

**Critical:** MX, SPF, DKIM, DMARC must match **exactly**. Proxy status:

| Record type | Proxied? |
|-------------|----------|
| A/AAAA/CNAME (web/API) | Yes (orange) |
| MX | No |
| TXT (email auth) | No |
| NS | N/A |

---

## SSL before traffic hits Cloudflare

1. Issue or confirm **Universal SSL** / Advanced Certificate covers `contoso.com`, `*.contoso.com`
2. Set SSL/TLS → **Full (strict)**
3. Install **Origin CA** or valid public cert on Azure App Gateway
4. Test from Cloudflare → origin:
   ```bash
   curl -I https://origin-ip -H "Host: www.contoso.com" --resolve www.contoso.com:443:ORIGIN_IP
   ```
5. Enable **Always Use HTTPS** and **Automatic HTTPS Rewrites**

Common errors:

| Error | Cause | Fix |
|-------|-------|-----|
| 525 | No SSL on origin | Enable HTTPS on origin |
| 526 | Invalid origin cert | Fix cert chain or hostname |
| 521 | Origin down / firewall | Allow Cloudflare IPs |
| 522 | Timeout | Origin slow or blocking |

---

## Nameserver cutover (change window)

### T-0 (change window open)

1. Confirm rollback NS values documented ([09-rollback](09-rollback-contingency.md))
2. At registrar, replace NS with Cloudflare-assigned nameservers:
   ```
   ada.ns.cloudflare.com
   bob.ns.cloudflare.com
   ```
   (Use values from Contoso zone dashboard)
3. Start war room bridge; monitor synthetic checks every 60s

### T+0 to T+4h

| Check | Tool |
|-------|------|
| Global DNS propagation | `dig @8.8.8.8`, Cloudflare DNS checker |
| HTTPS 200 on www | Synthetic monitor |
| API smoke test | Postman collection |
| Email send/receive | Test mailbox |
| Origin load | Azure metrics — expect CF IP sources |

### T+24h

- Confirm old NS no longer authoritative in major resolvers
- Raise TTL back to 3600+ for stable records (optional)

---

## Partial cutover alternative (low risk first)

If full NS change is politically difficult:

1. Move **only** `www.contoso.com` CNAME to Cloudflare (CNAME setup / SaaS mode)
2. Apex `contoso.com` → redirect to `www` at registrar
3. Migrate apex NS in phase 2

Enterprise **CNAME setup** documentation applies for apex on some registrars.

---

## Caching at cutover

| Asset type | Cache policy |
|------------|--------------|
| Static (JS/CSS/images) | Cache Everything + long TTL |
| HTML (marketing) | Standard or bypass if dynamic |
| API (`api.contoso.com`) | **Bypass cache** |
| Auth cookies | Respect origin `Cache-Control` |

Purge all cache once after cutover if content mismatch reported:

```bash
# API or dashboard — zone purge
curl -X POST "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/purge_cache" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}'
```

---

## What NOT to enable on cutover day

- HSTS (breaks rollback testing)
- HTTP/3 (debug separately)
- WAF block on managed rules
- Aggressive custom block rules
- Bot Fight Mode on API hostnames
- Minimum TLS 1.3-only

---

## Hypercare (days 1–5 post-cutover)

| Day | Focus |
|-----|-------|
| D+1 | DNS completeness, SSL errors, 5xx spike |
| D+2 | App owner regression suite |
| D+3 | Email deliverability spot check |
| D+4 | Performance baseline vs pre-cutover |
| D+5 | Handoff to observation phase; close change ticket |

---

Next: [05 — WAF security phasing](05-waf-security-phasing.md)
