# Drill 02 — Cutover War Room: 526 Spike

**Time:** 25 min · **Role:** Senior Security Engineer · **Phase:** 3

---

## Scenario inject (read aloud)

> 02:18 UTC — NS cutover complete 15 minutes ago.  
> Synthetic monitor: `https://www.contoso.com` → **526 Invalid SSL certificate**.  
> Priya (DNS): “NS is correct globally.”  
> Marcus (Azure): “AGW is up.”  
> Someone in bridge: “Should we disable WAF?”

---

## Your first 60 seconds (say and do)

**Say:**

> “526 is Cloudflare cannot validate the **origin** certificate — not WAF. Disabling WAF won’t fix this. Marcus, verify cert on App Gateway matches `www.contoso.com` and chain is complete. We stay on Full strict.”

**Do:**

```bash
# From your laptop — confirm edge works, origin SSL fails
curl -sI https://www.contoso.com/ | grep -E "HTTP|cf-ray|server"

# Optional — test origin directly if you have IP (Platform usually does)
curl -vk https://<AGW-IP>/ -H "Host: www.contoso.com" 2>&1 | grep -E "SSL|certificate"
```

---

## Branch A — Marcus fixes cert in 12 min

**You say:**

> “Re-test synthetics. Priya, no NS rollback needed. Log incident for post-mortem — root cause origin cert SAN missing www.”

**You do not:** Take credit for fixing cert — **you directed diagnosis**.

---

## Branch B — Still 526 at T+45

**You say to incident commander:**

> “Recommend DNS rollback to previous NS if origin cert not fixable in window. WAF state irrelevant. Priya owns NS revert per runbook.”

**You do:** Confirm WAF had no block rules (exclude WAF as cause).

---

## Branch C — “Switch to Flexible SSL”

**You:**

> “Flexible encrypts only client-to-Cloudflare — origin sees HTTP. That violates our security architecture and PCI scope. Not an option.”

---

## Debrief — what senior engineers demonstrate

| Behavior | Shown? |
|----------|--------|
| Map 526 to origin cert | ✅ |
| Reject WAF-disable red herring | ✅ |
| Reject Flexible | ✅ |
| Know NS rollback owner is DNS | ✅ |
| Stay on bridge calm | ✅ |

---

[Phase 3](../phases/phase-3-cutover-war-room.md)
