# ============================================
# Klinik Management System - Production Checklist
# ============================================
# Use this checklist to ensure everything is
# ready for production deployment
# ============================================

## Pre-Deployment Checklist

### 1. Code Review
- [ ] All features tested and working
- [ ] No TODO comments in production code
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Performance optimized

### 2. Security
- [ ] DEBUG=False
- [ ] SECRET_KEY changed (not default)
- [ ] ALLOWED_HOSTS set to actual domain
- [ ] Database password changed
- [ ] SSL certificate installed
- [ ] Firewall configured (UFW)
- [ ] Regular backups scheduled
- [ ] Security headers configured

### 3. Database
- [ ] PostgreSQL configured for production
- [ ] Database backup strategy in place
- [ ] Database user has minimal privileges
- [ ] Database connection pooling configured

### 4. Application
- [ ] All migrations applied
- [ ] Static files collected
- [ ] Environment variables configured
- [ ] Gunicorn workers configured
- [ ] Nginx reverse proxy configured

### 5. Monitoring
- [ ] Error logging configured
- [ ] Health check script ready
- [ ] Backup script configured
- [ ] Monitoring alerts set up

### 6. Testing
- [ ] All tests passing
- [ ] Manual testing completed
- [ ] Load testing completed (if applicable)
- [ ] Security scanning completed

### 7. Documentation
- [ ] README updated
- [ ] Installation guide updated
- [ ] Deployment guide updated
- [ ] API documentation updated
- [ ] Architecture documentation updated

### 8. Deployment
- [ ] Domain pointed to server
- [ ] DNS records configured
- [ ] SSL certificate installed
- [ ] Nginx configuration tested
- [ ] Gunicorn service running
- [ ] Database connection working

### 9. Post-Deployment
- [ ] Smoke test passed
- [ ] User acceptance testing completed
- [ ] Performance monitoring active
- [ ] Error monitoring active
- [ ] Backup verification completed

### 10. Emergency Procedures
- [ ] Rollback plan documented
- [ ] Emergency contact information available
- [ ] Incident response procedure documented
- [ ] Recovery procedures tested

## Post-Deployment Verification

### Quick Verification Steps
```bash
# 1. Check services
sudo systemctl status klinik
sudo systemctl status nginx
sudo systemctl status postgresql

# 2. Test application
curl -I https://your-domain.com

# 3. Check logs
sudo journalctl -u klinik -f
sudo tail -f /var/log/nginx/error.log

# 4. Run health check
bash health_check.sh

# 5. Test backup
bash backup.sh
```

### Performance Verification
- [ ] Page load time < 2 seconds
- [ ] API response time < 500ms
- [ ] Database query time < 100ms
- [ ] Memory usage < 500MB
- [ ] CPU usage < 70%

### Security Verification
- [ ] SSL certificate valid
- [ ] Security headers present
- [ ] No sensitive data in logs
- [ ] File permissions correct
- [ ] Firewall rules active

## Rollback Procedure

If deployment fails:

```bash
# 1. Stop services
sudo systemctl stop klinik
sudo systemctl stop nginx

# 2. Restore database
sudo -u postgres psql klinik_db < /var/backups/klinik/klinik_backup_YYYYMMDD_HHMMSS_database.sql

# 3. Restore files
tar -xzf /var/backups/klinik/klinik_backup_YYYYMMDD_HHMMSS_files.tar.gz -C /var/www/klinik

# 4. Restart services
sudo systemctl start nginx
sudo systemctl start klinik
```

## Contact Information

- **System Administrator**: admin@klinik.com
- **Emergency Contact**: +62-xxx-xxxx-xxxx
- **Support Team**: support@klinik.com
