# 🆓 Terraform AWS Free Tier - Filosofía App

## 📋 Descripción
Configuración Terraform para desplegar la aplicación de filosofía en AWS usando **exclusivamente recursos del Free Tier** - **$0.00 de costo**.

## 🛠️ Recursos Creados (FREE TIER)

| Recurso | Tipo | Límite Free Tier | Uso Estimado |
|---------|------|------------------|--------------|
| EC2 | t2.micro | 750h/mes | 24/7 (744h) |
| RDS | db.t2.micro | 750h/mes | 24/7 (744h) |
| S3 | Almacenamiento | 5GB | ~50MB |
| S3 | Requests | 20k GET, 2k PUT | ~1k total |
| EBS | Storage | 30GB | 8GB |
| Data Transfer | Salida | 1GB | ~100MB |

**💰 Costo Total: $0.00** (válido por 12 meses)

## 🚀 Uso Rápido

### 1. Preparación
```bash
# Instalar Terraform
# Ubuntu/Debian:
sudo apt-get update && sudo apt-get install -y terraform

# macOS:
brew install terraform

# Verificar instalación
terraform --version
```

### 2. Configurar AWS
```bash
# Instalar AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configurar credenciales
aws configure
```

### 3. Configurar SSH
```bash
# Generar clave SSH si no existe
ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa

# Verificar que existe la clave pública
ls ~/.ssh/id_rsa.pub
```

### 4. Configurar Variables
```bash
# Copiar archivo de ejemplo
cp terraform.tfvars.example terraform.tfvars

# Editar configuración
nano terraform.tfvars
```

### 5. Deploy
```bash
# Ir al directorio terraform
cd terraform

# Inicializar Terraform
terraform init

# Ver plan de deployment
terraform plan

# Aplicar configuración
terraform apply
```

### 6. Verificar Deployment
Terraform mostrará las URLs al finalizar:
- **Frontend**: `http://IP_PUBLICA:3000`
- **Backend**: `http://IP_PUBLICA:8000`
- **API Docs**: `http://IP_PUBLICA:8000/docs`

## 📝 Variables Configurables

| Variable | Descripción | Default | Requerida |
|----------|-------------|---------|-----------|
| `project_name` | Nombre del proyecto | `filosofia-app` | No |
| `environment` | Ambiente (dev/prod) | `prod` | No |
| `aws_region` | Región AWS | `us-east-1` | No |
| `db_password` | Password RDS | - | **Sí** |

## 🔧 Personalización

### Cambiar Región
```hcl
aws_region = "eu-west-1"  # Irlanda
aws_region = "ap-southeast-1"  # Singapur
```

### Ajustar Configuración
```hcl
project_name = "mi-filosofia-app"
environment  = "staging"
```

## 📊 Monitoreo

### Verificar Estado
```bash
# Estado de la infraestructura
terraform show

# Lista de recursos
terraform state list

# Información de un recurso específico
terraform state show aws_instance.main
```

### Logs de la Aplicación
```bash
# Conectar por SSH
ssh -i ~/.ssh/id_rsa ec2-user@IP_PUBLICA

# Ver logs
cd filosofia-app
docker-compose logs -f
```

## 🧹 Limpieza

### Destruir Infraestructura
```bash
# ⚠️ CUIDADO: Esto elimina TODO
terraform destroy

# Con confirmación automática
terraform destroy -auto-approve
```

### Limpieza Parcial
```bash
# Eliminar solo RDS
terraform destroy -target=aws_db_instance.main

# Eliminar solo EC2
terraform destroy -target=aws_instance.main
```

## 🔐 Seguridad

### Mejores Prácticas
1. **SSH**: Cambiar `0.0.0.0/0` por tu IP específica
2. **RDS**: Restringir acceso solo desde EC2
3. **Secrets**: No commitear `terraform.tfvars`
4. **State**: Usar backend remoto en producción

### Configuración Segura
```hcl
# En ec2.tf, cambiar:
cidr_blocks = ["TU_IP/32"]  # Solo tu IP

# En rds.tf, eliminar:
# cidr_blocks = ["0.0.0.0/0"]  # Solo security groups
```

## 🚨 Troubleshooting

### Errores Comunes

#### SSH Key No Encontrada
```bash
# Verificar clave SSH
ls ~/.ssh/id_rsa.pub

# Regenerar si no existe
ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa
```

#### RDS Connection Timeout
```bash
# Verificar security groups
aws ec2 describe-security-groups --group-names filosofia-app-prod-rds

# Verificar desde EC2
ssh ec2-user@IP_PUBLICA
telnet RDS_ENDPOINT 5432
```

#### Aplicación No Responde
```bash
# Conectar a EC2
ssh ec2-user@IP_PUBLICA

# Verificar Docker
docker ps
docker-compose logs

# Reiniciar servicios
docker-compose restart
```

### Verificar Free Tier
```bash
# Ver facturación AWS
aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-02-01 --granularity MONTHLY --metrics BlendedCost
```

## 📚 Recursos Adicionales

- [AWS Free Tier](https://aws.amazon.com/free/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)

## 💡 Tips

1. **Monitoring**: Configurar CloudWatch alarms gratuitos
2. **Backup**: RDS automático deshabilitado para FREE TIER
3. **SSL**: Usar CloudFlare gratis para HTTPS
4. **Domain**: Usar subdominios gratuitos como `app.tu-dominio.com`
5. **CI/CD**: GitHub Actions con AWS credentials

---

**✅ Garantía Free Tier**: Esta configuración usa exclusivamente recursos gratuitos de AWS por 12 meses.
