# Phase 0 — Discovery (Weeks 1–2)

**Your RACI:** **R/A** on security discovery · **C** on DNS inventory

---

## Mock drill — Tuesday 10:00, Workshop room 3

**Attendees:** You, DNS admin (Priya), App owner API (James), Platform (Marcus), PM (Lisa)

### Scene 1 — You set boundaries (2 min)

**You say:**

> “I’m not here to redesign DNS. I need to know what breaks if we put WAF in front of `api.contoso.com` in three weeks. Priya owns the zone export; James owns app behavior; I’ll turn that into a phased WAF plan.”

### Scene 2 — Real question you ask James

**You:** “Does `/api/v1/connect` accept a base64-encoded hostname in a query parameter named `target`?”

**James:** “Yes — mobile SDK sends `target` for deep links.”

**You write in threat model:**

```markdown
| Path | Param | Encoding | WAF risk |
|------|-------|----------|----------|
| /api/v1/connect | target | base64(url) | SSRF / host header abuse — custom rule candidate Phase 6 |
| Lab validation | mslearn.site /api/connect | same pattern | Expression proven in ADVANCED-WAF-RULES #2 |
```

**Action item:** James sends OpenAPI spec by Friday. **You** mark rule as “observe first, block after FP review.”

### Scene 3 — Real question you ask Priya

**You:** “When we move NS, what MX records must be byte-identical?”

**Priya:** `@ MX 10 mail.contoso.com` and SPF TXT.

**You:** “Those stay **DNS only**, grey cloud — I’ll sign off on proxy status before cutover.”

**You do not:** Export the zone yourself. **You do:** Add row to [discovery checklist](../enterprise-onboarding-contoso/checklists/discovery-checklist.md).

### Scene 4 — Azure ask to Marcus

**You send Teams message:**

```
Marcus — before pilot week, need App Gateway NSG inbound 443 from Cloudflare IP list.
Without this we see 521/522 during orange-cloud tests.
Ticket: REQ-10422. I'll verify from Security Events once James completes pilot curls.
```

---

## Your deliverables this phase

| Deliverable | Real content example |
|-------------|---------------------|
| Threat model v0.1 | 12 API paths, 3 high-risk patterns |
| WAF candidate rules list | Linked to lab rule IDs |
| Risk register entries | R3 WAF FP, R4 SSL 526 |
| Audit baseline | See below |

### Run audit script (lab or staging zone)

```powershell
cd cloudflare-security-lab
$env:CLOUDFLARE_ZONE_NAME = "staging.contoso.com"  # when zone exists
python scripts/zone_security_audit.py
```

**Sample output you paste into discovery report:**

```
Zone: staging.contoso.com
SSL mode: full
Always Use HTTPS: on
Managed WAF: not configured  ← gap, expected pre-cutover
Custom rules: 0
Recommendation: enable managed log post-cutover week 1
```

---

## Exit gate you sign

**Memo subject:** `Contoso CF Phase 0 — Security discovery complete`

> Discovery complete. 14 hostnames inventoried. 3 WAF custom candidates deferred to Phase 6.  
> Blockers: NSG CF IP allowlist (REQ-10422) must complete before pilot.  
> **Recommend proceed to Phase 1 design.**

**You sign.** Priya/James/Marcus co-sign inventory accuracy.

---

## Rehearsal prompt (solo, 5 min)

*“Walk me through Phase 0 as Contoso security lead. Who does DNS? What do you ask the API team? What do you deliver?”*

Expected beats: boundaries → base64/host question → MX grey cloud → NSG ticket → threat model → no WAF block yet.

---

[Phase 1 — Design](phase-1-design.md) · [Drill: API abuse discovery](../drills/drill-01-discovery-api-abuse.md)
