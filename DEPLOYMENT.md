# AfriBnB Deployment Guide

## 🚀 Deploy to Render (Recommended - Free Tier)

Render provides a free PostgreSQL database + free web service tier. This is the fastest way to get your app live.

### Prerequisites

- GitHub account with your code pushed
- Render account (https://render.com - free to sign up)
- About 5 minutes

### Step-by-Step Deployment

#### 1. Push to GitHub

```bash
cd c:\Dev\AfriBnB

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Production-ready AfriBnB MVP with full API and auth"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/afribnb.git

# Push to main branch
git branch -M main
git push -u origin main
```

#### 2. Create Render PostgreSQL Database

1. Go to https://render.com/dashboard
2. Click "New" → "PostgreSQL"
3. Choose:
   - Name: `afribnb-db`
   - Database: `afribnb`
   - Region: Closest to you
   - PostgreSQL Version: 12 or later
   - Plan: **Free** tier
4. Click "Create Database"
5. Copy the `Internal Database URL` (you'll need this)

⏱️ Database creation takes ~1 minute

#### 3. Create Render Web Service

1. Click "New" → "Web Service"
2. Select your GitHub repository
3. Configure:
   - **Name**: `afribnb-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
   - **Instance Type**: Free
4. Click "Create Web Service"

#### 4. Add Environment Variables

Once the web service is created:

1. Go to the service dashboard
2. Click "Environment" in left sidebar
3. Add these variables:

```
DATABASE_URL=[paste the internal database URL from step 2]
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your-random-secret-key-min-32-chars-change-this-securely
JWT_SECRET_KEY=your-random-jwt-secret-key-min-32-chars-change-this-too
PORT=5000
```

💡 **Generate strong secret keys**:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

5. Click "Save Changes"

#### 5. Deploy

Render automatically starts deployment when you:
- Create the service
- Push new commits to GitHub

View deployment logs in the service dashboard. ✅ You're done!

### ✅ Verify Deployment

Once deployment is complete (look for green checkmark):

1. Click the URL shown (e.g., `https://afribnb-api.onrender.com`)
2. You should see the AfriBnB frontend
3. Test the API:

```bash
# Test health endpoint
curl https://YOUR_RENDER_URL/api/health

# Register a user
curl -X POST https://YOUR_RENDER_URL/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

## 🔄 Continuous Deployment

Every time you push to GitHub, Render automatically:
1. Detects the push
2. Rebuilds your application
3. Deploys the new version

To push updates:

```bash
git add .
git commit -m "Update message"
git push origin main
```

## 📊 Alternative Deployment Options

### Deploy to Railway

1. Go to https://railway.app
2. Connect GitHub
3. Select repository
4. Add PostgreSQL plugin
5. Set environment variables
6. Deploy

### Deploy to Heroku (Legacy)

```bash
heroku login
heroku create afribnb-app
git push heroku main
heroku config:set DATABASE_URL=your_postgres_url
heroku open
```

### Deploy to Digital Ocean App Platform

1. Connect GitHub repository
2. Select `app.yaml` configuration
3. Add PostgreSQL service
4. Deploy

## 🛠️ Troubleshooting Deployment

### Build Fails

Check the build logs in Render dashboard. Common issues:

**Missing dependencies**
```bash
pip freeze > requirements.txt  # Update requirements
git add requirements.txt
git commit -m "Update dependencies"
git push
```

**Python version issue**
- Set Python version in `runtime.txt`:
```
python-3.9.16
```

### Application Crashes

Check the logs:
1. Go to Render service dashboard
2. Click "Logs" tab
3. Look for error messages

Common fixes:

**Database connection error**
- Verify `DATABASE_URL` is correct
- Ensure database is ready (not still starting)

**Import errors**
- Check all imports in `app.py` are available in `requirements.txt`

**PORT not listening**
- The Render start command already handles PORT binding
- Don't hardcode port 5000

### API Returns 502 Bad Gateway

- Check application logs for errors
- Verify environment variables are set
- Ensure start command is correct: `gunicorn wsgi:app`

## 📈 Monitoring & Logs

To monitor your deployed app:

1. **Logs**: Service Dashboard → Logs tab
2. **Metrics**: Service Dashboard → Metrics tab
3. **Environment**: Service Dashboard → Environment tab

## 💰 Pricing & Costs

**Render Free Tier** includes:
- ✅ Web service (shared CPU) - **free forever**
- ✅ PostgreSQL database - **free forever** (0.5 GB storage)
- ✅ 100 GB/month bandwidth
- ✅ Automatic SSL certificates

**Limits**:
- Services spin down after 15 min of inactivity
- Max 0.5GB RAM, 0.5GB storage
- Spins back up on first request (5-10 sec cold start)

**When to upgrade**:
- You need faster performance (paid instances: $7/mo)
- You need more database storage (paid tiers: $15/mo)
- You need multiple instances

## 🔐 Security in Production

Before going live with real users:

### Secrets Management
- [ ] Use strong random secrets for `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Never commit secrets to GitHub
- [ ] Use environment variables (done via Render dashboard)
- [ ] Rotate secrets periodically

### Database
- [ ] Enable automatic backups (Render does this)
- [ ] Use strong database password
- [ ] Restrict database access to app only

### HTTPS
- [ ] Render provides free SSL/TLS (automatic)
- [ ] All traffic is encrypted
- [ ] No additional setup needed

### Application
- [ ] `DEBUG=False` in production (✅ already set)
- [ ] Validate all user inputs (✅ basic validation in place)
- [ ] Use strong password hashing with bcrypt (✅ implemented)
- [ ] Keep dependencies updated

## 📝 Next Steps

After deployment:

1. **Create a custom domain**:
   - Go to Service Settings → Custom Domain
   - Add your domain and follow DNS instructions

2. **Set up monitoring**:
   - Enable Sentry integration for error tracking
   - Setup alerts for failures

3. **Add more features**:
   - Image upload for listings
   - Booking system
   - Payment processing
   - Email notifications

4. **Scale when needed**:
   - Upgrade to paid plan for consistent uptime
   - Add caching layer (Redis)
   - Setup CDN for static files

## 🆘 Getting Help

- **Render docs**: https://render.com/docs
- **Flask docs**: https://flask.palletsprojects.com
- **Database issues**: Render support via dashboard
- **GitHub issues**: Create issue in your repository

---

Your AfriBnB API is now deployed and accessible to the world! 🎉
