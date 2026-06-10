#!/bin/bash
set -e

DB_TO_CREATE=${DB_NAME:-memoryfm}

echo "Creating database $DB_TO_CREATE";

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$DB_TO_CREATE";
    GRANT ALL PRIVILEGES ON DATABASE "$DB_TO_CREATE" TO "$POSTGRES_USER";
EOSQL
