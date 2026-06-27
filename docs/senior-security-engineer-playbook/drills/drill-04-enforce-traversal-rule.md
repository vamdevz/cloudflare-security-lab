# Drill 04 — Enforce: Deploy Path Traversal Rule

**Time:** 25 min · **Role:** Senior Security Engineer · **Phase:** 6

---

## CAB context

**CHG-00258** — Saturday 06:00 UTC — Add custom WAF block rule `CONTOSO-API-TRAVERSAL-01`.

---

## Pre-change — your test script (run against staging)

```bash
#!/bin/bash
BASE="https://staging-api.contoso.com"
PASS=0; FAIL=0

# Attack samples — expect 403
for path in \
  "/api/v1/users/%252e%252e%252fadmin" \
  "/api/v1/files/..%2f..%2fetc%2fpasswd"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE$path")
  [[ "$code" == "403" ]] && ((PASS++)) || ((FAIL++))
  echo "$path → $code"
done

# Legit — expect 200/401 not 403
code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/api/v1/health")
[[ "$code" != "403" ]] && ((PASS++)) || ((FAIL++))
echo "health → $code"

echo "PASS=$PASS FAIL=$FAIL"
```

**Gate:** FAIL must be 0 before production apply.

---

## Change — Terraform snippet you review in PR

```hcl
{
  action      = "block"
  description = "CONTOSO-API-TRAVERSAL-01"
  expression  = <<-EOT
    (starts_with(http.request.uri.path, "/api/") and (
      http.request.uri.path contains "%2e%2e" or
      url_decode(http.request.uri.path, "r") contains ".."
    ))
  EOT
  enabled     = true
}
```

**Lab correlation you document in ticket:**

```bash
curl -i "https://mslearn.site/api/users/%252e%252e%252fadmin"
# 403 — expression validated on lab 2026-06-20
```

---

## Post-change — bridge script (say aloud)

> “Rule live 06:14 UTC. Attack curls 403 with Ray IDs logged. Health 200. James running Postman — standby.”

**If James reports 403 on `/api/v1/documents/../v2/list` (legitimate app routing):**

1. Disable rule (rollback)  
2. Tighten expression — block `%2e%2e` and `%252e` only, not single `../` in known safe pattern  
3. New CAB — do not hotfix in prod without ticket  

---

## Rollback command (Platform runs, you dictate)

```bash
# Dashboard: disable rule CONTOSO-API-TRAVERSAL-01
# Or terraform apply previous git tag v-waf-2026.08.01
```

---

[Phase 6](../phases/phase-6-enforce-custom-rules.md)
