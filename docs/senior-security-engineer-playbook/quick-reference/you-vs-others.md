# Quick Reference — You vs Others (Contoso)

| Situation | You say/do | They say/do |
|-----------|------------|-------------|
| “Who changes nameservers?” | “Priya owns registrar NS update; I review checklist.” | Priya executes NS |
| “526 errors after cutover” | “Origin cert issue — Marcus fixes AGW; not WAF.” | Marcus fixes cert |
| “Enable WAF block tonight” | “No — CHG-00241 next week after observation.” | PM may push — you hold gate |
| “Fix DNS record” | “Log ticket to Priya; I verify proxy status on web records.” | Priya edits DNS |
| “App returns 500” | “Check origin; if WAF block, Ray ID in Security Events.” | James debugs app |
| “Allow Cloudflare on firewall” | “REQ filed — verify before pilot.” | Marcus NSG change |
| “HSTS for launch” | “Stage 1 day 30; fix mixed content first.” | Marketing wants A+ |
| “Deploy custom rule” | “Terraform PR + CAB; curl test pack attached.” | Platform applies |
| “Partner 403” | “Ray ID → narrow skip → retro CAB.” | Partner reports |

## Phase one-liners (memorize)

| Phase | Your one-liner |
|-------|----------------|
| 0 | “I build threat model; DNS exports zone.” |
| 1 | “I design log→block phasing; board signs security appendix.” |
| 2 | “I sign security path on pilot; QA signs function.” |
| 3 | “War room — I guard SSL/WAF; DNS moves NS.” |
| 4 | “I turn managed WAF to log; SOC watches.” |
| 5 | “I run tuning log — no block until memo signed.” |
| 6 | “I ship rules one CAB at a time with curl proof.” |
| 7 | “I set HSTS/HTTP/3 policy; Platform toggles.” |
