#!/usr/bin/env bash
# Deploy to the Aliyun box. Run from the repo root on your own machine.
#
# Prerequisites, once:
#   1. Aliyun security group: allow inbound 80/TCP and 443/TCP
#   2. DuckDNS subdomain pointing at the server's public IP
#   3. SITE_DOMAIN set below (or exported)
#
# Everything else is idempotent — safe to re-run.
set -euo pipefail

HOST="${DEPLOY_HOST:-aliyun}"
DIR="${DEPLOY_DIR:-/opt/complaintguard}"
DOMAIN="${SITE_DOMAIN:?set SITE_DOMAIN, e.g. export SITE_DOMAIN=complaintguard.duckdns.org}"

echo "==> deploying to ${HOST}:${DIR} for ${DOMAIN}"

ssh "$HOST" "mkdir -p ${DIR}"

# Ship the repo without .git, .venv or secrets.
rsync -az --delete \
  --exclude '.git' --exclude '.venv' --exclude '.env' --exclude '__pycache__' \
  ./ "${HOST}:${DIR}/"

# .env is never in the repo — it lives on the server only.
ssh "$HOST" "test -f ${DIR}/.env || cp ${DIR}/.env.example ${DIR}/.env"

# Set SITE_DOMAIN, replacing any existing line. .env.example ships an empty
# SITE_DOMAIN=, so "append if absent" silently leaves it empty — and an empty
# value makes the Caddyfile's site address collapse to a bare "{", which Caddy
# reads as the global options block and refuses to start.
ssh "$HOST" "sed -i '/^SITE_DOMAIN=/d' ${DIR}/.env && echo 'SITE_DOMAIN=${DOMAIN}' >> ${DIR}/.env"
ssh "$HOST" "grep '^SITE_DOMAIN=' ${DIR}/.env"

ssh "$HOST" "cd ${DIR} && SITE_DOMAIN=${DOMAIN} docker compose up -d --build"

echo "==> waiting for health"
for i in $(seq 1 30); do
  if curl -fsS --max-time 5 "https://${DOMAIN}/health" >/dev/null 2>&1; then
    echo "==> live: https://${DOMAIN}"
    curl -s "https://${DOMAIN}/health"; echo
    exit 0
  fi
  sleep 4
done

echo "!! health check did not pass in 2 minutes. Check:"
echo "   ssh ${HOST} 'cd ${DIR} && docker compose logs --tail 60'"
exit 1
