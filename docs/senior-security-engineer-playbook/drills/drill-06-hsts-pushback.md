# Drill 06 — HSTS Pushback from Marketing

**Time:** 15 min · **Role:** Senior Security Engineer · **Phase:** 7

---

## Scenario

**Marketing director (Teams):**  
> “Security scorecard shows B on SSL Labs. Competitors have A+. Enable HSTS preload before our product launch in 10 days.”

**PM Lisa:** “Can we do it?”

---

## Your response (practice verbatim)

> “HSTS tells browsers to never use HTTP for up to a year. If we enable preload before launch and anything still serves mixed content or we need DNS rollback, users get hard failures.  
>   
> Launch in 10 days is **not** compatible with HSTS preload. We can target **A** by fixing mixed content on `/blog` and `/campaign/*` — James’s team — while we run HSTS **stage 1** at 300 seconds **after** day 30 post-cutover per program plan.  
>   
> I’ll share SSL Labs report breakdown by Monday. Platform owns cert; I own timing policy.”

---

## Supporting facts you cite

| Item | Detail |
|------|--------|
| Current day | 22 post-cutover |
| Policy gate | HSTS stage 1 at day 30, max-age 300 |
| Preload | Day 90+ with legal + comms |
| B grade cause | Mixed content `http://cdn.old.contoso.com/logo.png` — not missing HSTS |

---

## What you offer (constructive)

1. Ticket to James — fix mixed content (list 4 URLs from SSL Labs)  
2. Schedule CHG-00301 for day 30 — HSTS 300s  
3. Re-scan SSL Labs after fixes — expect A without preload  

---

## What you refuse

- HSTS preload before launch  
- “Flexible SSL” for quick grade  
- Enabling HTTP/3 same day as HSTS to “compensate”  

---

[Phase 7](../phases/phase-7-hardening-hsts.md)
