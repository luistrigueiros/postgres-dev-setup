#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: ./scripts/restore.sh <backup_file>"
    exit 1
fi

docker exec -i dev-postgres psql -U devuser devdb < "$1"
echo "✓ Restored from $1"