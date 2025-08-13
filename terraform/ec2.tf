# 🖥️ EC2 INSTANCE - FREE TIER
# ✅ t2.micro gratis (750h/mes)

# Key pair
resource "aws_key_pair" "main" {
  key_name   = "${local.name_prefix}-key"
  public_key = file("~/.ssh/id_rsa.pub")  # Usar tu clave SSH existente

  tags = local.tags
}

# Security group para EC2
resource "aws_security_group" "ec2" {
  name_prefix = "${local.name_prefix}-ec2"
  vpc_id      = aws_vpc.main.id

  # SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH access"
  }

  # HTTP
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP"
  }

  # HTTPS
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS"
  }

  # Frontend (Next.js)
  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Frontend Next.js"
  }

  # Backend (FastAPI)
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Backend FastAPI"
  }

  # Outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-ec2-sg"
  })
}

# IAM role para EC2 (acceso a S3)
resource "aws_iam_role" "ec2_role" {
  name = "${local.name_prefix}-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = local.tags
}

# Policy para acceso a S3
resource "aws_iam_role_policy" "ec2_s3_policy" {
  name = "${local.name_prefix}-ec2-s3-policy"
  role = aws_iam_role.ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "${aws_s3_bucket.images.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.images.arn
      }
    ]
  })
}

# Instance profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${local.name_prefix}-ec2-profile"
  role = aws_iam_role.ec2_role.name

  tags = local.tags
}

# User data script
locals {
  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    s3_bucket         = aws_s3_bucket.images.bucket
    database_url      = "postgresql://admin:${var.db_password}@${aws_db_instance.main.endpoint}:${aws_db_instance.main.port}/filosofia_db"
    aws_region        = var.aws_region
    cloudfront_domain = "https://${aws_s3_bucket.images.bucket}.s3.amazonaws.com"
  }))
}

# EC2 Instance - FREE TIER
resource "aws_instance" "main" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t2.micro"  # ✅ FREE TIER
  key_name              = aws_key_pair.main.key_name
  vpc_security_group_ids = [aws_security_group.ec2.id]
  subnet_id             = aws_subnet.public_1.id
  iam_instance_profile  = aws_iam_instance_profile.ec2_profile.name

  # User data para setup inicial
  user_data = local.user_data

  # Storage FREE TIER
  root_block_device {
    volume_type = "gp2"
    volume_size = 8  # ✅ 30GB gratis EBS, usamos solo 8GB
    encrypted   = false
  }

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-server"
  })
}

# Outputs
output "ec2_public_dns" {
  description = "DNS público de EC2"
  value       = aws_instance.main.public_dns
}

output "ssh_command" {
  description = "Comando SSH para conectar"
  value       = "ssh -i ~/.ssh/id_rsa ec2-user@${aws_instance.main.public_ip}"
}
