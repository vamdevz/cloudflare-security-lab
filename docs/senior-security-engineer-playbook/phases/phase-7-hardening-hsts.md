# Phase 7 — Hardening: HSTS & HTTP/3 (Week 12+)

**Your RACI:** **R** on policy/timing · Platform **A** on dashboard toggle · App **C**

---

## Mock drill — Steering committee asks for HSTS day 30

**CISO delegate:** “Can we enable HSTS this week? SSL Labs says B.”

**You:**

> “We’re at day 22 post-cutover. Policy is 30 days stable before HSTS stage 1 at max-age 300 seconds — 5 minutes — not preload. B grade is likely mixed content on `/blog` — James’s team fixes that first; HSTS won’t fix HTTP assets.”

**You show staged plan:**

| Stage | When | max-age | preload |
|-------|------|---------|---------|
| 1 | Day 30 | 300 | No |
| 2 | Day 45 | 86400 | No |
| 3 | Day 90 | 31536000 | No |
| 4 | Optional | 31536000 | Yes (legal review) |

**Platform (Marcus)** clicks dashboard when you send CHG-00301 after stage 1 bake-in.

---

## Mock drill — HTTP/3 enable

**You run read-only check first:**

```bash
curl -I --http3 https://www.contoso.com/ 2>/dev/null | head -3
# If unsupported locally, use external monitor
```

**Enable criteria you sign:**

- [ ] 30 days no P1/P2 SSL incidents  
- [ ] Corporate proxy test lab (Contoso VPN) passed  
- [ ] Rollback: disable HTTP/3 in Network tab documented  

**Incident rehearsal:** 3 users report “site won’t load on corporate WiFi” → disable HTTP/3; HTTP/2 fallback automatic.

Full drill: [drill-06-hsts-pushback.md](../drills/drill-06-hsts-pushback.md)

---

## Your steady-state after Phase 7

| Cadence | Activity |
|---------|----------|
| Weekly | Review new Security Events rule IDs |
| Per change | Terraform PR + WAF go-live checklist |
| Quarterly | Token rotation, RBAC review, audit script |
| Annual | Re-run discovery on new hostnames |

---

[Back to playbook index](../README.md)
