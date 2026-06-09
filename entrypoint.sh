#!/bin/bash

set -e

# Run migrations
echo "Running database migrations..."
uv run alembic upgrade head

# Execute the main container command (FastAPI)
echo "Starting FastAPI application..."
exec "$@"
