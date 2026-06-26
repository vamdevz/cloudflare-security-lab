# Publish to GitHub

Local git is initialized and committed. Complete **one-time** GitHub login, then run the script below.

## Option A — GitHub CLI (recommended)

### Step 1: Login (once)

```powershell
gh auth login
```

Choose:
- **GitHub.com**
- **HTTPS**
- **Login with a web browser** (or paste a token)

### Step 2: Create repo and push

```powershell
cd "C:\Users\Mr. Dev Mishra\Documents\Projects\cloudflare-security-lab"
.\scripts\publish-github.ps1
```

Or manually:

```powershell
gh repo create cloudflare-security-lab --public --source=. --remote=origin --push `
  --description "Cloudflare WAF security lab - advanced rules, Python automation, and edge security patterns"
```

---

## Option B — Manual (no gh)

1. Go to https://github.com/new
2. Repository name: `cloudflare-security-lab`
3. **Do not** add README, .gitignore, or license (already in local repo)
4. Create repository, then:

```powershell
cd "C:\Users\Mr. Dev Mishra\Documents\Projects\cloudflare-security-lab"
git remote add origin https://github.com/YOUR_USERNAME/cloudflare-security-lab.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub handle.

---

## What is NOT pushed (secrets)

| File | Reason |
|------|--------|
| `.env` | API tokens |
| `.cursor/mcp.json` | API tokens |
| `.venv/` | local Python env |

Use `.env.example` and `.cursor/mcp.json.example` after clone.

---

## After publish

Your repo will include:
- `docs/ADVANCED-WAF-RULES.md` — top 20 rules guide
- `scripts/` — deploy and audit automation
- `terraform/` — WAF-as-code starters
- `src/cf_client.py` — Cloudflare API helper
