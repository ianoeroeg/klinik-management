#!/bin/bash
# ============================================
# Backup Script - Klinik Management System
# ============================================
# Run: bash backup.sh
# ============================================

set -e

BACKUP_DIR="/var/backups/klinik"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="klinik_backup_${TIMESTAMP}"

echo "Starting backup..."

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
echo "Backing up database..."
sudo -u postgres pg_dump klinik_db > $BACKUP_DIR/${BACKUP_NAME}_database.sql

# Backup files
echo "Backing up files..."
tar -czf $BACKUP_DIR/${BACKUP_NAME}_files.tar.gz \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    -C /var/www/klinik \
    .

# Backup environment
echo "Backing up environment..."
cp /var/www/klinik/.env $BACKUP_DIR/${BACKUP_NAME}_env 2>/dev/null || true

# Show backup info
echo ""
echo "Backup completed successfully!"
echo "Backup files:"
ls -lh $BACKUP_DIR/${BACKUP_NAME}*

echo ""
echo "To restore:"
echo "  Database: sudo -u postgres psql klinik_db < $BACKUP_DIR/${BACKUP_NAME}_database.sql"
echo "  Files: tar -xzf $BACKUP_DIR/${BACKUP_NAME}_files.tar.gz -C /var/www/klinik"
