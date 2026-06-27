# Drill 05 — Incident: Partner Blocked After Block Mode

**Time:** 20 min · **Role:** Senior Security Engineer · **Phase:** 6 (day 2 after enforce)

---

## Scenario

**10:22 UTC Monday** — P2 ticket: Partner **Fabrikam** cannot call `POST /api/v1/orders` — HTTP 403.  
Ray ID: `924abc123def4567`.  
CHG-00241 (managed block) went live Saturday.  
Fabrikam IP: `203.0.113.50` (fixed egress).

---

## Step 1 — Security Events lookup (5 min)

Find event by Ray ID. Example fields you narrate:

```
Action: block
Rule: Cloudflare Managed Ruleset — 949110 (Inbound Anomaly Score)
Client IP: 203.0.113.50
URI: /api/v1/orders
User-Agent: Fabrikam-Integration/2.1
Header: Content-Type: application/json; body 40KB
```

**Hypothesis:** Large JSON body or missing Accept header triggers anomaly score — **not** malicious.

---

## Step 2 — Immediate mitigation (you decide)

**Option A — Emergency skip (narrow):**

```text
(ip.src eq 203.0.113.50
 and http.request.uri.path eq "/api/v1/orders"
 and http.request.method eq "POST")
```

Action: **skip** → specific managed ruleset OR skip all WAF for this flow temporarily.

**Say on bridge:**

> “Emergency skip for Fabrikam IP on orders POST only — valid 24h. Retro CAB today. Not disabling global WAF.”

---

## Step 3 — Permanent fix (next CAB)

- Lower paranoia for API path via config rule  
- Or move Fabrikam to **mTLS** / **Cloudflare API Shield** (Enterprise roadmap)  
- Update tuning log; Fabrikam on IP allowlist **only if** IP is stable (document risk)

---

## Step 4 — Comms template

```
To: Fabrikam ops, James, Lisa
Subject: RESOLVED — 403 on orders API

Root cause: Managed WAF anomaly rule blocked legitimate large POST.
Mitigation: Narrow skip applied 10:45 UTC. Service restored.
Permanent fix: CHG-00267 Friday — API path exception review.

Ray ID: 924abc123def4567
```

---

## Debrief — senior behaviors

- Used Ray ID  
- Narrow skip, not global off  
- Emergency authority + retro CAB  
- Partner comms without blaming app team  

---

[Phase 6](../phases/phase-6-enforce-custom-rules.md)
