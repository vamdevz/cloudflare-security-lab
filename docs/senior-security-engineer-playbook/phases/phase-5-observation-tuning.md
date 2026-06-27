# Phase 5 — Observation & Tuning (Weeks 6–9)

**Your RACI:** **R/A** — this is your **core** phase for 3+ weeks

---

## Mock drill — Weekly tuning meeting #3 (Thursday 10:00)

**Attendees:** You, James (API), SOC analyst (Sam), optional Marcus

### Real data you bring

From Security Events (last 7 days, top rules):

| Rule ID | Description | Hits | Sample URI | Your call |
|---------|-------------|------|------------|-----------|
| `abc-123` | OWASP SQLi | 4,821 | `/api/v1/search?q=1%20OR%201=1--` | **TP** — keep for block |
| `def-456` | OWASP SQLi | 892 | `/api/v1/search?q=O%27Brien%20whiskey` | **FP** — apostrophe in product search |
| `ghi-789` | Anomaly header | 44 | Partner webhook POST | **Investigate** |

### Scene — James pushes back

**James:** “Search breaks if you block SQLi — we get legal product names with quotes.”

**You:**

> “We’re not blocking yet. For enforce week I’ll propose an exception: skip SQLi rule only on `/api/v1/search` GET with query param `q` under 256 chars — not skip all API. Here’s draft expression for your review.”

**Draft skip (narrow):**

```text
(http.request.uri.path eq "/api/v1/search"
 and http.request.method eq "GET"
 and cf.waf.rule_id eq "def-456")
```

**Action:** James tests staging URLs; you add to [tuning log](../artifacts/waf-tuning-log-template.md) row #7.

### Scene — SOC correlation

**Sam:** “Spike in log hits matches app 422 errors — same timestamps.”

**You:**

> “That’s app validation failing, not WAF block — good catch. We’ll note in enforce memo: monitor 422 vs WAF block separately.”

---

## Your weekly rhythm (real calendar)

| Day | Task | Output |
|-----|------|--------|
| Mon | Export top 10 rules from Sentinel | Email to workstream |
| Thu | 60 min tuning meeting | Updated tuning log |
| Fri | Update enforce readiness scorecard | % rules dispositioned |

### Enforce readiness scorecard (example week 4)

| Gate | Status |
|------|--------|
| ≥ 14 days log mode | ✅ 28 days |
| Top 5 rules reviewed | ✅ |
| Open P2 FP tickets | ❌ 1 (search apostrophe) |
| App owner written OK | ⏳ pending James sign-off |
| Rollback tested (disable rule) | ✅ staging |

**You do not** sign enforce until all ✅.

---

Full scenario: [drill-03-weekly-tuning-fp.md](../drills/drill-03-weekly-tuning-fp.md)

---

[Phase 6 — Enforce](phase-6-enforce-custom-rules.md)
