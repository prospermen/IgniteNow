#!/bin/bash
set -e

# Run the bootstrap script to ensure the database and admin user are initialized
python backend/scripts/bootstrap_admin.py

# Execute the main container command (e.g., uvicorn or rq worker)
exec "$@"
