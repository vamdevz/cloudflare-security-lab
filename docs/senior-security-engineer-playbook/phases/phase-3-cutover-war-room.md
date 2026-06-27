# Phase 3 — Cutover War Room (Week 5)

**Your RACI:** **C** on NS change · **R/A** on security config during window

**DNS admin (Priya) drives NS.** **You** monitor SSL/WAF and veto bad security toggles.

---

## Mock drill — Saturday 02:00 UTC change window

### T-30 min — Your pre-flight (real dashboard checks)

| Check | Where | Expected |
|-------|-------|----------|
| Managed WAF | Security → WAF | Off or **Log** only |
| HSTS | SSL → Edge Certificates | **Disabled** |
| HTTP/3 | Network | **Off** |
| Custom rules | WAF custom | 0 block rules (or lab-only skip bots) |
| SSL mode | SSL/TLS | Full (strict) |

**You say on bridge:**

> “Security baseline confirmed: no block rules, no HSTS. Priya, you’re clear to update NS when ready.”

### T+0 — Priya updates registrar NS to Cloudflare

**You watch** (not click registrar):

```bash
watch -n 30 "dig NS contoso.com +short @8.8.8.8"
```

### T+15 min — Incident inject (rehearsal)

**Marcus:** “Synthetic monitor red — 526 on www!”

**Your runbook:**

1. **Not WAF** — 526 = invalid origin cert. Check SSL mode first.
2. Ask Marcus: “Did AGW present cert for `www.contoso.com` with full chain?”
3. **Do not** flip to Flexible.
4. If cert fixed in 10 min → continue. If not → advise Priya on NS rollback criteria per [09-rollback](../../enterprise-onboarding-contoso/09-rollback-contingency.md).

**You say:**

> “526 is origin certificate, not WAF. Marcus, verify SNI cert on AGW. I’m not disabling Full strict. Priya, we only rollback NS if still broken at T+60.”

See full drill: [drill-02-cutover-526-spike.md](../drills/drill-02-cutover-526-spike.md)

### T+45 min — Someone suggests “enable OWASP block while we’re here”

**Platform engineer:** “Can we turn on WAF block now that DNS works?”

**You (firm):**

> “No. That’s Phase 6 with CAB. Tonight we only confirm DNS, SSL, and email. I’ll enable managed **log** tomorrow morning CHG-00235.”

### T+2h — Your hypercare Security Events check

Filter: last 2 hours, all actions.

**Expected:** Mostly `allow` / DDoS automatic. No spike in `block` (you didn’t enable block).

**You paste to war room channel** ([templates](../artifacts/war-room-comms-templates.md)):

```
[02:45 UTC] Security: 847k requests, 0 WAF blocks (expected). 12 managed rule LOG hits — review Monday tuning.
Email MX dig OK. Hypercare security green.
```

---

## What you never do in this phase

- Change nameservers at registrar  
- Enable HSTS “because SSL works”  
- Deploy custom block rules from lab repo same night  

---

## Exit — D+1 memo you own

Hypercare day 1 security summary → SteerCo. Hand off to Phase 4 baseline enablement (your ticket CHG-00235).

---

[Phase 4 — Baseline WAF log](phase-4-baseline-waf-log.md)
