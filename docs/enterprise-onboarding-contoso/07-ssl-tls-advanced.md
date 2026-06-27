# SSL/TLS & Advanced Edge Settings

## Sequencing principle

**Advanced TLS features come last.** HSTS and HTTP/3 are hard to roll back without client-side pain.

| Setting | Earliest enable | Prerequisite |
|---------|-----------------|--------------|
| Full (strict) | Cutover day | Valid origin cert |
| Always Use HTTPS | Cutover day | Full mode working |
| TLS 1.2 minimum | Cutover day | Legacy clients assessed |
| TLS 1.3 | Week 2+ | No TLS 1.0/1.1 clients in logs |
| HSTS (short max-age) | Day 30+ post-cutover | SSL Labs A |
| HSTS preload | Day 90+ | Legal/comms approval |
| HTTP/3 (QUIC) | Day 30+ | UDP 443 allowed to origin path |
| Authenticated Origin Pulls | Phase 7 | Origin nginx/Azure config ready |

---

## Phase A — Cutover TLS baseline

### Dashboard: SSL/TLS

| Setting | Value |
|---------|-------|
| Encryption mode | **Full (strict)** |
| Always Use HTTPS | On |
| Minimum TLS Version | 1.2 |
| Opportunistic Encryption | On |
| TLS 1.3 | On (default) |
| Automatic HTTPS Rewrites | On |

### Origin certificate options

| Option | Pros | Cons |
|--------|------|------|
| Public CA cert on origin | Standard | Renewal management |
| Cloudflare Origin CA | Long-lived, free | Trust only via CF edge |
| mTLS (Authenticated Origin Pulls) | Strongest | Config complexity |

**Contoso recommendation:** Public cert or Origin CA on App Gateway; plan mTLS in phase 7.

### Validation commands

```bash
# External SSL test
curl -I https://www.contoso.com/

# Check redirect from HTTP
curl -I http://www.contoso.com/

# Origin cert from Cloudflare perspective (525/526 debug)
# Use dashboard Edge Certificates → Test origin
```

---

## Phase B — HSTS (staged rollout)

### Why wait 30 days?

- Rollback to non-CF origin requires HTTP access during migration
- HSTS cached in browsers survives DNS rollback
- Mis-issued certs become harder to recover from

### Staged max-age

| Stage | max-age | includeSubDomains | preload |
|-------|---------|-------------------|---------|
| 1 (pilot internal) | 300 (5 min) | Off | Off |
| 2 (production) | 86400 (1 day) | Off | Off |
| 3 (stable) | 31536000 (1 year) | On | Off |
| 4 (optional) | 31536000 | On | **On** (hstspreload.org) |

Enable via **SSL/TLS → Edge Certificates → HSTS**.

### Pre-HSTS checklist

- [ ] All subdomains serve valid HTTPS (no mixed content)
- [ ] `http://` redirects to `https://` everywhere
- [ ] No intentional HTTP-only legacy apps on subdomains
- [ ] SSL Labs grade **A** on www and api
- [ ] Rollback runbook updated (HSTS warning section)

---

## Phase C — HTTP/3 (QUIC)

### Benefits

- Faster handshake on lossy networks
- Multiplexing improvements

### Risks

- Some corporate firewalls block UDP 443
- Debug tooling less mature than TCP

### Rollout

1. Enable **Network → HTTP/3 (with QUIC)** in dashboard
2. Monitor 7 days: support tickets, synthetic failures from corporate networks
3. Keep HTTP/2 fallback (automatic)

```bash
# Test HTTP/3 support (requires curl with HTTP/3)
curl -I --http3 https://www.contoso.com/
```

If corporate users report failures: disable HTTP/3; document known limitation.

---

## Phase D — Authenticated Origin Pulls (optional)

Edge presents client certificate to origin; origin validates against Cloudflare CA.

**Use when:** Origin is public IP but must only accept Cloudflare.

Azure App Gateway / nginx configuration required — separate runbook per platform.

---

## Phase E — Advanced performance (post-security)

| Feature | When | Notes |
|---------|------|-------|
| Brotli | After cache policy stable | Auto for text |
| Early Hints | Marketing site | Test LCP |
| Argo Smart Routing | Enterprise | Cost vs latency |
| Tiered Cache | Multi-region | Enterprise |

Do not enable Argo + HTTP/3 + aggressive cache in one change.

---

## SSL/TLS decision log (template)

| Date | Change | Approver | Rollback tested |
|------|--------|----------|-----------------|
| 2026-08-15 | HSTS max-age 86400 | CISO delegate | N/A (5 min stage used first) |
| 2026-09-01 | HTTP/3 enabled | Platform lead | Yes — disable in dashboard |

---

Next: [08 — Governance & operations](08-governance-operations.md)
