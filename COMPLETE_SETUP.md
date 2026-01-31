# 🚀 Complete Synova AI Setup Guide

## ✅ **Current Status**
- **GitHub Repository**: https://github.com/fuzzynetwork1989-alt/synova-ai
- **Docker Services**: Running (PostgreSQL, pgAdmin, Redis, Web)
- **Local API**: Working at http://localhost:8000
- **Database**: PostgreSQL connected

## 🔧 **PostgreSQL Configuration**

### **Database Credentials**
- **Host**: localhost:5432
- **Username**: postgres
- **Password**: postgres
- **Database**: synova_dev

### **pgAdmin Access**
- **URL**: http://localhost:5050
- **Email**: admin@synova.ai
- **Password**: admin

### **Connection String**
```
postgresql://postgres:postgres@localhost:5432/synova_dev
```

## 🐳 **Docker Desktop Services**

### **Running Services**
```bash
# Check status
docker ps

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Restart services
docker-compose up -d
```

### **Service URLs**
- **FastAPI App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050
- **Redis**: localhost:6379

## 🌐 **API Testing**

### **Health Check**
```bash
curl http://localhost:8000/api/health
```

### **Chat API**
```python
# Use the Python client
python example_api_client.py
```

### **API Endpoints**
- `GET /api/health` - Health check
- `GET /api/stats` - Application stats
- `POST /api/chat` - Chat with AI
- `GET /` - Web interface

## 🚂 **Railway Deployment Ready**

### **Repository Configuration**
- ✅ `railway.toml` configured
- ✅ `vercel.json` updated
- ✅ `render.yaml` ready
- ✅ Environment variables documented

### **Deployment Steps**
1. Go to https://railway.app
2. Login with GitHub (`fuzzynetwork1989-alt`)
3. New Project → Deploy from GitHub
4. Select `synova-ai` repository
5. Add PostgreSQL service
6. Set environment variables:
   ```
   SECRET_KEY=RJkWf2CkX36LUEDwU_3whZNcSxJrVCNQ82FN6SllBKc
   JWT_SECRET=irt7a-wwsxBHjtK1rTvpniCBSWZkpk4_M3e5C054-2Y
   ENVIRONMENT=production
   DEBUG=False
   RAILWAY_ENVIRONMENT=production
   ```

## 📱 **React Native Development**

### **Start Mobile App**
```bash
cd synova-ai
npm install
npx expo start
```

### **Mobile App URLs**
- **Expo Go**: Scan QR code
- **Web**: http://localhost:19006
- **Android**: `npx expo start --android`
- **iOS**: `npx expo start --ios`

## 🔐 **Security Configuration**

### **Generate New Secrets**
```python
python generate_secret.py
```

### **Environment Files**
- `.env.local` - Local development
- `.env.production` - Production settings
- `.env.example` - Template file

## 🧪 **Testing**

### **Run Tests**
```bash
# Python tests
pytest tests/ -v

# JavaScript tests
npm test

# Coverage report
pytest --cov=app tests/
```

### **API Testing**
```bash
# Test all endpoints
python example_api_client.py

# Manual testing
curl http://localhost:8000/api/health
```

## 📊 **Monitoring**

### **Application Stats**
```bash
curl http://localhost:8000/api/stats
```

### **Database Status**
```bash
# Connect to PostgreSQL
docker exec -it synova-ai-db-1 psql -U postgres -d synova_dev

# Check tables
\dt
```

## 🔄 **CI/CD Pipeline**

### **GitHub Actions**
- ✅ Python CI/CD configured
- ✅ Railway deployment workflow
- ✅ Code quality checks
- ✅ Automated testing

### **Manual Deploy**
```bash
# Push to trigger Railway deployment
git add .
git commit -m "Update for deployment"
git push origin main
```

## 🎯 **Next Steps**

1. **Test locally** - Verify all features work
2. **Deploy to Railway** - Get production URL
3. **Test production** - Verify deployment
4. **Set up custom domain** - Optional
5. **Monitor performance** - Check logs and stats

## 🆘 **Troubleshooting**

### **Common Issues**
- **Port conflicts**: Check if ports 8000, 5432, 5050 are available
- **Database connection**: Verify Docker containers are running
- **Environment variables**: Check `.env.local` configuration
- **Build failures**: Check `requirements.txt` dependencies

### **Get Help**
- Check Docker logs: `docker-compose logs`
- Check application logs: `docker-compose logs web`
- Verify database: Connect via pgAdmin
- Test API: Use health endpoint

---

**🎉 Your Synova AI application is fully configured and ready for deployment!**
