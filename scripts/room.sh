#!/usr/bin/env bash
# Open or close the live room on the deployed server.
#
#   ./scripts/room.sh on       before judging, or before testing
#   ./scripts/room.sh off      afterwards
#   ./scripts/room.sh status
#
# The room is the only public route that spends ElevenLabs and model credits per
# interaction. Closing it leaves /try and the twelve prepared cases untouched —
# the page just explains that the room is switched off and points at them.
set -euo pipefail

HOST="${DEPLOY_HOST:-aliyun}"
DIR="${DEPLOY_DIR:-/opt/complaintguard}"
WANT="${1:-status}"

case "$WANT" in
  on|off)
    ssh "$HOST" "sed -i '/^LIVE_ROOM=/d' ${DIR}/.env && echo 'LIVE_ROOM=${WANT}' >> ${DIR}/.env \
                 && cd ${DIR} && docker compose up -d --force-recreate app >/dev/null 2>&1"
    echo "==> live room is now ${WANT}"
    ;;
  status)
    ssh "$HOST" "grep '^LIVE_ROOM=' ${DIR}/.env || echo 'LIVE_ROOM=on (default)'"
    ;;
  *)
    echo "usage: $0 [on|off|status]" >&2
    exit 2
    ;;
esac
