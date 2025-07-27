# Deployment Guide

This guide covers various deployment options for ShrinkItPy, from development to production environments.

## 📋 Prerequisites

### System Requirements
- **CPU**: 1 vCPU minimum, 2+ recommended for production
- **RAM**: 512MB minimum, 1GB+ recommended for production  
- **Storage**: 10GB minimum for database and application
- **Network**: Inbound access on port 5000 (or your chosen port)

### Software Requirements
- **Docker** 20.10+ and **Docker Compose** 2.0+ (recommended)
- **PostgreSQL** 12+ (if not using Docker)
- **Python** 3.12+ (if running locally)

---

## 🚀 Quick Deployment Options

### Option 1: Docker Compose (Recommended)

This is the fastest way to get ShrinkItPy running with all dependencies.

```bash
# Clone the repository
git clone https://github.com/ivansmarbun/shrinkitpy.git
cd shrinkitpy

# Start the application with PostgreSQL
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app
```

**Access**: http://localhost:5000

**What this does**:
- Starts PostgreSQL database container
- Runs database migrations automatically
- Starts the Flask application
- Sets up networking between containers

### Option 2: Docker Hub Image

Use the pre-built image from Docker Hub:

```bash
# Pull and run with external PostgreSQL
docker run -d \
  --name shrinkitpy \
  -p 5000:5000 \
  -e DATABASE_URL="postgresql://user:password@host:5432/database" \
  -e FLASK_ENV="production" \
  ivansmarbun/shrinkitpy:latest
```

---

## 🏭 Production Deployment

### Environment Configuration

Create a production environment file:

```bash
# .env.production
DATABASE_URL=postgresql://username:password@hostname:5432/shrinkitpy_prod
FLASK_ENV=production
SECRET_KEY=your-super-secret-production-key-here
```

### Docker Compose Production Setup

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: shrinkitpy_prod
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
    networks:
      - shrinkitpy_network
    restart: unless-stopped

  app:
    image: ivansmarbun/shrinkitpy:latest
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/shrinkitpy_prod
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    networks:
      - shrinkitpy_network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    networks:
      - shrinkitpy_network
    restart: unless-stopped

volumes:
  postgres_prod_data:

networks:
  shrinkitpy_network:
    driver: bridge
```

### Nginx Configuration

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:5000;
    }

    server {
        listen 80;
        server_name your-domain.com;
        
        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Deploy to Production

```bash
# Set environment variables
export DB_USER=shrinkitpy_user
export DB_PASSWORD=secure_password_here
export SECRET_KEY=your-production-secret-key

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Verify deployment
docker-compose -f docker-compose.prod.yml ps
curl -I https://your-domain.com
```

---

## ☁️ Cloud Platform Deployments

### AWS Deployment

#### Using AWS ECS (Elastic Container Service)

1. **Create ECS Cluster**:
```bash
aws ecs create-cluster --cluster-name shrinkitpy-cluster
```

2. **Set up RDS PostgreSQL**:
```bash
aws rds create-db-instance \
  --db-instance-identifier shrinkitpy-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YourSecurePassword \
  --allocated-storage 20
```

3. **Create Task Definition** (`task-definition.json`):
```json
{
  "family": "shrinkitpy",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::YOUR_ACCOUNT:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "shrinkitpy",
      "image": "ivansmarbun/shrinkitpy:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://admin:password@your-rds-endpoint:5432/postgres"
        },
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/shrinkitpy",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

4. **Deploy Service**:
```bash
aws ecs create-service \
  --cluster shrinkitpy-cluster \
  --service-name shrinkitpy-service \
  --task-definition shrinkitpy \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
```

### Google Cloud Platform (GCP)

#### Using Cloud Run

1. **Build and Push Image**:
```bash
# Configure gcloud
gcloud auth configure-docker

# Build and push
docker build -t gcr.io/YOUR_PROJECT_ID/shrinkitpy .
docker push gcr.io/YOUR_PROJECT_ID/shrinkitpy
```

2. **Deploy to Cloud Run**:
```bash
gcloud run deploy shrinkitpy \
  --image gcr.io/YOUR_PROJECT_ID/shrinkitpy \
  --platform managed \
  --region us-central1 \
  --set-env-vars DATABASE_URL="postgresql://user:pass@host/db" \
  --set-env-vars FLASK_ENV="production" \
  --allow-unauthenticated
```

### DigitalOcean App Platform

Create `app.yaml`:
```yaml
name: shrinkitpy
services:
- name: web
  source_dir: /
  github:
    repo: ivansmarbun/shrinkitpy
    branch: master
  run_command: python app.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: DATABASE_URL
    value: ${db.DATABASE_URL}
  - key: FLASK_ENV
    value: production
  http_port: 5000
databases:
- name: db
  engine: PG
  num_nodes: 1
  size: db-s-dev-database
```

Deploy:
```bash
doctl apps create --spec app.yaml
```

---

## 🔒 Security Hardening

### Environment Variables
Never commit sensitive data to version control:

```bash
# Use a secrets management system
# AWS Secrets Manager, HashiCorp Vault, etc.

# For Docker Compose, use an env file
echo "DATABASE_URL=postgresql://..." > .env.production
echo ".env.production" >> .gitignore
```

### Database Security
```bash
# Create dedicated database user
psql -c "CREATE USER shrinkitpy_app WITH PASSWORD 'secure_password';"
psql -c "GRANT CONNECT ON DATABASE shrinkitpy_prod TO shrinkitpy_app;"
psql -c "GRANT USAGE ON SCHEMA public TO shrinkitpy_app;"
psql -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO shrinkitpy_app;"
```

### Nginx Security Headers
```nginx
# Add to nginx.conf server block
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
```

### SSL/TLS Certificate
```bash
# Using Let's Encrypt with Certbot
certbot --nginx -d your-domain.com

# Or use CloudFlare, AWS Certificate Manager, etc.
```

---

## 📊 Monitoring and Logging

### Health Check Endpoint
Add to your Flask app:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

### Docker Health Check
```dockerfile
# Add to Dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1
```

### Logging Configuration
```python
# Add to app.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/shrinkitpy.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

---

## 🔄 Database Backup and Recovery

### Automated Backups
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="shrinkitpy_backup_$DATE.sql"

pg_dump $DATABASE_URL > /backups/$BACKUP_FILE
gzip /backups/$BACKUP_FILE

# Upload to S3, Google Cloud Storage, etc.
aws s3 cp /backups/$BACKUP_FILE.gz s3://your-backup-bucket/
```

### Cron Job for Regular Backups
```bash
# Add to crontab
0 2 * * * /path/to/backup.sh
```

### Recovery Process
```bash
# Restore from backup
gunzip shrinkitpy_backup_20250727_020000.sql.gz
psql $DATABASE_URL < shrinkitpy_backup_20250727_020000.sql
```

---

## 🚨 Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Verify credentials
psql "postgresql://user:password@host:5432/database" -c "SELECT 1;"

# Check Docker network
docker network ls
docker network inspect shrinkitpy_default
```

#### Migration Failures
```bash
# Check migration status
python migrate.py status

# Manually fix database state
psql $DATABASE_URL -c "DELETE FROM schema_migrations WHERE version = 'problematic_version';"

# Retry migration
python migrate.py migrate
```

#### Performance Issues
```bash
# Check container resources
docker stats

# Monitor database connections
psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity;"

# Check slow queries
psql $DATABASE_URL -c "SELECT query, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 5;"
```

---

## 📈 Scaling Considerations

### Horizontal Scaling
- Use multiple app instances behind a load balancer
- Implement Redis for session storage (if sessions are added)
- Use CDN for static assets

### Database Scaling
- Implement read replicas for analytics queries
- Consider connection pooling (PgBouncer)
- Database partitioning for large datasets

### Caching Strategy
- Implement Redis for URL caching
- Use HTTP caching headers
- CDN for geographic distribution

---

## 🔧 Maintenance

### Regular Tasks
- **Weekly**: Review application logs for errors
- **Monthly**: Update dependencies and security patches  
- **Quarterly**: Review and test backup/recovery procedures
- **Yearly**: Security audit and penetration testing

### Update Process
```bash
# Pull latest changes
git pull origin master

# Rebuild and deploy
docker-compose down
docker-compose pull
docker-compose up -d

# Verify deployment
curl -I http://your-domain.com/health
```

---

This deployment guide provides comprehensive coverage from local development to enterprise production deployments. Choose the approach that best fits your infrastructure and requirements.
