#!/bin/sh
# Build the public site locally.
set -eu
exec python3 "$(dirname "$0")/build.py" "${RODION_OUTPUT_DIR:-$(dirname "$0")/dist}"
