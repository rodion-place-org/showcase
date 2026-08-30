#!/bin/sh
# LAN preview (Caddy serves /srv/rodion/public/site at http://10.10.5.15/site/). Public build for rodion.place: ./deploy.sh
set -eu
exec python3 "$(dirname "$0")/build.py" /srv/rodion/public/site --base /site
