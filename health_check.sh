#!/bin/bash
# ============================================
# Health Check Script - Klinik Management System
# ============================================
# Run: bash health_check.sh
# ============================================

echo "============================================"
echo "Klinik Management System - Health Check"
echo "============================================"
echo ""

# Check Gunicorn
echo -e "\033[1;33m1. Checking Gunicorn service...\033[0m"
if systemctl is-active --quiet klinik; then
    echo -e "\033[32m✓ Gunicorn is running\033[0m"
else
    echo -e "\033[31m✗ Gunicorn is NOT running\033[0m"
    echo "Run: sudo systemctl start klinik"
fi

# Check Nginx
echo -e "\033[1;33m2. Checking Nginx service...\033[0m"
if systemctl is-active --quiet nginx; then
    echo -e "\033[32m✓ Nginx is running\033[0m"
else
    echo -e "\033[31m✗ Nginx is NOT running\033[0m"
    echo "Run: sudo systemctl start nginx"
fi

# Check PostgreSQL
echo -e "\033[1;33m3. Checking PostgreSQL...\033[0m"
if systemctl is-active --quiet postgresql; then
    echo -e "\033[32m✓ PostgreSQL is running\033[0m"
else
    echo -e "\033[31m✗ PostgreSQL is NOT running\033[0m"
    echo "Run: sudo systemctl start postgresql"
fi

# Check database connection
echo -e "\033[1;33m4. Testing database connection...\033[0m"
cd /var/www/klinik
source venv/bin/activate
python manage.py check --deploy 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "\033[32m✓ Database connection OK\033[0m"
else
    echo -e "\033[31m✗ Database connection FAILED\033[0m"
fi

# Check static files
echo -e "\033[1;33m5. Checking static files...\033[0m"
if [ -d "staticfiles" ]; then
    STATIC_COUNT=$(find staticfiles -type f | wc -l)
    echo -e "\033[32m✓ Static files OK (${STATIC_COUNT} files)\033[0m"
else
    echo -e "\033[31m✗ Static files NOT FOUND\033[0m"
    echo "Run: python manage.py collectstatic --noinput"
fi

# Check disk space
echo -e "\033[1;33m6. Checking disk space...\033[0m"
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}')
echo "Disk usage: $DISK_USAGE"
if [ "${DISK_USAGE%\%}" -gt 90 ]; then
    echo -e "\033[31m⚠ Disk space is critically low!\033[0m"
else
    echo -e "\033[32m✓ Disk space OK\033[0m"
fi

# Check memory
echo -e "\033[1;33m7. Checking memory usage...\033[0m"
free -h | grep Mem

# Check recent errors
echo -e "\033[1;33m8. Checking recent errors...\033[0m"
ERROR_COUNT=$(sudo journalctl -u klinik --since "1 hour ago" | grep -c "ERROR" || echo "0")
echo "Errors in last hour: $ERROR_COUNT"
if [ "$ERROR_COUNT" -gt 10 ]; then
    echo -e "\033[31m⚠ High error count detected!\033[0m"
fi

echo ""
echo "============================================"
echo "Health check completed!"
echo "============================================"
