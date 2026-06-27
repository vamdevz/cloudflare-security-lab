# Enforce Readiness Memo — Template

**To:** Lisa (PM), James (App), Sam (SOC), Marcus (Platform)  
**From:** [You], Senior Cloud Security Engineer  
**Subject:** Contoso WAF — Ready for managed rules BLOCK (CHG-00241)

---

## Observation summary

| Gate | Required | Actual | Status |
|------|----------|--------|--------|
| Log mode duration | ≥ 14 days | 28 days | ✅ |
| Weekly tuning meetings | 4 | 4 | ✅ |
| Top 5 rules reviewed | Yes | Yes | ✅ |
| Open P2+ FP tickets | 0 | 0 | ✅ |
| App owner approval | Written | Attached | ✅ |
| Rollback tested | Staging | 2026-08-10 | ✅ |

## Metrics

- Total requests (7d avg): 12.4M/day  
- Managed rule log hits: 0.08% of traffic  
- Confirmed FP after skip design: 2 (documented in tuning log #2, #8)  
- Confirmed TP: 847 scanner events/week  

## Rules entering block mode

1. Cloudflare Managed Ruleset — default block  
2. Exceptions: tuning log #2 (search GET skip), #8 (Fabrikam staging IP — remove before prod if not needed)

## Not in scope this change

- Custom traversal rule → CHG-00258 next week  
- HSTS → Phase 7  
- HTTP/3 → Phase 7  

## Recommendation

**Approve CHG-00241** for Saturday 06:00 UTC.

---

**App owner approval:**  
James _______________ Date _______

**Security approval:**  
[You] _______________ Date _______
