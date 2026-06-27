# Rollback & Contingency

## When to rollback

| Symptom | Likely cause | First action |
|---------|--------------|--------------|
| Site down globally | DNS/NS error | Verify NS; rollback NS if wrong |
| 525/526 everywhere | SSL mode / origin cert | Temp Full (not strict) **only** with Security approval |
| API broken for all users | WAF block | Set managed rules to Log; disable last custom rule |
| Email stopped | MX/SPF wrong | Fix DNS records; grey-cloud mail records |
| Partial region down | Propagation | Wait TTL; check registrar NS |

**Decision authority:** Incident commander + DNS admin (NS rollback) or Security (WAF rollback).

---

## Rollback A — Nameservers (full revert)

**Use when:** Critical outage and Cloudflare config cannot be fixed within RTO (4h).

### Steps

1. Document current Cloudflare NS values (for forensics)
2. At registrar, restore **previous** nameservers:
   ```
   ns1.contoso-dns-provider.com
   ns2.contoso-dns-provider.com
   ```
3. Verify propagation: `dig NS contoso.com @8.8.8.8`
4. Confirm traffic bypasses Cloudflare (origin sees client IPs directly)
5. Post-incident review before re-attempting migration

**Note:** If HSTS was enabled with long max-age, browsers may still force HTTPS — rollback planning must account for this.

---

## Rollback B — WAF only (keep Cloudflare proxy)

**Use when:** Application broken but edge/DNS is correct.

### Fast mitigation (minutes)

1. Security → WAF → Managed rules → set to **Log** or **Off**
2. Disable most recent custom rule (change ticket ID)
3. Purge cache if stale content suspected
4. Communicate Ray ID to users for support

### API rollback single rule

```bash
# Disable by updating ruleset — prefer Terraform revert PR
# Emergency: dashboard toggle on rule
```

---

## Rollback C — SSL mode downgrade (controlled)

**Use when:** Origin cert broken mid-incident.

| Mode | Risk |
|------|------|
| Full (strict) → Full | Accepts self-signed origin temporarily |
| Full → Flexible | **Avoid** — bypasses origin encryption |

Always treat Flexible as **last resort**; fix origin cert instead.

---

## Rollback D — HTTP/3 / HSTS

| Feature | Rollback |
|---------|----------|
| HTTP/3 | Dashboard → Network → disable HTTP/3 |
| HSTS short max-age | Reduce max-age to 0; wait cache expiry |
| HSTS preload | Cannot quickly undo — prevention only |

---

## War room contacts

| Role | Name | Phone | Escalation |
|------|------|-------|------------|
| Incident commander | TBD | | |
| DNS admin | TBD | | NS rollback |
| Cloudflare TAM | Enterprise support | | CF ticket P1 |
| App owner | TBD | | Functional validation |
| Security lead | TBD | | WAF rollback |

---

## Communication templates

### Internal (outage)

> Contoso.com traffic is experiencing [issue]. Cause under investigation.  
> Actions: [WAF reverted / NS rollback in progress].  
> Next update: [time]. ETA: [time].

### External (status page)

> We are investigating connectivity issues affecting our website.  
> API services [impacted / not impacted]. Updates every 30 minutes.

---

## Post-incident requirements

Within 5 business days:

- Timeline with Ray IDs and rule IDs
- Root cause (5 whys)
- Updated runbook
- Re-schedule cutover with additional gates

---

[Back to index](README.md)
