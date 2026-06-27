# Drill 03 — Weekly Tuning: Search API False Positive

**Time:** 30 min · **Role:** Senior Security Engineer · **Phase:** 5

---

## Data pack (study 5 min)

Security Events — rule `OWASP-SQLi-942100`, last 7 days:

| Time | URI | Client | Action |
|------|-----|--------|--------|
| Mon 14:02 | `/api/v1/search?q=O%27Brien` | Mobile app | log |
| Mon 14:02 | `/api/v1/search?q=1%20OR%201=1--` | 185.x.x.x | log |
| Tue 09:11 | `/api/v1/search?q=union%20select` | Scanner | log |

James: “If you block SQLi, product search breaks on Irish whiskey names.”

---

## Exercise 1 — Classify (5 min)

| Event | TP or FP? | Action at enforce |
|-------|-----------|-------------------|
| O'Brien search | **FP** | Narrow skip or paranoia tuning |
| OR 1=1 | **TP** | Block |
| union select | **TP** | Block |

---

## Exercise 2 — Write tuning log entry (5 min)

```markdown
| Date | Rule | Type | URI | Disposition | Exception |
|------|------|------|-----|-------------|-----------|
| 2026-08-14 | 942100 | FP | /api/v1/search GET q | Skip only this path+method | Pending James UAT |
```

---

## Exercise 3 — Propose exception (10 min)

**Bad (reject this):**

```text
starts_with(http.request.uri.path, "/api/")
```

**Good:**

```text
(http.request.uri.path eq "/api/v1/search"
 and http.request.method eq "GET"
 and http.request.uri.query contains "q="
 and not ip.src in $partner_scanner_ips)
```

**Say to James:**

> “This skip only affects logged SQLi on search GET — scanners hitting OR 1=1 still block. Test these 10 URLs in staging before I attach to CHG-00241.”

---

## Exercise 4 — Sentinel query (5 min)

Write KQL to count FP candidates:

```kql
CloudflareFirewallEvents
| where RuleID == "942100"
| where ClientRequestURI has "/api/v1/search"
| where ClientRequestURI !has "OR 1=1" and ClientRequestURI !has "union"
| summarize count() by bin(TimeGenerated, 1d)
```

---

## Debrief

You demonstrated **surgical tuning**, not **WAF off**.

---

[Phase 5](../phases/phase-5-observation-tuning.md)
