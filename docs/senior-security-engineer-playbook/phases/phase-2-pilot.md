# Phase 2 — Pilot (Week 4)

**Your RACI:** **C** on pilot execution · **R** on security sign-off for production cutover

---

## Mock drill — Pilot results review

**James shares:** Pilot hostname `pilot-www.contoso.com` proxied through Cloudflare. QA passed login and API smoke tests.

**Your job:** Validate **security path**, not functional test cases.

### Checklist you run (real commands)

```bash
# 1. SSL mode — expect 200, valid cert
curl -sI https://pilot-www.contoso.com/ | head -5

# 2. HTTP redirect
curl -sI http://pilot-www.contoso.com/ | grep -i location

# 3. Origin sees CF (Marcus confirms AGW logs show 104.x.x.x / 172.x.x.x sources)

# 4. Deliberate bad path — should reach origin or CF default, NOT block yet
curl -sI "https://pilot-www.contoso.com/api/users/%252e%252e%252fadmin"
# Expect: likely 404/403 from app, NOT WAF 403 yet (no custom rule)
```

### Lab parallel — what you already proved at home

On `mslearn.site` you deployed traversal rule and got **403**:

```bash
curl -i "https://mslearn.site/api/users/%252e%252e%252fadmin"
# HTTP/2 403 — cf-ray: ...
```

**You tell James:**

> “Pilot proves SSL and origin path. Post-cutover week 6 we’ll deploy the same expression on `api.contoso.com` after log observation — I’ll give you the test URLs before CAB.”

### Sign-off email you send

```
To: Lisa (PM), Priya, James, Marcus
Subject: Security sign-off — pilot OK for production cutover planning

Pilot security checks:
✓ Full (strict), no 525/526 in 48h synthetic
✓ CF IPs allowed on AGW (REQ-10422 closed)
✓ No WAF block rules enabled (by design)
✓ api cache bypass confirmed

Conditions for cutover:
- WAF remains log-only on cutover night (CHG-00230)
- HSTS remains OFF

— [Your name], Security
```

**You do not:** Move production NS. **You do:** Block cutover if pilot had 526.

---

[Phase 3 — Cutover war room](phase-3-cutover-war-room.md) · [Drill: 526 spike](../drills/drill-02-cutover-526-spike.md)
