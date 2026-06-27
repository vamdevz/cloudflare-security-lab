# Stakeholder Walkthrough Guide — 45 Minute Version

Use this narrative when leading Contoso IT, Security, and App teams through the proposed Cloudflare onboarding. Adjust depth by audience.

---

## Minute 0–5 — Problem & outcome

**Say:**  
Contoso needs consistent DDoS and WAF at the edge, unified TLS, and visibility we do not get from origin-only security. The goal is **not** to turn on every Cloudflare feature on day one. The goal is **zero unplanned outage** during DNS migration and **phased security** so we do not break API or checkout flows.

**Show:** [Executive summary](../00-executive-summary.md) success criteria table.

---

## Minute 5–12 — Why DNS and WAF are separate phases

**Say:**  
When nameservers move to Cloudflare, the Internet starts resolving to Cloudflare anycast IPs. That alone changes TLS termination and client IP visibility. If we simultaneously enable aggressive WAF block rules, we cannot tell whether a failure is DNS, SSL, or a false positive.

**Show:** Phase diagram in [README](../README.md) — cutover → baseline → observe → enforce.

**Key line:**  
> Golden rule: nameservers first, WAF block later.

---

## Minute 12–20 — Discovery & pilot (de-risk before production)

**Say:**  
We inventory every DNS record — especially email — and prove the app works through Cloudflare on a **pilot** hostname before touching production NS.

**Show:** [Discovery checklist](../checklists/discovery-checklist.md) email/DNS section.

**Questions to invite:**

- Who owns registrar access?
- Any WebSockets or large uploads on API?
- Which paths must never be cached?

---

## Minute 20–28 — Cutover mechanics (what happens on the night)

**Walk through** [Pre-cutover checklist](../checklists/pre-cutover-checklist.md):

1. TTL lowered 72h ahead  
2. Zone imported; MX copied exactly  
3. SSL Full (strict) validated  
4. NS changed at registrar  
5. Hypercare 5 days  
6. **WAF log only; HSTS off; HTTP/3 off**

**Show:** SSL error table (525/526) from [migration doc](../04-migration-cutover.md).

**Rollback:** One slide on NS revert ([09-rollback](../09-rollback-contingency.md)).

---

## Minute 28–35 — Security phasing (their main concern)

**Say:**  
Managed WAF runs in **log mode** for a minimum of two weeks. Security and app owners review Security Events weekly. We only move to **block** after a signed memo. Custom rules (path traversal, API abuse) deploy **one group per week**.

**Show:** [WAF phasing table](../05-waf-security-phasing.md) waves 0–4.

**Connect to lab (optional):**  
We validated expression syntax on a test domain; Contoso uses the same patterns with Enterprise log/simulate first.

---

## Minute 35–40 — Advanced TLS (HSTS, HTTP/3)

**Say:**  
HSTS tells browsers to never use HTTP again. If we enable it too early, rollback becomes painful. We stage max-age from 5 minutes → 1 day → 1 year over **months**, not cutover night. HTTP/3 is enabled only after 30 days stable; some corporate networks block QUIC — we keep HTTP/2 fallback.

**Show:** HSTS staging table in [07-ssl-tls-advanced](../07-ssl-tls-advanced.md).

---

## Minute 40–45 — Governance & next steps

**Say:**  
Every production WAF change goes through Terraform and PR review. Logs stream to Sentinel. API tokens are zone-scoped. Enterprise TAM on speed dial for cutover week.

**Show:** [RACI](raci.md) + [08-governance](../08-governance-operations.md).

**Close with ask:**

- Approve Phase 0 discovery workshops  
- Assign DNS admin + Security + App owner names  
- Propose cutover window (avoid quarter-end / marketing launches)

---

## Anticipated questions (quick answers)

| Question | Answer |
|----------|--------|
| Will email break? | Not if MX/SPF/DKIM are cloned and grey-clouded |
| Downtime during NS change? | No hard outage; TTL-bound propagation only |
| Can we pause WAF? | Yes — log mode or disable rules in minutes |
| Why not HSTS day one? | Rollback and cert incidents become harder |
| How long until full security? | ~12 weeks typical; block mode ~week 6+ |
| What about internal apps? | Zero Trust / Access — separate project |

---

[Back to index](../README.md)
