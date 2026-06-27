# War Room Comms Templates

## Cutover started

```
[02:00 UTC] Security (@[You]): Pre-flight complete — WAF block OFF, HSTS OFF, SSL Full strict.
DNS team cleared to proceed with NS update when ready.
```

## SSL 526 incident

```
[02:18 UTC] Security: Seeing 526 — origin cert validation failure, NOT WAF.
Action: Platform verify AGW cert for www.contoso.com + chain.
WAF unchanged. NS rollback decision at T+60 if unresolved.
```

## Reject WAF block on cutover night

```
[02:25 UTC] Security: Request to enable OWASP block denied — out of scope for CHG-00230.
Managed log enablement scheduled CHG-00235 Monday 09:00.
```

## Post-cutover all green

```
[04:30 UTC] Security: 1.2M req, 0 WAF blocks. 23 managed LOG events (scanners).
Email MX verified. Handing to hypercare — security green.
```

## Emergency WAF skip (partner)

```
[10:45 UTC] Security: Emergency skip applied Fabrikam IP 203.0.113.50 POST /api/v1/orders only.
Retro CAB CHG-00266 today. Global WAF remains enabled.
Ray ID: 924abc123def4567
```

## Enforce go-live

```
[06:15 UTC] Security: CHG-00241 complete — managed rules BLOCK.
Attack samples 403, health 200, partner orders 200. Monitoring 24h.
```
