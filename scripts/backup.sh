#!/bin/bash
BACKUP_DIR="backups"
mkdir -p "$BACKUP_DIR"
BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"

docker exec dev-postgres pg_dump -U devuser devdb > "$BACKUP_FILE"
echo "✓ Backup saved to $BACKUP_FILE"