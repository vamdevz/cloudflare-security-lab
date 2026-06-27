# Senior Security Engineer — Role Playbook (Contoso + Cloudflare)

Hands-on **mock drills** and **real implementation examples** for the **Senior Cloud Security Engineer** on a Contoso-style Cloudflare Enterprise onboarding.

You are **not** the DNS admin. You are **not** the app owner. You **are** accountable for edge security outcomes: WAF phasing, tuning, enforcement gates, Azure↔Cloudflare integration, and incident response when security controls misbehave.

---

## How to use this playbook

1. Read [Role scope & RACI](01-role-scope-and-raci.md) once.
2. Walk each **phase doc** in order — each includes a **mock drill** you can rehearse aloud.
3. Run **scenario drills** under [drills/](drills/) as timed exercises (15–30 min each).
4. Copy **artifacts** from [artifacts/](artifacts/) into your own notes.

**Companion docs:** [Enterprise onboarding](../enterprise-onboarding-contoso/README.md) · [Advanced WAF rules](../ADVANCED-WAF-RULES.md) · Lab domain `mslearn.site`

---

## Phase map — what you do vs others

| Phase | You (Security) | Others | Drill doc |
|-------|----------------|--------|-----------|
| 0 Discovery | Threat model, app/WAF questionnaire | DNS exports zone; App lists APIs | [Phase 0](phases/phase-0-discovery.md) |
| 1 Design | WAF phasing, SSL policy, RBAC | Architecture board sign-off | [Phase 1](phases/phase-1-design.md) |
| 2 Pilot | Review SSL/WAF test evidence | Platform + QA run pilot | [Phase 2](phases/phase-2-pilot.md) |
| 3 Cutover | War room: block **no** WAF block tonight | DNS changes NS | [Phase 3](phases/phase-3-cutover-war-room.md) |
| 4 Baseline | Enable managed WAF **Log** | Platform sets Full strict | [Phase 4](phases/phase-4-baseline-waf-log.md) |
| 5 Observation | Weekly tuning; FP triage | App validates samples | [Phase 5](phases/phase-5-observation-tuning.md) |
| 6 Enforce | Block mode + custom rules (Terraform) | CAB approves windows | [Phase 6](phases/phase-6-enforce-custom-rules.md) |
| 7 Hardening | HSTS/HTTP/3 go-no-go | Platform toggles dashboard | [Phase 7](phases/phase-7-hardening-hsts.md) |

---

## Scenario drill catalog

| # | Scenario | Time | File |
|---|----------|------|------|
| 1 | Discovery workshop — API uses base64 host param | 20 min | [drill-01-discovery-api-abuse.md](drills/drill-01-discovery-api-abuse.md) |
| 2 | Cutover war room — 526 spike | 25 min | [drills/drill-02-cutover-526-spike.md](drills/drill-02-cutover-526-spike.md) |
| 3 | Weekly tuning — OWASP FP on search API | 30 min | [drills/drill-03-weekly-tuning-fp.md](drills/drill-03-weekly-tuning-fp.md) |
| 4 | Enforce day — deploy path traversal rule | 25 min | [drills/drill-04-enforce-traversal-rule.md](drills/drill-04-enforce-traversal-rule.md) |
| 5 | Incident — partner blocked after block mode | 20 min | [drills/drill-05-partner-blocked-incident.md](drills/drill-05-partner-blocked-incident.md) |
| 6 | HSTS decision — marketing wants it day one | 15 min | [drills/drill-06-hsts-pushback.md](drills/drill-06-hsts-pushback.md) |

---

## Artifacts (copy-paste templates)

- [WAF tuning log](artifacts/waf-tuning-log-template.md)
- [CAB ticket — managed rules to block](artifacts/cab-ticket-managed-rules-block.md)
- [Enforce readiness memo](artifacts/enforce-readiness-memo-template.md)
- [War room Slack/Teams messages](artifacts/war-room-comms-templates.md)

---

## 30-second role pitch (rehearse this)

> “Platform owns DNS cutover and origin on Azure. App teams own functional behavior. I own **Cloudflare security policy**: phased WAF from log to block, custom rules for our API threat model, Logpush to Sentinel, and the gate that says we’re ready to enforce. I’m in the cutover war room for SSL and WAF incidents, but I won’t move nameservers — and I won’t enable block rules the same night we do.”

---

*Fictional customer: Contoso. Lab reference: mslearn.site patterns in this repo.*
