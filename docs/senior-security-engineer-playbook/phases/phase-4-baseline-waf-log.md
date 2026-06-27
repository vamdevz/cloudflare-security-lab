# Phase 4 — Baseline WAF Log (Week 5–6)

**Your RACI:** **R/A** — you execute this; SOC observes

---

## Mock drill — Monday after cutover, 09:00

**Ticket CHG-00235:** Enable Cloudflare Managed Ruleset in **Log** mode.

### Step 1 — Dashboard (Enterprise)

**Path:** Security → WAF → Managed rules → Cloudflare Managed Ruleset → **Log**

**You screenshot** before/after for change record.

### Step 2 — Verify events flow

Within 15 minutes, Security Events should show `action: log` for probe traffic.

**Real filter (dashboard or GraphQL concept):**

```
action eq "log" and datetime ge 15 minutes ago
```

### Step 3 — Notify SOC

**Email:**

```
To: soc@contoso.com
Subject: Contoso WAF now logging — no blocks yet

Managed ruleset set to LOG as of 09:12 UTC.
Dashboard: Security → Events (zone contoso.com)
Expected: log entries on scanners; zero production blocks.
Weekly tuning: Thursdays 10:00 with App team.
Tuning log: \\share\\security\\contoso-waf-tuning.xlsx
```

### Step 4 — Logpush spec (you write; Platform/SOC deploys)

```json
{
  "dataset": "firewall_events",
  "destination": "azure_blob://contosologs/cf/firewall/",
  "retention_days": 90,
  "fields": ["RayID", "Action", "RuleID", "ClientIP", "ClientRequestURI", "UserAgent"]
}
```

**Your role:** Requirements + validate first events in Sentinel query:

```kql
CloudflareFirewallEvents
| where TimeGenerated > ago(1h)
| where Action == "log"
| summarize count() by RuleID
| top 10 by count_
```

---

## What if you're on Free plan (lab)?

On `mslearn.site` there is no `log` action — you use Security Events + skip rules with logging. **Tell Contoso Enterprise:** “Lab proved expressions; production uses log before block.”

---

## Exit criteria (you sign)

- [ ] Managed rules logging ≥ 7 days  
- [ ] SOC receiving Logpush or manual export  
- [ ] Zero block rules enabled  
- [ ] Tuning meeting #1 scheduled  

---

[Phase 5 — Observation](phase-5-observation-tuning.md)
