#!/bin/bash
set -e

# Only run the bootstrap script if we are starting the main web server (uvicorn)
# This prevents race conditions when the worker container starts concurrently
if [[ "$1" == "uvicorn" ]]; then
    python backend/scripts/bootstrap_admin.py
fi

# Execute the main container command
exec "$@"
