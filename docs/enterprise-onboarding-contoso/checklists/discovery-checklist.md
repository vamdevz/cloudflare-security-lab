# Discovery Checklist — Contoso

**Workshop date:** _______________  
**Facilitator:** _______________

## DNS & names

- [ ] Export full zone file (BIND / JSON)
- [ ] List all hostnames (internal + external)
- [ ] Document current NS and registrar access (2 custodians)
- [ ] Record TTL values for apex, www, api
- [ ] MX / SPF / DKIM / DMARC documented
- [ ] Identify wildcard and CNAME chains
- [ ] Split-horizon DNS documented (if any)

## Origins & network

- [ ] Origin IPs / FQDNs for each public hostname
- [ ] Firewall allows [Cloudflare IP ranges](https://www.cloudflare.com/ips/)
- [ ] Origin TLS certificate validity confirmed (hostname + chain)
- [ ] Port 80 behavior documented (redirect vs close)
- [ ] WebSockets / long polling in use?
- [ ] Max upload size requirements

## Applications

- [ ] Critical user journeys listed (login, checkout, API auth)
- [ ] Mobile apps and partner integrations identified
- [ ] Custom headers required (API keys, Host overrides)
- [ ] Webhook endpoints (inbound) listed
- [ ] Legacy paths (/admin, CMS) documented

## Security & compliance

- [ ] Data classification for public sites
- [ ] Log retention requirements (days)
- [ ] SIEM platform identified (Sentinel / Splunk)
- [ ] PCI / regulatory scope confirmed
- [ ] Pen test window constraints

## Cloudflare account

- [ ] Enterprise contract / account ID
- [ ] SSO (Entra ID) integration planned
- [ ] RBAC roles mapped to Contoso groups
- [ ] API token naming convention agreed

## Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| DNS admin | | | |
| Security architect | | | |
| App owner | | | |
| Program manager | | | |
