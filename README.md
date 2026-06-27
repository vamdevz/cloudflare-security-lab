# Cloudflare Security Lab

Hands-on lab for Cloudflare security automation and production-style edge security engineering.

**📖 [Top 20 Advanced WAF Rules](docs/ADVANCED-WAF-RULES.md)** — expressions, API curl commands, validation tests, and operational notes.

**🏢 [Enterprise onboarding playbook (Contoso)](docs/enterprise-onboarding-contoso/README.md)** — phased migration, WAF rollout, HSTS/HTTP/3, governance, and checklists for production domains.

## Connect options

### Option A: MCP in Cursor (recommended for AI-assisted work)

1. Create an API token: [Cloudflare Dashboard → API Tokens](https://dash.cloudflare.com/profile/api-tokens)
   - Permissions: **Zone:Read**, **Zone:Edit**, **Account:Read** (for WAF/rulesets)
2. Edit `.cursor/mcp.json` — replace `YOUR_CLOUDFLARE_API_TOKEN`
3. Restart Cursor
4. Ask the agent: *"List my Cloudflare zones"* or *"Show WAF rules for my test domain"*

Official Cloudflare MCP: https://mcp.cloudflare.com/mcp (full API via Code Mode)

### Option B: Python scripts (this repo)

```powershell
cd cloudflare-security-lab
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your token and zone name
python scripts/list_zones.py
python scripts/zone_security_audit.py
```

## Lab use cases (build order)

| # | Use case | Script / Terraform | Engineering outcome |
|---|----------|-------------------|---------------------|
| 1 | Zone inventory | `scripts/list_zones.py` | "I automated zone discovery" |
| 2 | Security baseline audit | `scripts/zone_security_audit.py` | SSL, HTTPS, WAF gaps |
| 3 | WAF-as-code | `terraform/main.tf` | PR-based rule changes |
| 4 | Rate limit API paths | `terraform/main.tf` | Protect auth/API abuse |
| 5 | Drift detection | *coming next* | Dashboard vs code |
| 6 | Logpush → SIEM | *coming next* | Sentinel correlation |

## API token permissions

Minimum for this lab:

- Zone → Zone → Read
- Zone → Zone Settings → Read
- Zone → DNS → Read
- Zone → Firewall Services → Read (WAF rulesets)
- Zone → Firewall Services → Edit (if applying Terraform)

## Safety

- Use a **test domain** only
- Start WAF rules in **log** mode before **block**
- Never commit `.env` or tokens to GitHub

## Next steps

1. Add your API token to `.env`
2. Run `python scripts/list_zones.py`
3. Set `CLOUDFLARE_ZONE_NAME` and run the security audit
4. Push this repo to GitHub (private recommended)
