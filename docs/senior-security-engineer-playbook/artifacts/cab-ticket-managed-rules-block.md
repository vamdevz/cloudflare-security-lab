# CAB Ticket Template — Managed WAF Log → Block

```
Change: CHG-00241
Type: Standard
Risk: Medium
Window: Saturday 06:00–08:00 UTC
Implementer: [Platform engineer]
Verifier: [You — Security]
Backout: Set managed ruleset to Log (dashboard or Terraform revert PR #46)
```

## Description

Enable **Block** on Cloudflare Managed Ruleset for zone `contoso.com` after 28-day observation period.

## Justification

- 28 days log mode complete  
- Tuning log entries #1–12 dispositioned  
- App owner sign-off attached  
- FP rate < 0.1% in log sample  

## Test plan

| # | Test | Expected |
|---|------|----------|
| 1 | Scanner payload `OR 1=1` on `/api/v1/users` | 403 |
| 2 | Legit search `O'Brien` with skip rule | 200 |
| 3 | Health `/api/v1/health` | 200 |
| 4 | Partner Fabrikam POST orders | 200 |

## Security engineer pre-approval

> I confirm observation gates met and rollback tested on staging.  
> Signed: _______________ Date: _______________
