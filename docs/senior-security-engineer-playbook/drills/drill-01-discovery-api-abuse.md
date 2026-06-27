# Drill 01 — Discovery: API Base64 Host Parameter

**Time:** 20 min · **Role:** Senior Security Engineer · **Phase:** 0

---

## Setup

Contoso API team built `/api/v1/connect?target=<base64>` for mobile deep links. You learned this in discovery. A colleague asks: *“Should we block that in WAF on day one?”*

---

## Part A — Answer out loud (3 min)

**Good answer structure:**

1. **Not day one** — cutover + log phase first  
2. **Yes, eventually** — SSRF/host abuse pattern; lab validated expression  
3. **Need app input** — allowlist of decoded hosts  
4. **You don’t own DNS** — you own rule timing and expression  

---

## Part B — Write the threat model row (5 min)

```markdown
## Rule candidate: CF-CUSTOM-002

**Path:** /api/v1/connect  
**Parameter:** target (base64, url-decoded)  
**Risk:** Attacker supplies internal hostname (169.254.169.254, metadata)  
**Phase:** 6 (block)  
**Prerequisite:** 14d log; allowlist from James: api.contoso.com, links.contoso.com  
**Lab reference:** mslearn.site ADVANCED-WAF-RULES #2  
**Expression sketch:**
  starts_with(path, "/api/v1/connect") and len(target) > 0
  and not lower(decode_base64(url_decode(target))) in {allowed hosts}
```

---

## Part C — Email to James (5 min)

```
Subject: Action — allowlist for /api/v1/connect target parameter

Hi James,

For Phase 6 WAF rule CF-CUSTOM-002 we need the complete list of 
legitimate decoded host values your mobile SDK may send in `target`.

Please reply by EOD Friday with FQDNs (not base64).

I will NOT enable this rule before enforce gate sign-off.

Thanks,
[You]
```

---

## Part D — What you refuse (2 min)

**Bad request from PM:** “Can you add the block rule this sprint to show progress?”

**You:** “Progress is the tuning log and log mode metrics — block before observation violates program gates and risks API outage.”

---

## Debrief checklist

- [ ] Named phase for rule (6, not 3)  
- [ ] Asked app for allowlist  
- [ ] Referenced lab without claiming prod deploy  
- [ ] Did not offer to change DNS  

---

[Phase 0](../phases/phase-0-discovery.md)
