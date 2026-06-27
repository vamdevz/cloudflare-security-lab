# Governance & Operations

## Operating model (steady state)

| Function | Responsibility |
|----------|----------------|
| **Platform team** | DNS records, SSL mode, cache rules |
| **Security team** | WAF rules, rate limits, IP lists |
| **SOC** | Security Events, Logpush alerts, incident triage |
| **App owners** | False positive validation, UAT for rule changes |

## Change control

| Change type | Approval | Method |
|-------------|----------|--------|
| DNS record (prod) | DNS admin + CAB | Terraform PR |
| WAF managed mode Log→Block | Security + App owner | Terraform PR + ticket |
| Custom WAF rule | Security | Terraform PR |
| Emergency block (0-day) | Security on-call | Dashboard + retro PR within 24h |
| Cache purge everything | Platform | Ticket + peer approve |

## API token strategy

| Token name | Scope | Used by |
|------------|-------|---------|
| `contoso-terraform-prod` | Zone WAF + DNS edit (prod zone only) | CI pipeline |
| `contoso-audit-readonly` | Zone read | Audit scripts |
| `contoso-break-glass` | Account admin | Vault, 2 custodians |

**Never:** store tokens in Git; rotate every 90 days; use short-lived tokens where available.

Align with lab `.env.example` pattern — IDs and tokens in local `.env` only.

## RBAC (Enterprise)

| Role | Permissions |
|------|-------------|
| Administrator | Account settings (minimal headcount) |
| Security Admin | WAF, Firewall, Tools |
| DNS Editor | DNS only |
| Analytics | Read-only dashboards |
| Cache Purge | Purge + read |

Enable **SSO (SAML)** with Contoso Entra ID; enforce MFA.

## Infrastructure as code

```
terraform/
├── modules/
│   └── waf-ruleset/
├── environments/
│   ├── staging/     # contoso-staging zone
│   └── prod/        # contoso.com
└── backend.tf       # Azure Storage remote state
```

**Workflow**

1. Engineer opens PR with rule change
2. `terraform plan` in CI (Cloudflare provider)
3. Security reviewer approves
4. Apply in maintenance window
5. Post-change validation (`curl` + Security Events)

Lab reference: `terraform/main.tf` in this repo.

## Drift detection

Weekly job:

```powershell
python scripts/zone_security_audit.py
# Compare output to last baseline; alert on SSL mode or WAF downgrades
```

Future: export rulesets via API and diff against Terraform state.

## Logpush & SIEM

| Alert | Condition | Severity |
|-------|-----------|----------|
| WAF spike | Block rate > 3× baseline 15 min | P3 |
| Origin 5xx | > 1% 5 min | P2 |
| SSL handshake fail | Any 525/526 sustained | P1 |
| DDoS attack | CF notification | P2 |

Map Cloudflare rule IDs to Sentinel analytics rules.

## Documentation deliverables (handoff)

- [ ] Architecture diagram (as-built)
- [ ] DNS runbook
- [ ] WAF tuning log
- [ ] Token inventory + rotation schedule
- [ ] Escalation matrix (Cloudflare Enterprise support TAM)
- [ ] Decision log (HSTS, HTTP/3 dates)

## Compliance mapping (example)

| Requirement | Control |
|-------------|---------|
| Encryption in transit | Full (strict), TLS 1.2+ |
| Access control | SSO + RBAC |
| Audit trail | Logpush + Terraform git history |
| Change management | CAB + PR |
| DDoS resilience | CF automatic + runbook |

---

Next: [09 — Rollback & contingency](09-rollback-contingency.md)
