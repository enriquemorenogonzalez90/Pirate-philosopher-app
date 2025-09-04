# 🚀 GCP Setup Instructions - Step by Step

## Pre-requisitos

### 1. **Instalar Google Cloud CLI**
```bash
# En Linux/Ubuntu
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Verificar instalación
gcloud --version
```

### 2. **Tener cuenta Google con tarjeta de crédito**
- Necesaria para verificación (no se cobrará con Free Tier)
- $300 de crédito gratis para nuevos usuarios

## Paso a Paso Seguro

### **Paso 1: Configurar variables locales**

1. **Edita el archivo `.env.gcp-setup`**:
   ```bash
   nano .env.gcp-setup
   ```

2. **Solo necesitas cambiar esta línea** (después de crear el proyecto):
   ```bash
   export GCP_BILLING_ACCOUNT_ID="your-billing-account-id-here"
   ```
   Los demás valores ya están configurados correctamente.

### **Paso 2: Ejecutar setup automático**

1. **Ejecuta el script seguro**:
   ```bash
   ./setup-gcp.sh
   ```

2. **El script hará automáticamente**:
   - ✅ Verificar que gcloud esté instalado
   - ✅ Login a tu cuenta Google (si no estás logueado)
   - ✅ Crear proyecto `filosofia-app-serverless`
   - ✅ Mostrar tus billing accounts disponibles
   - ⏸️  **SE PAUSARÁ** para que copies tu Billing Account ID

3. **Cuando se pause**, verás algo así:
   ```
   Available billing accounts:
   ACCOUNT_ID              NAME
   01A234-567890-BCDEF1    My Billing Account
   ```
   
4. **Copia el ACCOUNT_ID** y actualiza `.env.gcp-setup`:
   ```bash
   export GCP_BILLING_ACCOUNT_ID="01A234-567890-BCDEF1"
   ```

5. **Ejecuta de nuevo**:
   ```bash
   ./setup-gcp.sh
   ```

### **Paso 3: Setup automático continuará**
- ✅ Enlazar billing account
- ✅ Habilitar APIs necesarias
- ✅ Crear service account para Terraform
- ✅ Asignar permisos IAM
- ✅ Generar credenciales seguras
- ✅ Crear bucket para Terraform state

### **Paso 4: Copiar credenciales para GitHub**

El script al final mostrará:
```
Copy this content to GitHub Secrets as 'GCP_SERVICE_ACCOUNT_KEY':
====== START COPYING FROM HERE ======
{
  "type": "service_account",
  "project_id": "filosofia-app-serverless",
  ...
}
====== END COPYING HERE ======
```

## Configuración GitHub Secrets

### 1. **Ve a tu repositorio en GitHub**
   - Settings → Secrets and variables → Actions

### 2. **Crear nuevo secret**
   - Name: `GCP_SERVICE_ACCOUNT_KEY`
   - Value: Pega el contenido JSON completo

### 3. **Verificar secret**
   - Debe aparecer como "GCP_SERVICE_ACCOUNT_KEY" en la lista

## Seguridad Garantizada 🔐

### ✅ **Lo que SÍ está protegido:**
- Credenciales guardadas localmente en `~/.config/gcloud/`
- Archivos `.env.gcp-setup` y `*.json` están en `.gitignore`
- Service account con permisos mínimos necesarios
- Bucket de Terraform con versionado habilitado

### ❌ **Lo que NUNCA se commitea:**
- Claves JSON
- Billing account IDs
- Credenciales de autenticación
- Variables de entorno sensibles

## Verificar Setup

### **Test de conectividad:**
```bash
# Verificar autenticación
gcloud auth list

# Verificar proyecto
gcloud config get-value project

# Verificar APIs habilitadas
gcloud services list --enabled
```

### **Test de Terraform:**
```bash
cd terraform-gcp/
terraform init
terraform plan -var="project_id=filosofia-app-serverless"
```

## Troubleshooting

### **Error: "gcloud command not found"**
```bash
# Instalar gcloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### **Error: "Billing account not found"**
1. Ve a [GCP Billing Console](https://console.cloud.google.com/billing)
2. Copia el ID correcto de tu billing account
3. Actualiza `.env.gcp-setup`

### **Error: "Permission denied"**
```bash
# Hacer script ejecutable
chmod +x setup-gcp.sh
```

### **Error: "Service account already exists"**
- Normal, el script detecta recursos existentes
- Continúa sin problemas

## Costos Esperados

- **Setup**: $0 (todo en Free Tier)
- **Funcionamiento**: €0-3/mes
- **Free Tier**: 2M requests/mes + 1GB Firestore

---

## 📞 ¿Necesitas ayuda?

Si algo falla, comparte el error y te ayudo a resolverlo paso a paso.