# Phase 1 — Design (Week 3)

**Your RACI:** **R/A** on security architecture · **C** on overall target state

---

## Mock drill — Architecture review board

**You present slides 4–7 only** (security slice). Platform presents network diagram.

### Slide you present — WAF phasing (real content)

```
Phase 3 cutover:  WAF managed = OFF or LOG only
Week 1 post-cut:  Managed ruleset → LOG (Enterprise)
Weeks 2–5:        Weekly tuning; tuning log
Week 6:           Managed → BLOCK (CAB CHG-00241)
Weeks 7–8:        Custom rules one group/week
HSTS:             NOT before day 30
HTTP/3:           NOT before day 30
```

**Board member:** “Why not block OWASP on day one?”

**You:**

> “We change authoritative DNS that night. If checkout fails, we need to know it’s cert or DNS — not a false positive on SQLi in a JSON cart field. Log mode gives us Ray IDs tied to rule IDs before we block.”

### Real design decision you document

**Decision log entry DEC-014:**

| ID | Decision | Rationale | Approver |
|----|----------|-----------|----------|
| DEC-014 | api.contoso.com cache = bypass | Auth headers; no stale API | James + You |
| DEC-015 | Custom base64 host rule Phase 6 only | Mobile SDK uses param | You |
| DEC-016 | Logpush firewall → Sentinel 90d | SOC requirement | SOC lead |

### Token design you write (not share in Git)

```yaml
# Terraform CI token — contoso-terraform-prod
permissions:
  - Zone:Zone:Read
  - Zone:Zone Settings:Read
  - Zone:Firewall Services:Edit
  - Zone:DNS:Read   # read-only for drift check
resources:
  - Zone: contoso.com zone_id only
```

**Platform** stores in Azure Key Vault; **you** define scopes.

---

## What you review (not author)

| Artifact | Owner | Your review comment example |
|----------|-------|----------------------------|
| Network diagram | Marcus | “Add CF IP allowlist on AGW NSG” |
| DNS import plan | Priya | “Confirm api CNAME proxied orange” |
| Rollback runbook | PM | “Add WAF disable steps before NS revert” |

---

## Exit gate

Architecture sign-off with your **security exceptions** appendix attached — list every hostname and Phase 4–7 control timing.

---

[Phase 2 — Pilot](phase-2-pilot.md)
