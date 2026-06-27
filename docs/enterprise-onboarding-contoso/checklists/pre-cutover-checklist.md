# Pre-Cutover Checklist — Contoso

**Change ticket:** _______________  
**Window:** _______________ (UTC)

## T-72h

- [ ] TTL lowered to 300s at current DNS provider
- [ ] Full zone imported to Cloudflare; diff matches export
- [ ] MX/SPF/DKIM/DMARC verified character-for-character
- [ ] Proxy status correct (web orange, mail grey)
- [ ] Universal SSL / ACM cert active for all hostnames
- [ ] SSL mode Full (strict) tested from CF to origin
- [ ] Origin allows Cloudflare IP ranges

## T-24h

- [ ] Pilot / `--resolve` tests passed (QA sign-off)
- [ ] Rollback NS values documented and accessible at registrar
- [ ] War room bridge scheduled; contacts confirmed
- [ ] Synthetic monitors baseline captured (pre-cutover)
- [ ] Status page draft prepared
- [ ] CAB approval recorded

## T-1h

- [ ] No other conflicting changes in same window
- [ ] On-call engineers at keyboard
- [ ] `dig` baseline saved from 3 public resolvers
- [ ] Communication sent: maintenance starting

## Cutover (execute in order)

- [ ] Update NS at registrar to Cloudflare nameservers
- [ ] Verify NS propagation (`dig NS @8.8.8.8`)
- [ ] HTTPS 200 on www and api
- [ ] HTTP → HTTPS redirect works
- [ ] Send test email; receive test email
- [ ] Origin metrics show Cloudflare source IPs
- [ ] WAF: managed rules **Log only** (no new block rules)
- [ ] HSTS **still off**
- [ ] HTTP/3 **still off**

## Abort criteria (stop and rollback)

- [ ] MX broken > 15 min
- [ ] Site 5xx > 10% sustained 10 min
- [ ] API auth completely failing
- [ ] Wrong NS entered at registrar

**Rollback owner decision:** _______________

## Sign-off

| Role | Name | Time (UTC) |
|------|------|------------|
| Cutover lead | | |
| DNS admin | | |
| App owner | | |
