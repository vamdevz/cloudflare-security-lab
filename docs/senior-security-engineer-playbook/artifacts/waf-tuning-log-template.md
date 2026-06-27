# WAF Tuning Log — Contoso (template)

| # | Date | Rule ID | Rule name | TP/FP/Investigate | Sample Ray ID | URI / sample | Disposition | Exception expression | Approver |
|---|------|---------|-----------|-------------------|---------------|--------------|-------------|----------------------|----------|
| 1 | 2026-08-01 | efb7... | CF Managed | TP | 8a1... | `/wp-admin` probe | Block at enforce | — | You |
| 2 | 2026-08-07 | 942100 | SQLi | FP | 9b2... | `/api/v1/search?q=O'Brien` | Skip narrow | path eq search GET | James |
| 3 | 2026-08-07 | 942100 | SQLi | TP | 9c3... | `OR 1=1--` | Block | — | You |
| 4 | | | | | | | | | |

## Weekly summary (paste into SteerCo)

- Log mode days: ___
- Top triggered rule: ___
- Open FP items: ___
- Ready for enforce: Yes / No
