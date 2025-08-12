#!/bin/bash

# 🚀 DEPLOYMENT AUTOMÁTICO CON TERRAFORM
# Filosofía App - AWS Free Tier ($0.00)

set -e

echo "🆓 TERRAFORM DEPLOYMENT - AWS FREE TIER"
echo "======================================="

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Función de ayuda
show_help() {
    echo -e "${BLUE}Uso: $0 [opción]${NC}"
    echo ""
    echo "Opciones:"
    echo "  init     - Inicializar Terraform"
    echo "  plan     - Ver plan de deployment"
    echo "  apply    - Crear infraestructura"
    echo "  destroy  - Eliminar infraestructura"
    echo "  outputs  - Mostrar outputs"
    echo "  ssh      - Conectar por SSH a EC2"
    echo "  logs     - Ver logs de la aplicación"
    echo "  help     - Mostrar esta ayuda"
    echo ""
    echo -e "${GREEN}Ejemplo: $0 apply${NC}"
}

# Verificar prerequisitos
check_prerequisites() {
    echo -e "${BLUE}📋 Verificando prerequisitos...${NC}"
    
    # Terraform
    if ! command -v terraform &> /dev/null; then
        echo -e "${RED}❌ Terraform no está instalado${NC}"
        echo "Instalar: https://www.terraform.io/downloads.html"
        exit 1
    fi
    
    # AWS CLI
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}❌ AWS CLI no está instalado${NC}"
        echo "Instalar: https://aws.amazon.com/cli/"
        exit 1
    fi
    
    # Credenciales AWS
    if ! aws sts get-caller-identity &> /dev/null; then
        echo -e "${RED}❌ Credenciales AWS no configuradas${NC}"
        echo "Ejecutar: aws configure"
        exit 1
    fi
    
    # SSH Key
    if [ ! -f ~/.ssh/id_rsa.pub ]; then
        echo -e "${YELLOW}⚠️ SSH key no encontrada, creando...${NC}"
        ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa -N ""
    fi
    
    echo -e "${GREEN}✅ Prerequisitos verificados${NC}"
}

# Configurar variables
setup_variables() {
    echo -e "${BLUE}🔧 Configurando variables...${NC}"
    
    if [ ! -f terraform/terraform.tfvars ]; then
        cp terraform/terraform.tfvars.example terraform/terraform.tfvars
        
        echo -e "${YELLOW}Configuración inicial creada.${NC}"
        echo -e "${YELLOW}Edita terraform/terraform.tfvars antes de continuar:${NC}"
        echo ""
        cat terraform/terraform.tfvars.example
        echo ""
        read -p "¿Editar ahora? (y/N): " edit_vars
        
        if [[ $edit_vars == [yY] ]]; then
            ${EDITOR:-nano} terraform/terraform.tfvars
        else
            echo -e "${RED}❌ Edita terraform/terraform.tfvars antes de continuar${NC}"
            exit 1
        fi
    fi
    
    echo -e "${GREEN}✅ Variables configuradas${NC}"
}

# Inicializar Terraform
init_terraform() {
    echo -e "${BLUE}🚀 Inicializando Terraform...${NC}"
    cd terraform
    terraform init
    cd ..
    echo -e "${GREEN}✅ Terraform inicializado${NC}"
}

# Planificar deployment
plan_terraform() {
    echo -e "${BLUE}📋 Generando plan de deployment...${NC}"
    cd terraform
    terraform plan
    cd ..
    echo -e "${GREEN}✅ Plan generado${NC}"
}

# Aplicar configuración
apply_terraform() {
    echo -e "${BLUE}🚀 Creando infraestructura AWS...${NC}"
    echo -e "${YELLOW}⚠️ Esto creará recursos en AWS (FREE TIER)${NC}"
    
    read -p "¿Continuar? (y/N): " confirm
    if [[ $confirm != [yY] ]]; then
        echo "Cancelado"
        exit 0
    fi
    
    cd terraform
    terraform apply
    cd ..
    
    echo -e "${GREEN}🎉 Infraestructura creada exitosamente${NC}"
    show_outputs
}

# Destruir infraestructura
destroy_terraform() {
    echo -e "${RED}🧹 DESTRUIR INFRAESTRUCTURA${NC}"
    echo -e "${RED}⚠️ ESTO ELIMINARÁ TODOS LOS RECURSOS AWS${NC}"
    
    read -p "¿Estás seguro? Escribe 'DESTROY' para confirmar: " confirm
    if [[ $confirm != "DESTROY" ]]; then
        echo "Cancelado"
        exit 0
    fi
    
    cd terraform
    terraform destroy
    cd ..
    
    echo -e "${GREEN}✅ Infraestructura eliminada${NC}"
}

# Mostrar outputs
show_outputs() {
    echo -e "${BLUE}📤 Información de la infraestructura:${NC}"
    cd terraform
    terraform output
    cd ..
}

# Conectar por SSH
ssh_connect() {
    echo -e "${BLUE}🔗 Conectando por SSH...${NC}"
    cd terraform
    EC2_IP=$(terraform output -raw ec2_public_ip 2>/dev/null || echo "")
    cd ..
    
    if [ -z "$EC2_IP" ]; then
        echo -e "${RED}❌ No se pudo obtener la IP de EC2${NC}"
        echo "¿La infraestructura está creada?"
        exit 1
    fi
    
    echo -e "${YELLOW}Conectando a: $EC2_IP${NC}"
    ssh -i ~/.ssh/id_rsa ec2-user@$EC2_IP
}

# Ver logs de aplicación
show_logs() {
    echo -e "${BLUE}📊 Logs de la aplicación...${NC}"
    cd terraform
    EC2_IP=$(terraform output -raw ec2_public_ip 2>/dev/null || echo "")
    cd ..
    
    if [ -z "$EC2_IP" ]; then
        echo -e "${RED}❌ No se pudo obtener la IP de EC2${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Conectando a: $EC2_IP${NC}"
    ssh -i ~/.ssh/id_rsa ec2-user@$EC2_IP "cd filosofia-app && docker-compose logs -f"
}

# Función principal
main() {
    case ${1:-help} in
        init)
            check_prerequisites
            setup_variables
            init_terraform
            ;;
        plan)
            check_prerequisites
            plan_terraform
            ;;
        apply)
            check_prerequisites
            setup_variables
            init_terraform
            apply_terraform
            ;;
        destroy)
            destroy_terraform
            ;;
        outputs)
            show_outputs
            ;;
        ssh)
            ssh_connect
            ;;
        logs)
            show_logs
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}❌ Opción no válida: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# Verificar si estamos en el directorio correcto
if [ ! -d "terraform" ]; then
    echo -e "${RED}❌ Directorio terraform no encontrado${NC}"
    echo "Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Ejecutar función principal
main "$@"
