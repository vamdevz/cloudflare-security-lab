terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.0"
    }
  }
}

provider "cloudflare" {
  # Uses CLOUDFLARE_API_TOKEN env var
}

variable "zone_id" {
  description = "Cloudflare zone ID for your test domain"
  type        = string
}

# Use case 1: API path rate limit (log mode first — safe for lab)
resource "cloudflare_ruleset" "api_rate_limit_lab" {
  zone_id = var.zone_id
  name    = "lab-api-rate-limit"
  kind    = "zone"
  phase   = "http_ratelimit"

  rules = [{
    action      = "block"
    description = "Lab: rate limit sensitive API paths"
    expression  = "(http.request.uri.path contains \"/api/\")"
    enabled     = true
    ratelimit = {
      characteristics     = ["ip.src"]
      period              = 60
      requests_per_period = 100
      mitigation_timeout  = 600
    }
  }]
}

# Use case 2: Custom WAF rule in log mode (tune before blocking)
resource "cloudflare_ruleset" "waf_custom_lab" {
  zone_id = var.zone_id
  name    = "lab-waf-custom"
  kind    = "zone"
  phase   = "http_request_firewall_custom"

  rules = [{
    action      = "log"
    description = "Lab: log high threat score on API paths"
    expression  = "(http.request.uri.path contains \"/api/\" and cf.threat_score gt 10)"
    enabled     = true
  }]
}

output "rate_limit_ruleset_id" {
  value = cloudflare_ruleset.api_rate_limit_lab.id
}

output "custom_waf_ruleset_id" {
  value = cloudflare_ruleset.waf_custom_lab.id
}
