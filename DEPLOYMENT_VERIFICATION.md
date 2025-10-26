# Pre-Deployment Verification Guide

This guide will help you verify that your code is working correctly BEFORE deploying to production.

## 🎯 Problem You're Experiencing

Your production server (https://imageeditor.flowiran.ir) returns:
- ✅ Health check passes (server is healthy)
- ❌ `/layouts` endpoint returns 404 (new code not deployed)

**Why?** Production is running OLD code without the layout engine.

**Solution:** Verify code works locally first, then deploy.

---

## 📋 3-Step Verification Process

### Step 1: Verify Code Files (No Server Needed)

This checks if all required files exist in your code.

```bash
python verify_code.py
```

**Expected Output:**
```
✅ Main API file exists
✅ Has /layouts endpoint
✅ Has /generate_post endpoint
✅ Layout engine module
✅ All 7 layout implementations
...
CODE VERIFICATION PASSED!
```

**If This Fails:**
- Check you're on the correct branch:
  ```bash
  git status
  # Should show: claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u
  ```
- If not, checkout the branch:
  ```bash
  git checkout claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u
  git pull origin claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u
  ```

---

### Step 2: Test Local Server

Start your local server and test it:

```bash
# Terminal 1: Start server
python social_image_api.py

# Terminal 2: Run tests (wait for server to start first)
python test_local_server.py
```

**Expected Output:**
```
🧪 LOCAL SERVER VERIFICATION

STEP 1: Check if Local Server is Running
✅ Local server is running!

STEP 2: Test /health Endpoint
✅ Health endpoint works!

STEP 3: Test /layouts Endpoint (NEW)
✅ /layouts endpoint works! Found 7 layouts

STEP 4: Test /generate_post Endpoint (NEW)
✅ /generate_post endpoint works!

STEP 5: Test Farsi/RTL Text Support
✅ Farsi text works!

STEP 6: Test All Layout Types
  Testing headline_promo...
  ✅ headline_promo: OK
  Testing split_image_text...
  ✅ split_image_text: OK
  ... (all 7 layouts)

FINAL SUMMARY
🎉 ALL TESTS PASSED!

READY FOR PRODUCTION DEPLOYMENT
```

**What This Tests:**
- ✅ Server starts correctly
- ✅ `/layouts` endpoint exists and returns 7 layouts
- ✅ `/generate_post` endpoint works
- ✅ All 7 layout types generate images
- ✅ Farsi/RTL text renders correctly
- ✅ External images load successfully

**If Tests Fail:**
- Check error messages - they'll tell you exactly what's wrong
- Most common issue: Running old code (see Step 1)
- Check server logs for detailed errors

---

### Step 3: Deploy to Production

**Only proceed if Steps 1 and 2 pass!**

#### Option A: Deploy Feature Branch Directly (Fastest)

```bash
# On production server
ssh your-server-user@your-server-ip

cd /path/to/your/app

# Fetch latest
git fetch origin

# Checkout feature branch
git checkout claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u

# Pull latest
git pull origin claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u

# Restart your server
# (Method depends on your setup)

# Examples:
sudo systemctl restart your-app-name    # If using systemd
docker-compose restart                   # If using Docker
pm2 restart app                         # If using PM2
# Or manually stop and start: Ctrl+C then python social_image_api.py
```

#### Option B: Merge to Main First (Recommended)

1. **Create Pull Request on GitHub:**
   - Go to: https://github.com/MohammadHamidi/social-image-generator/compare/main...claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u
   - Create PR
   - Review changes
   - Merge to main

2. **Deploy main branch:**
   ```bash
   # On production server
   git checkout main
   git pull origin main
   # Restart server
   ```

---

## 🧪 Verify Production Deployment

After deploying, test production:

```bash
python test_production_deployment.py
```

**Expected Output:**
```
🚀 Production Deployment Test Suite

TEST 1: System Health Check
✅ System is healthy!

TEST 2: Available Layouts
✅ Found 7 available layouts

TEST 3: Layout Generation Tests
✅ All layouts work

TEST SUMMARY
🎉 All tests passed! Production system is working perfectly!
```

---

## 🔧 Troubleshooting

### Issue: `verify_code.py` shows missing files

**Solution:**
```bash
# Check your branch
git status

# Should show: On branch claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u
# If not:
git checkout claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u
git pull origin claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u
```

### Issue: Local server test shows 404 on `/layouts`

**Solution:** You're running old code. Stop server, verify branch, restart:
```bash
# Ctrl+C to stop server
git status  # Check branch
git checkout claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u  # Switch if needed
python social_image_api.py  # Restart
```

### Issue: Can't connect to local server

**Solution:** Server not running:
```bash
python social_image_api.py
# Wait for: "Running on http://127.0.0.1:5000"
# Then run tests in another terminal
```

### Issue: Production still returns 404 after deployment

**Solutions:**
1. **Check deployment actually happened:**
   ```bash
   ssh your-server
   cd /path/to/app
   git log --oneline -5  # Check latest commits
   git branch  # Verify correct branch
   ```

2. **Check server restarted:**
   ```bash
   # Check if process is running
   ps aux | grep python

   # Restart server
   sudo systemctl restart your-app
   ```

3. **Check server logs:**
   ```bash
   # Location depends on your setup
   tail -f /var/log/your-app.log
   journalctl -u your-app -f  # If using systemd
   docker logs container-name  # If using Docker
   ```

---

## 📊 What Each Script Does

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `verify_code.py` | Check files exist | Before starting server |
| `test_local_server.py` | Test local server | Before deploying |
| `test_production_deployment.py` | Test production | After deploying |
| `diagnose_production.py` | Check what's deployed | When production fails |
| `test_old_endpoints.py` | Test pre-layout endpoints | If new endpoints missing |

---

## ✅ Success Checklist

Before deploying to production, ensure:

- [ ] `verify_code.py` passes (all files present)
- [ ] Local server starts without errors
- [ ] `test_local_server.py` passes (all tests ✅)
- [ ] All 7 layouts generate images locally
- [ ] Farsi text renders correctly locally
- [ ] External images load successfully locally

After deploying to production:

- [ ] Production server restarts successfully
- [ ] `test_production_deployment.py` passes
- [ ] All 7 layouts work in production
- [ ] Farsi text works in production

---

## 🎯 Quick Reference

**Before Deployment:**
```bash
# 1. Verify code
python verify_code.py

# 2. Start server
python social_image_api.py

# 3. Test server (different terminal)
python test_local_server.py
```

**Deploy:**
```bash
# On production server
git checkout claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u
git pull
# Restart server
```

**After Deployment:**
```bash
# Test production
python test_production_deployment.py
```

---

## 📞 Still Having Issues?

If all local tests pass but production still fails:

1. **Check production is actually running new code:**
   ```bash
   python diagnose_production.py
   ```

2. **Compare production vs local:**
   - Local has `/layouts`? Check with: `curl http://localhost:5000/layouts`
   - Production missing it? Check deployment steps again

3. **Check server logs** for specific error messages

---

**The key:** If local tests pass, your code is correct. Any production issues are deployment-related, not code-related.
