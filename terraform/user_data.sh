#!/bin/bash

# 🚀 USER DATA SCRIPT PARA EC2
# Configuración automática de la aplicación Filosofía

set -e

# Log todo
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
echo "🚀 Iniciando configuración de Filosofía App..."

# Update system
yum update -y

# Install Docker
yum install -y docker git htop curl

# Start Docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Create app directory
mkdir -p /home/ec2-user/filosofia-app
cd /home/ec2-user/filosofia-app

# Create environment file
cat > .env.production << EOF
# Database
DATABASE_URL=${database_url}

# AWS Configuration
AWS_REGION=${aws_region}
S3_BUCKET_IMAGES=${s3_bucket}
CLOUDFRONT_DOMAIN=${cloudfront_domain}
USE_S3=true

# API Configuration
CORS_ORIGINS=*
NEXT_PUBLIC_API_URL=http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000
NEXT_PUBLIC_CDN_URL=${cloudfront_domain}
EOF

# Create minimal docker-compose for deployment
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  backend:
    image: ghcr.io/balladofathinman/pirate-philosopher-app/backend:latest
    environment:
      - DATABASE_URL=${database_url}
      - AWS_REGION=${aws_region}
      - S3_BUCKET_IMAGES=${s3_bucket}
      - CLOUDFRONT_DOMAIN=${cloudfront_domain}
      - USE_S3=true
      - CORS_ORIGINS=*
    ports:
      - "8000:8000"
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 400M

  frontend:
    image: ghcr.io/balladofathinman/pirate-philosopher-app/frontend:latest
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - NEXT_PUBLIC_CDN_URL=${cloudfront_domain}
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 400M
EOF

# Set ownership
chown -R ec2-user:ec2-user /home/ec2-user/filosofia-app

# Create startup script
cat > /home/ec2-user/start-app.sh << 'EOF'
#!/bin/bash
cd /home/ec2-user/filosofia-app
docker-compose --env-file .env.production up -d
EOF

chmod +x /home/ec2-user/start-app.sh
chown ec2-user:ec2-user /home/ec2-user/start-app.sh

# Create systemd service para auto-start
cat > /etc/systemd/system/filosofia-app.service << 'EOF'
[Unit]
Description=Filosofia App
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
User=ec2-user
WorkingDirectory=/home/ec2-user/filosofia-app
ExecStart=/usr/local/bin/docker-compose --env-file .env.production up -d
ExecStop=/usr/local/bin/docker-compose down

[Install]
WantedBy=multi-user.target
EOF

# Enable service (pero no lo iniciamos hasta tener las imágenes)
systemctl enable filosofia-app

echo "✅ Configuración de EC2 completada"
echo "📋 Para deployar la app:"
echo "   1. ssh ec2-user@$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "   2. cd filosofia-app"
echo "   3. docker-compose up -d"

# Create info file
cat > /home/ec2-user/deployment-info.txt << EOF
🚀 FILOSOFÍA APP - DEPLOYMENT INFO

📍 URLs:
   - Frontend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):3000
   - Backend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000
   - API Docs: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000/docs

🔧 Comandos útiles:
   - Ver logs: docker-compose logs -f
   - Reiniciar: docker-compose restart
   - Parar: docker-compose down
   - Estado: docker-compose ps

📊 Recursos:
   - S3 Bucket: ${s3_bucket}
   - Database: PostgreSQL RDS
   - Instancia: t2.micro (FREE TIER)

💰 Costo: $0.00 (FREE TIER)
EOF

chown ec2-user:ec2-user /home/ec2-user/deployment-info.txt

echo "🎉 Setup completado. La instancia está lista para deployment."
