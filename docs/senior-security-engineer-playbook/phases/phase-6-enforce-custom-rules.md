# Phase 6 — Enforce & Custom Rules (Weeks 9–11)

**Your RACI:** **R/A** on rule content and rollout · Platform executes Terraform apply

---

## Mock drill — CAB night CHG-00241: Managed rules → Block

### Before window — your test pack (send to James)

```bash
# Should BLOCK after change (attack)
curl -i "https://api.contoso.com/api/v1/admin?id=1'%20OR%201=1--"

# Should PASS (legit — with agreed skip for search)
curl -i "https://api.contoso.com/api/v1/search?q=O%27Brien"

# Capture Ray ID header on any failure
```

### During window — you do (or pair with Platform)

**Option A — Dashboard:** Managed ruleset → **Block**

**Option B — Terraform PR #47 (preferred Enterprise)**

```hcl
resource "cloudflare_ruleset" "managed" {
  zone_id = var.zone_id
  name    = "zone"
  kind    = "zone"
  phase   = "http_request_firewall_managed"

  rules {
    action      = "execute"
    expression  = "true"
    action_parameters {
      id = "efb7b8c949ac4650a09736fb37514609"  # Cloudflare Managed Ruleset ID
      overrides {
        rules {
          id      = "def-456"  # SQLi rule
          action  = "block"
        }
      }
    }
  }
}
```

### T+30 min validation

**You in bridge:**

> “Block rate 0.02% of traffic — within baseline. James, run Postman collection — green? Sam, any Sentinel P2 alerts?”

If FP spike → **you** set affected rule to log or deploy skip — do not wait for DNS rollback.

---

## Mock drill — Week 7: Custom rule group A (path traversal)

**CAB CHG-00258** — one rule only.

### Expression (from lab, production hostname)

```text
(starts_with(http.request.uri.path, "/api/") and (
  http.request.uri.path contains "%2e%2e" or
  url_decode(http.request.uri.path, "r") contains ".."
))
```

### Deploy via repo pattern

```powershell
# .env has CLOUDFLARE_ZONE_ID, CLOUDFLARE_CUSTOM_RULESET_ID, token
python scripts/deploy_advanced_waf_rules.py  # adapt expressions for Contoso in Terraform ideally
```

**Lab proof you cite internally:**

```bash
curl -i "https://mslearn.site/api/users/%252e%252e%252fadmin"
# HTTP/2 403
```

### Rollback you rehearse

1. Dashboard → disable rule “Contoso block path traversal API”  
2. Or `terraform apply` previous commit  
3. Post to channel: “CHG-00258 rolled back rule ID xxx — FP on partner path /api/v1/legacy/export”

Full drill: [drill-04-enforce-traversal-rule.md](../drills/drill-04-enforce-traversal-rule.md)

---

## Enforce memo you sign (template)

Use [enforce-readiness-memo-template.md](../artifacts/enforce-readiness-memo-template.md).

---

[Phase 7 — Hardening](phase-7-hardening-hsts.md) · [Partner blocked incident](../drills/drill-05-partner-blocked-incident.md)
