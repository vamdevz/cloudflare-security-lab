# Post-Cutover Checklist — Contoso

**Cutover date:** _______________  
**Hypercare ends:** _______________

## D+0 (within 4 hours)

- [ ] Global DNS propagation confirmed (multiple regions)
- [ ] All P1 user journeys tested (www + api)
- [ ] No elevated 525/526/522 errors
- [ ] Email send/receive verified
- [ ] Security Events receiving traffic
- [ ] Change ticket updated: success / issues

## D+1

- [ ] Compare origin 5xx to pre-cutover baseline
- [ ] Review Security Events top rules (log mode)
- [ ] Support desk ticket volume normal
- [ ] Cache hit ratio reasonable for static assets
- [ ] Logpush job configured (or scheduled)

## D+2 to D+5

- [ ] App regression suite complete
- [ ] Performance p95 within acceptable delta
- [ ] False positive triage process started
- [ ] Hypercare daily summary sent to SteerCo
- [ ] TTL restored to standard values (optional)

## Handoff to observation phase

- [ ] Observation phase owner assigned
- [ ] Weekly WAF tuning meetings scheduled (4 weeks)
- [ ] Tuning log document created
- [ ] Terraform repo access granted to platform team
- [ ] Close cutover change ticket

## Sign-off (end hypercare)

| Role | Name | Date |
|------|------|------|
| Engagement lead | | |
| Contoso IT lead | | |
| Security architect | | |
