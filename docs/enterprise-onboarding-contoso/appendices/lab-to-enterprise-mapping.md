# Lab-to-Enterprise Mapping — mslearn.site → Contoso

This appendix connects hands-on work on **`mslearn.site`** (personal lab) to the **Contoso Enterprise** playbook — what transfers directly vs what must be added for production.

## What the lab already proved

| Lab activity | Enterprise equivalent | Contoso phase |
|--------------|----------------------|---------------|
| Zone added to Cloudflare | Production zone import | Phase 2–3 |
| Orange-cloud DNS | Proxied A/CNAME records | Phase 3 cutover |
| SSL Full (strict) | Same | Phase 3 |
| Custom WAF expressions (base64 host, traversal) | Custom rule groups A–C | Phase 6 |
| `curl` validation with Ray ID | Rule test plan per change | Phase 6 |
| `zone_security_audit.py` | Pre/post audit in CI | Phase 0, 4, steady state |
| Terraform WAF starter | GitOps for rules | Phase 6+ |
| API token in `.env` only | Scoped tokens + vault | Phase 1 governance |

## What Enterprise adds (not in lab)

| Capability | Why it matters |
|------------|----------------|
| **Log** action on managed WAF | Observe before block — Free plan lacks this |
| Logpush to SIEM | Compliance, correlation with Azure AD / app logs |
| SSO + RBAC | Separation of duties |
| Account teams | Multi-brand / multi-zone governance |
| TAM / priority support | Cutover war room escalation |
| Advanced Certificate Manager | Wildcard + SAN control |
| Rate limiting rules (separate product) | Auth endpoint abuse |
| Bot Management | After baseline traffic known |

## Rule deployment comparison

| Aspect | mslearn.site (lab) | contoso.com (Enterprise) |
|--------|-------------------|--------------------------|
| Rollout speed | Same day experiments | CAB windows; one wave/week |
| First action | Often block (learning) | **Log** 14+ days |
| Rule count | 5 (Free max) | Many; merged expressions |
| False positive impact | Low (test domain) | Revenue / API SLA |
| Rollback | Delete rule in dashboard | Terraform revert + comms |

## Expression reuse

Rules documented in [ADVANCED-WAF-RULES.md](../../ADVANCED-WAF-RULES.md) are **candidates** for Contoso phase 6 — not cutover day defaults.

| Lab rule | Contoso hostname | Pre-requisite |
|----------|------------------|---------------|
| Base64 host on `/api/connect` | Only if app uses encoded hosts | App owner confirms parameter |
| Path traversal `/api/*` | `api.contoso.com` | Observation shows probes |
| Method override headers | API zone | Log shows attempts |
| Host allowlist | API zone | Partner Host headers reviewed |

## Audit script usage

```powershell
# Lab / staging
$env:CLOUDFLARE_ZONE_NAME = "mslearn.site"
python scripts/zone_security_audit.py

# Contoso staging (separate token recommended)
$env:CLOUDFLARE_ZONE_NAME = "staging.contoso.com"
python scripts/zone_security_audit.py
```

Compare audit output before cutover and after each WAF wave.

## Engineering note for stakeholder walkthroughs

When explaining the engagement to Contoso leadership:

1. **Start with risk:** DNS change is controlled; security is phased.
2. **Show the timeline:** 12-week diagram from [project plan](../03-project-plan-milestones.md).
3. **Demo lab curl** (optional): one blocked traversal on test domain — proves competence, not production config.
4. **Emphasize gates:** Observation sign-off before any block mode.
5. **Close with operations:** Terraform, Logpush, RACI — not a one-time migration.

---

[Back to index](../README.md)
