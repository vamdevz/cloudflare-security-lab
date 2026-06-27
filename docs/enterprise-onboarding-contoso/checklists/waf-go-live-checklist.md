# WAF Go-Live Checklist — Per Rule Wave

Use **one checklist instance per rule change** (managed block, custom group A, etc.).

**Change ticket:** _______________  
**Rule description:** _______________  
**Window:** _______________

## Pre-change

- [ ] Observation phase sign-off on file
- [ ] Rule expression reviewed in staging / lower paranoia
- [ ] Terraform PR approved (or emergency pre-approved)
- [ ] Rollback: disable rule ID _______________
- [ ] App owner notified; support on standby
- [ ] Baseline block rate captured (last 7 days)

## Test plan (before enable)

| Test | Command / step | Expected |
|------|----------------|----------|
| Attack sample | `curl` malicious payload | 403 + Ray ID |
| Legit API | Production-like client | 200 |
| Legit web | Browser flow login | Success |
| Partner IP | Partner test call | 200 |

## Enable

- [ ] Rule enabled in **log** first (if not already validated)
- [ ] Monitor Security Events 30 min
- [ ] Switch to **block** (if applicable)
- [ ] Monitor 24h

## Post-change (24h)

- [ ] Block rate vs baseline acceptable
- [ ] No P2+ false positive tickets open
- [ ] SIEM alert thresholds updated
- [ ] Terraform state matches dashboard
- [ ] Change ticket closed

## Rollback executed?

- [ ] No
- [ ] Yes — reason: _______________

**Approver:** _______________
