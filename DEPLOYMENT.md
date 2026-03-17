# Deployment Guide

## Table of Contents
1. [Backend Deployment](#backend-deployment)
2. [Frontend Deployment](#frontend-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Production Checklist](#production-checklist)

## Backend Deployment

### Local Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production (Uvicorn)

```bash
# Install production dependencies
pip install -r requirements.txt

# Run with multiple workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Or use Gunicorn with Uvicorn workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Environment Variables

Create `.env` file:
```env
MODEL_WEIGHTS=weights/best.pt
DEVICE=0  # GPU device, or 'cpu'
API_PORT=8000
CONF_THRESHOLD=0.25
ALLOWED_ORIGINS=https://yourdomain.com
```

### Systemd Service (Linux)

Create `/etc/systemd/system/cotton-api.service`:

```ini
[Unit]
Description=Cotton Disease Detection API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable cotton-api
sudo systemctl start cotton-api
sudo systemctl status cotton-api
```

## Frontend Deployment

### Build for Production

```bash
cd frontend
npm install
npm run build
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel deploy --prod
```

### Deploy to Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd frontend
netlify deploy --prod --dir=dist
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    root /path/to/frontend/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Docker Deployment

### Build Backend Image

```bash
cd backend
docker build -t cotton-disease-api:latest .
```

### Run Backend Container

```bash
docker run -d \
  --name cotton-api \
  -p 8000:8000 \
  -v $(pwd)/weights:/app/weights \
  -e DEVICE=cpu \
  cotton-disease-api:latest
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend/weights:/app/weights
      - ./data:/app/data
    environment:
      - DEVICE=cpu
      - MODEL_WEIGHTS=/app/weights/best.pt
    restart: unless-stopped
    
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

## Cloud Deployment

### AWS EC2

1. **Launch EC2 Instance**:
   - AMI: Ubuntu 22.04 LTS
   - Instance Type: t3.medium (or g4dn.xlarge for GPU)
   - Security Group: Allow ports 22, 80, 443, 8000

2. **Setup**:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.10 python3-pip python3-venv -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Clone repository
git clone <your-repo-url>
cd cotton-disease-detection

# Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install
npm run build
```

3. **Configure Nginx**:
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/cotton-disease
# Add configuration from above
sudo ln -s /etc/nginx/sites-available/cotton-disease /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Google Cloud Platform (GCP)

1. **Create Compute Engine Instance**
2. **Setup similar to AWS EC2**
3. **Configure firewall rules**

### Azure

1. **Create Virtual Machine**
2. **Setup similar to AWS EC2**
3. **Configure Network Security Group**

### Heroku (Backend Only)

Create `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Deploy:
```bash
heroku create cotton-disease-api
git push heroku main
```

## Production Checklist

### Security
- [ ] Enable HTTPS (SSL/TLS certificates)
- [ ] Configure CORS properly
- [ ] Set strong environment variables
- [ ] Disable debug mode
- [ ] Implement rate limiting
- [ ] Add authentication (if needed)
- [ ] Regular security updates

### Performance
- [ ] Enable gzip compression
- [ ] Configure caching headers
- [ ] Use CDN for static assets
- [ ] Optimize images
- [ ] Enable HTTP/2
- [ ] Monitor resource usage

### Monitoring
- [ ] Setup logging (ELK stack, CloudWatch, etc.)
- [ ] Configure error tracking (Sentry)
- [ ] Setup uptime monitoring
- [ ] Configure alerts
- [ ] Monitor API performance

### Backup
- [ ] Backup model weights
- [ ] Backup prediction logs
- [ ] Backup configuration files
- [ ] Setup automated backups

### Documentation
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Deployment procedures
- [ ] Troubleshooting guide
- [ ] User manual

## SSL/TLS Setup (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Monitoring with PM2 (Alternative to Systemd)

```bash
# Install PM2
npm install -g pm2

# Start backend
cd backend
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name cotton-api

# Save PM2 configuration
pm2 save
pm2 startup
```

## Troubleshooting

### Backend won't start
- Check Python version (3.10+)
- Verify all dependencies installed
- Check model weights path
- Review logs: `journalctl -u cotton-api -f`

### Frontend build fails
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node version (18+)
- Verify API URL in environment variables

### Slow inference
- Enable GPU if available
- Reduce image size
- Use ONNX runtime
- Increase worker count

### High memory usage
- Limit batch size
- Reduce worker count
- Monitor with `htop` or `nvidia-smi`

## Scaling

### Horizontal Scaling
- Load balancer (Nginx, HAProxy)
- Multiple backend instances
- Shared model weights (NFS, S3)

### Vertical Scaling
- Larger instance type
- More CPU/RAM
- Better GPU

### Auto-scaling
- Kubernetes deployment
- AWS Auto Scaling Groups
- GCP Managed Instance Groups

## Cost Optimization

1. **Use spot instances** for non-critical workloads
2. **Schedule instances** to run only when needed
3. **Optimize model size** (quantization, pruning)
4. **Use CDN** for static assets
5. **Monitor usage** and right-size instances

---

For questions or issues, please open an issue on GitHub or contact support.
