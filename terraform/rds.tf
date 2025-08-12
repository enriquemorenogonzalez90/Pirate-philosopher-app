# 🗄️ RDS POSTGRESQL - FREE TIER
# ✅ db.t2.micro gratis, 20GB storage

# Subnet group para RDS
resource "aws_db_subnet_group" "main" {
  name       = "${local.name_prefix}-db-subnet-group"
  subnet_ids = [aws_subnet.public_1.id, aws_subnet.public_2.id]

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-db-subnet-group"
  })
}

# Security group para RDS
resource "aws_security_group" "rds" {
  name_prefix = "${local.name_prefix}-rds"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ec2.id]
    description     = "PostgreSQL from EC2"
  }

  # Acceso desde tu IP para administración
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # ⚠️ Cambiar por tu IP en producción
    description = "PostgreSQL admin access"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-rds-sg"
  })
}

# RDS PostgreSQL instance - FREE TIER
resource "aws_db_instance" "main" {
  # Configuración FREE TIER
  identifier     = "${local.name_prefix}-db"
  engine         = "postgres"
  engine_version = "13.13"
  instance_class = "db.t2.micro"  # ✅ FREE TIER
  
  # Storage FREE TIER
  allocated_storage     = 20     # ✅ 20GB gratis
  max_allocated_storage = 20     # No auto-scaling para evitar costos
  storage_type          = "gp2"
  storage_encrypted     = false  # Encryption requiere t3.micro (de pago)

  # Database configuration
  db_name  = "filosofia_db"
  username = "admin"
  password = var.db_password

  # Network
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = true  # Para acceso desde EC2 e internet

  # Backup configuration (FREE)
  backup_retention_period = 0  # Sin backups automáticos para FREE TIER
  backup_window          = null
  maintenance_window     = "sun:03:00-sun:04:00"

  # Performance
  performance_insights_enabled = false  # De pago
  monitoring_interval         = 0       # CloudWatch básico gratis

  # Deletion protection
  deletion_protection      = false
  delete_automated_backups = true
  skip_final_snapshot     = true

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-postgres"
  })
}

# Outputs
output "rds_endpoint" {
  description = "RDS endpoint"
  value       = aws_db_instance.main.endpoint
}

output "rds_port" {
  description = "RDS port"
  value       = aws_db_instance.main.port
}

output "database_url" {
  description = "Database connection URL"
  value       = "postgresql://admin:${var.db_password}@${aws_db_instance.main.endpoint}:${aws_db_instance.main.port}/filosofia_db"
  sensitive   = true
}
