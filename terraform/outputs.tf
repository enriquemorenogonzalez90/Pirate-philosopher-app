# 📤 OUTPUTS PRINCIPALES

# URLs de la aplicación
output "frontend_url" {
  description = "URL del frontend"
  value       = "http://${aws_instance.main.public_ip}:3000"
}

output "backend_url" {
  description = "URL del backend"
  value       = "http://${aws_instance.main.public_ip}:8000"
}

output "api_docs_url" {
  description = "URL de la documentación de la API"
  value       = "http://${aws_instance.main.public_ip}:8000/docs"
}

# Información de conexión
output "ssh_connection" {
  description = "Comando para conectar por SSH"
  value       = "ssh -i ~/.ssh/id_rsa ec2-user@${aws_instance.main.public_ip}"
}

output "ec2_public_ip" {
  description = "IP pública de la instancia EC2"
  value       = aws_instance.main.public_ip
}

# Recursos AWS
output "s3_bucket_name" {
  description = "Nombre del bucket S3 para imágenes"
  value       = aws_s3_bucket.images.bucket
}

output "s3_bucket_url" {
  description = "URL del bucket S3"
  value       = "https://${aws_s3_bucket.images.bucket}.s3.amazonaws.com"
}

output "rds_endpoint" {
  description = "Endpoint de la base de datos RDS"
  value       = aws_db_instance.main.endpoint
}

# Variables de entorno para la aplicación
output "environment_variables" {
  description = "Variables de entorno para la aplicación"
  value = {
    DATABASE_URL      = "postgresql://admin:${var.db_password}@${aws_db_instance.main.endpoint}:${aws_db_instance.main.port}/filosofia_db"
    AWS_REGION        = var.aws_region
    S3_BUCKET_IMAGES  = aws_s3_bucket.images.bucket
    CLOUDFRONT_DOMAIN = "https://${aws_s3_bucket.images.bucket}.s3.amazonaws.com"
    USE_S3           = "true"
    CORS_ORIGINS     = "*"
    NEXT_PUBLIC_API_URL = "http://${aws_instance.main.public_ip}:8000"
    NEXT_PUBLIC_CDN_URL = "https://${aws_s3_bucket.images.bucket}.s3.amazonaws.com"
  }
  sensitive = true
}

# Resumen de costos
output "cost_summary" {
  description = "Resumen de costos (FREE TIER)"
  value = {
    ec2_instance    = "t2.micro - FREE (750h/mes)"
    rds_instance    = "db.t2.micro - FREE (750h/mes)"
    s3_storage      = "5GB - FREE"
    s3_requests     = "20k GET, 2k PUT - FREE"
    ebs_storage     = "30GB - FREE (usando 8GB)"
    data_transfer   = "1GB salida - FREE"
    total_monthly   = "$0.00"
    free_tier_expires = "12 meses desde creación de cuenta"
  }
}

# Información de deployment
output "deployment_info" {
  description = "Información para el deployment"
  value = {
    message = "✅ Infraestructura creada exitosamente"
    next_steps = [
      "1. Conectar por SSH: ssh -i ~/.ssh/id_rsa ec2-user@${aws_instance.main.public_ip}",
      "2. Verificar que Docker esté funcionando: docker --version",
      "3. Ir al directorio: cd filosofia-app",
      "4. Subir las imágenes Docker a un registry público",
      "5. Actualizar docker-compose.yml con las imágenes correctas",
      "6. Iniciar la aplicación: docker-compose up -d"
    ]
    warnings = [
      "⚠️ Cambiar el acceso SSH de 0.0.0.0/0 a tu IP específica",
      "⚠️ Cambiar el acceso RDS de 0.0.0.0/0 a solo el security group de EC2",
      "⚠️ Configurar un dominio personalizado para producción"
    ]
  }
}
