# RACI Matrix — Contoso Cloudflare Onboarding

**R** = Responsible · **A** = Accountable · **C** = Consulted · **I** = Informed

| Activity | PM | DNS admin | Platform | Security | App owner | SOC | CF consultant |
|----------|----|-----------|----------|----------|-----------|-----|---------------|
| Discovery workshops | A | R | C | R | C | I | R |
| Architecture sign-off | A | C | C | R | C | I | R |
| Pilot testing | I | C | R | C | R | I | C |
| TTL lowering | I | R/A | C | I | I | I | C |
| NS cutover | C | R/A | R | C | C | I | R |
| SSL/TLS baseline | I | C | R | C | C | I | C |
| WAF log enable | I | I | C | R/A | C | R | C |
| Observation / tuning | I | I | C | R/A | R | R | C |
| WAF block enforce | C | I | C | R/A | C | R | C |
| Custom WAF rules | I | I | R | R/A | C | R | C |
| Logpush / SIEM | I | I | R | C | I | R/A | C |
| HSTS / HTTP/3 | C | I | R/A | R | C | I | C |
| NS rollback | C | R/A | C | C | I | I | C |
| WAF rollback | I | I | C | R/A | C | R | C |
| SteerCo reporting | R/A | I | I | C | I | I | C |

## Escalation to Cloudflare Enterprise support

| Severity | Example | Channel |
|----------|---------|---------|
| P1 | Production down, CF-related | Phone + ticket |
| P2 | WAF widespread FP | Ticket |
| P3 | Tuning question | TAM email |
