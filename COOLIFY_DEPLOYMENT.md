# Coolify Deployment Guide

Complete guide to deploying the Social Image Generator on Coolify - the self-hosted PaaS alternative to Heroku, Netlify, and Vercel.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Deployment](#quick-deployment)
- [Step-by-Step Setup](#step-by-step-setup)
- [Environment Configuration](#environment-configuration)
- [Persistent Storage](#persistent-storage)
- [Domain & SSL Setup](#domain--ssl-setup)
- [Monitoring & Health Checks](#monitoring--health-checks)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)
- [Production Best Practices](#production-best-practices)

---

## Prerequisites

Before deploying to Coolify, ensure you have:

- ✅ **Coolify Instance**: A running Coolify server (v4.0 or later recommended)
- ✅ **Git Repository**: Your code in a Git repository (GitHub, GitLab, Bitbucket, or self-hosted)
- ✅ **Server Resources**: Minimum 2GB RAM, 2 vCPU recommended for production
- ✅ **Domain** (optional): For SSL and custom domain access

---

## Quick Deployment

### 1. Create New Resource

In Coolify dashboard:

1. Click **"+ New"** → **"Resource"**
2. Select **"Application"**
3. Choose your Git source (GitHub, GitLab, etc.)

### 2. Configure Application

**Basic Settings:**
```
Name: social-image-generator
Project: (choose or create project)
Environment: production
```

**Build Configuration:**
```
Build Pack: Dockerfile
Dockerfile Location: ./Dockerfile
Base Directory: ./
Port: 5000
```

### 3. Deploy

Click **"Save & Deploy"** - Coolify will automatically:
- Clone your repository
- Build the Docker image
- Start the container
- Configure health checks
- Set up automatic restarts

That's it! Your API will be available at the Coolify-provided URL.

---

## Step-by-Step Setup

### Step 1: Create Application in Coolify

1. **Login to Coolify Dashboard**
   ```
   https://your-coolify-instance.com
   ```

2. **Add New Application**
   - Navigate to your project or create a new one
   - Click **"+ New Resource"** → **"Application"**

3. **Connect Git Repository**
   - Select your Git provider (GitHub, GitLab, etc.)
   - Authorize Coolify to access your repositories
   - Select the `social-image-generator` repository
   - Choose the branch to deploy (e.g., `main` or `production`)

### Step 2: Configure Build Settings

In the **Build** section:

```yaml
Build Pack: Dockerfile
Dockerfile Location: ./Dockerfile
Docker Compose Location: (leave empty - not using compose)
Base Directory: ./
Port Exposes: 5000
Port Mappings: 5000:5000
```

**Important:** Coolify will automatically detect the `EXPOSE` directive in the Dockerfile.

### Step 3: Environment Variables

Navigate to **"Environment Variables"** tab and add:

**Required Variables:**
```bash
PORT=5000
FLASK_ENV=production
PYTHONPATH=/app/src
PYTHONDONTWRITEBYTECODE=1
```

**Optional Variables:**
```bash
# Logging
LOG_LEVEL=INFO

# Performance
WEB_CONCURRENCY=4
```

> **Note:** You can copy all variables from `.env.coolify` file in the repository.

### Step 4: Configure Persistent Storage

This is **CRITICAL** for the application to work properly!

Navigate to **"Storages"** or **"Persistent Storage"** tab:

#### Add Storage Volumes:

**Volume 1: Uploads**
```
Source: /var/lib/coolify/applications/{app-id}/uploads
Destination: /app/uploads
```

**Volume 2: Output**
```
Source: /var/lib/coolify/applications/{app-id}/output
Destination: /app/output
```

**Volume 3: Generated**
```
Source: /var/lib/coolify/applications/{app-id}/generated
Destination: /app/generated
```

> **Tip:** Coolify will create these directories automatically on the host server.

### Step 5: Health Check Configuration

Coolify automatically uses the `HEALTHCHECK` directive from the Dockerfile:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health').read()" || exit 1
```

**Manual Override** (if needed):
```
Health Check Path: /health
Health Check Port: 5000
Health Check Method: GET
```

The `/health` endpoint returns comprehensive system status:
```json
{
  "status": "healthy",
  "timestamp": "2024-10-24T10:00:00",
  "version": "2.0",
  "system": {
    "python_version": "3.11.x",
    "upload_ready": true,
    "generation_ready": true
  }
}
```

### Step 6: Deploy the Application

1. Click **"Deploy"** or **"Save & Deploy"**
2. Monitor the build logs in real-time
3. Wait for deployment to complete (typically 2-5 minutes)

### Step 7: Verify Deployment

Once deployed, test the API:

```bash
# Replace with your Coolify URL
COOLIFY_URL="https://your-app.coolify.app"

# Check health
curl $COOLIFY_URL/health

# Expected response: {"status": "healthy", ...}
```

---

## Environment Configuration

### Complete Environment Variables List

Copy these to your Coolify **Environment Variables** section:

```bash
# Application Core
PORT=5000
FLASK_ENV=production
PYTHONPATH=/app/src
PYTHONDONTWRITEBYTECODE=1

# Optional: Performance
WEB_CONCURRENCY=4
WORKER_TIMEOUT=120

# Optional: Logging
LOG_LEVEL=INFO

# Optional: Upload Limits
MAX_CONTENT_LENGTH=104857600  # 100MB
```

### Managing Sensitive Data

For API keys or secrets:

1. Add them in Coolify's Environment Variables UI
2. Mark them as **"Secret"** (Coolify will encrypt them)
3. Never commit secrets to your repository

---

## Persistent Storage

### Why Persistent Storage?

Docker containers are **ephemeral** - data is lost when containers restart. Persistent storage ensures:
- ✅ Uploaded images persist across deployments
- ✅ Generated images are retained
- ✅ Configuration files survive restarts

### Required Volumes

| Container Path | Purpose | Required | Size Estimate |
|---------------|---------|----------|---------------|
| `/app/uploads` | User-uploaded images | Yes | 5-20GB |
| `/app/output` | Generated output images | Yes | 5-20GB |
| `/app/generated` | API-generated images | Yes | 5-20GB |

### Storage Configuration in Coolify

#### Option 1: Coolify UI (Recommended)

1. Go to **"Storages"** tab
2. Click **"Add Volume"**
3. Fill in details:
   ```
   Name: uploads
   Source: /var/lib/coolify/applications/{app-id}/uploads
   Destination: /app/uploads
   ```
4. Repeat for `output` and `generated`

#### Option 2: Advanced (Custom Host Paths)

If you want to use custom host paths:

```
Source: /mnt/storage/social-gen/uploads
Destination: /app/uploads
```

### Backup Strategies

**Automated Backups:**

```bash
# Coolify server - run via cron
#!/bin/bash
APP_ID="your-app-id"
BACKUP_DIR="/backups/social-image-gen"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

tar -czf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" \
    "/var/lib/coolify/applications/$APP_ID/uploads" \
    "/var/lib/coolify/applications/$APP_ID/output" \
    "/var/lib/coolify/applications/$APP_ID/generated"

# Keep only last 7 days
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete
```

---

## Domain & SSL Setup

### Using Coolify's Built-in Domain

Coolify automatically provides a domain:
```
https://{app-name}.{coolify-domain}
```

### Custom Domain Setup

1. **Add Custom Domain in Coolify:**
   - Go to **"Domains"** tab
   - Click **"Add Domain"**
   - Enter your domain: `api.yourdomain.com`

2. **Configure DNS:**

   Add A record pointing to your Coolify server:
   ```
   Type: A
   Name: api
   Value: <your-coolify-server-ip>
   TTL: 3600
   ```

3. **Enable SSL (Let's Encrypt):**

   Coolify automatically provisions SSL certificates!
   - Check **"Enable SSL"**
   - Select **"Let's Encrypt"**
   - Wait 1-2 minutes for certificate provisioning

4. **Force HTTPS:**
   - Enable **"Force HTTPS"** option
   - All HTTP requests will redirect to HTTPS

### Multiple Domains

You can add multiple domains:
```
- api.yourdomain.com (primary)
- social-gen.yourdomain.com (alias)
```

---

## Monitoring & Health Checks

### Built-in Health Monitoring

Coolify monitors your application using:

1. **HTTP Health Checks:** `GET /health`
2. **Container Status:** Docker container health
3. **Resource Usage:** CPU, Memory, Disk

### Health Check Endpoint

The application provides a comprehensive health check:

**Request:**
```bash
curl https://your-app.coolify.app/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-10-24T10:00:00.000000",
  "version": "2.0",
  "system": {
    "python_version": "3.11.x",
    "platform": "linux",
    "upload_ready": true,
    "generation_ready": true,
    "upload_limit_mb": 100
  },
  "disk": {
    "free_gb": 45.2,
    "total_gb": 100.0,
    "used_gb": 54.8,
    "usage_percent": 54.8
  },
  "endpoints": {
    "upload": "/upload/{main|watermark|background}",
    "generate": "/generate",
    "health": "/health"
  }
}
```

### Monitoring Dashboard

Access Coolify's monitoring:

1. Go to your application dashboard
2. View **"Logs"** tab for real-time logs
3. View **"Metrics"** for resource usage
4. Set up **"Notifications"** for alerts

### Alerts & Notifications

Configure alerts in Coolify:

1. **Go to Settings → Notifications**
2. **Add notification channel:**
   - Email
   - Slack
   - Discord
   - Telegram
   - Webhook

3. **Configure alert rules:**
   - Health check failures
   - High CPU/Memory usage
   - Container restarts

---

## Performance Optimization

### Resource Limits

In Coolify, configure resource limits:

**Recommended for Production:**
```yaml
CPU Limit: 2 cores
Memory Limit: 2048 MB
Memory Reservation: 512 MB
```

**For High Traffic:**
```yaml
CPU Limit: 4 cores
Memory Limit: 4096 MB
Memory Reservation: 1024 MB
```

### Scaling Options

#### Vertical Scaling (Single Instance)

Increase resources in Coolify:
- Go to **"Resources"** tab
- Adjust **CPU** and **Memory** sliders
- Save and redeploy

#### Horizontal Scaling (Multiple Instances)

For high availability:

1. Use Coolify's **Load Balancer** feature
2. Deploy multiple instances
3. Configure round-robin or least-connections

### Build Optimization

**Enable Build Cache:**
```bash
# In Coolify Build settings
Enable Build Cache: Yes
```

**Multi-stage Builds** (already optimized in Dockerfile):
- Reduces final image size
- Faster deployments
- Less storage usage

### Runtime Optimization

**Use Gunicorn** (recommended for production):

Update `CMD` in Dockerfile:
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "--timeout", "120", "social_image_api:app"]
```

Add to `requirements.txt`:
```
gunicorn>=21.0.0
```

---

## Troubleshooting

### Common Issues & Solutions

#### 1. Build Fails

**Symptom:** Build process fails in Coolify

**Solutions:**
```bash
# Check build logs in Coolify dashboard
# Look for:
- Missing dependencies
- Network issues during pip install
- Insufficient disk space

# Common fixes:
- Clear build cache
- Rebuild from scratch
- Check Dockerfile syntax
```

#### 2. Container Won't Start

**Symptom:** Container starts but immediately stops

**Solutions:**
```bash
# Check container logs in Coolify
# Common causes:
1. Port already in use
2. Missing environment variables
3. Permission issues with volumes

# Verify:
- PORT environment variable is set
- Volumes are properly mounted
- Health check endpoint is accessible
```

#### 3. Health Check Failing

**Symptom:** Coolify shows application as unhealthy

**Solutions:**
```bash
# Test health endpoint manually:
curl http://localhost:5000/health

# Check:
1. Flask app is running
2. Port 5000 is accessible
3. Dependencies are installed
4. Volumes have correct permissions

# Review health check logs:
docker logs <container-id> | grep health
```

#### 4. Upload/Generation Fails

**Symptom:** API accepts uploads but fails to save/generate

**Solutions:**
```bash
# Check volume permissions
# On Coolify server:
ls -la /var/lib/coolify/applications/{app-id}/

# Should show writable directories
drwxr-xr-x appuser appuser uploads/
drwxr-xr-x appuser appuser output/
drwxr-xr-x appuser appuser generated/

# Fix permissions if needed:
chown -R 1000:1000 /var/lib/coolify/applications/{app-id}/
```

#### 5. Out of Memory

**Symptom:** Container crashes under load

**Solutions:**
```bash
# Increase memory limit in Coolify
# Recommended: 2048 MB minimum

# Check current usage:
# In Coolify Metrics tab

# Optimize:
- Reduce image processing quality
- Limit concurrent requests
- Add request queuing
```

#### 6. Slow Build Times

**Symptom:** Builds take 10+ minutes

**Solutions:**
```bash
# Enable BuildKit in Coolify
# Enable build cache
# Use a closer pip mirror

# Add to Dockerfile (before pip install):
RUN pip config set global.index-url https://your-mirror/simple
```

### Debug Mode

Enable debug logging:

```bash
# In Coolify Environment Variables
FLASK_ENV=development
LOG_LEVEL=DEBUG
```

**⚠️ Warning:** Never use debug mode in production!

### Accessing Container Shell

Via Coolify UI:
1. Go to your application
2. Click **"Terminal"** or **"Shell"**
3. Access container shell directly

Via SSH:
```bash
# SSH to Coolify server
ssh user@coolify-server

# Find container
docker ps | grep social-image-generator

# Access shell
docker exec -it <container-id> bash
```

---

## Production Best Practices

### Security

#### 1. Use HTTPS Only
- ✅ Enable SSL via Coolify (Let's Encrypt)
- ✅ Force HTTPS redirect
- ✅ Use secure headers

#### 2. Environment Variables
- ✅ Store secrets in Coolify's encrypted storage
- ❌ Never commit secrets to Git
- ✅ Rotate API keys regularly

#### 3. Network Security
- ✅ Use Coolify's built-in firewall
- ✅ Limit access to necessary ports only
- ✅ Enable rate limiting if available

#### 4. Updates
- ✅ Keep Coolify updated
- ✅ Regularly rebuild images with latest base image
- ✅ Update Python dependencies

### Reliability

#### 1. Health Checks
- ✅ Use the built-in `/health` endpoint
- ✅ Set appropriate timeouts (60s start period)
- ✅ Monitor health check status

#### 2. Automatic Restarts
- ✅ Enable restart policy: `unless-stopped`
- ✅ Configure in Coolify automatically

#### 3. Backups
- ✅ Automated daily backups of volumes
- ✅ Store backups off-server
- ✅ Test restore procedures

#### 4. Monitoring
- ✅ Set up alerts for failures
- ✅ Monitor resource usage
- ✅ Track error rates

### Performance

#### 1. Resource Allocation
```yaml
Minimum: 1 CPU, 1GB RAM
Recommended: 2 CPU, 2GB RAM
High Traffic: 4 CPU, 4GB RAM
```

#### 2. Caching
- Consider adding Redis for caching
- Cache generated images
- Implement request deduplication

#### 3. CDN Integration
- Use CDN for serving generated images
- Reduce server load
- Improve global latency

### Maintenance

#### 1. Regular Updates
```bash
# Schedule monthly:
- Update base Docker image
- Update Python dependencies
- Review and apply security patches
```

#### 2. Log Management
```bash
# Configure log rotation in Coolify
# Keep logs for 7-30 days
# Export important logs for analysis
```

#### 3. Monitoring & Alerts
```bash
# Set up alerts for:
- Container restarts
- Health check failures
- High resource usage
- Disk space warnings
```

---

## Deployment Checklist

Use this checklist before going to production:

### Pre-Deployment

- [ ] Repository connected to Coolify
- [ ] Environment variables configured
- [ ] Persistent volumes configured
- [ ] Health check endpoint tested
- [ ] Domain configured (if using custom domain)
- [ ] SSL certificate provisioned
- [ ] Resource limits set appropriately

### Post-Deployment

- [ ] Application is accessible via URL
- [ ] Health check returns `{"status": "healthy"}`
- [ ] Test image upload: `POST /upload/main`
- [ ] Test image generation: `POST /generate`
- [ ] Verify persistent storage is working
- [ ] Check logs for errors
- [ ] Set up monitoring alerts
- [ ] Document API endpoint for team

### Production Readiness

- [ ] HTTPS enforced
- [ ] Secrets stored securely
- [ ] Backup strategy implemented
- [ ] Monitoring & alerts configured
- [ ] Resource limits tested under load
- [ ] Error handling tested
- [ ] Rate limiting considered
- [ ] Documentation updated

---

## Support & Resources

### Coolify Resources

- **Official Docs:** https://coolify.io/docs
- **Community Discord:** https://coollabs.io/discord
- **GitHub:** https://github.com/coollabsio/coolify

### This Application

- **API Reference:** See `API_REFERENCE.md`
- **cURL Examples:** See `COMPREHENSIVE_CURL_REFERENCE.md`
- **Docker Guide:** See `DOCKER_QUICKSTART.md`
- **Main README:** See `README.md`

### Getting Help

1. Check this guide first
2. Review Coolify's build/runtime logs
3. Test the `/health` endpoint
4. Check the troubleshooting section
5. Open an issue on GitHub

---

## Summary

Deploying to Coolify is straightforward:

1. **Connect repository** → Coolify clones your code
2. **Configure environment** → Set PORT, FLASK_ENV, etc.
3. **Add persistent storage** → For uploads, output, generated
4. **Deploy** → Coolify builds and starts your app
5. **Configure domain & SSL** → Optional but recommended
6. **Monitor** → Use health checks and alerts

**Your application is production-ready on Coolify!**

Key benefits:
- ✅ Zero-downtime deployments
- ✅ Automatic SSL certificates
- ✅ Built-in monitoring & logs
- ✅ Easy scaling & updates
- ✅ Self-hosted & private

---

**Happy deploying!** 🚀
