# Instalación de Hermes Business OS

## Requisitos

- **macOS** o **Linux** (Windows con WSL2)
- **Python 3.11+**
- **Hermes Agent** instalado
- **Cuenta de Google Workspace** (opcional, recomendado)
- **Bot de Telegram** (via @BotFather)

---

## Instalación Rápida (5 minutos)

### Paso 1: Instalar Hermes Agent

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Reinicia tu terminal o ejecuta:
```bash
source ~/.bashrc  # o ~/.zshrc
```

Verifica:
```bash
hermes --version
```

### Paso 2: Instalar Hermes Business OS

```bash
curl -fsSL https://raw.githubusercontent.com/cuentadeservicio377-cell/hermes-business-os/main/scripts/install.sh | bash
```

### Paso 3: Configurar tu empresa

```bash
hbos setup
```

Sigue el wizard interactivo. Te preguntará:
- Nombre de tu empresa
- Industria
- Tamaño del equipo
- Moneda
- Departamentos a activar

### Paso 4: Configurar Google Workspace (opcional pero recomendado)

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto nuevo
3. Habilita las APIs: Sheets, Drive, Docs, Calendar
4. Crea una cuenta de servicio y descarga el JSON
5. Mueve el JSON a: `config/google-service-account.json`
6. Comparte tus Sheets/Drive con el email de la cuenta de servicio

### Paso 5: Configurar Telegram

1. Abre Telegram y busca @BotFather
2. Crea un nuevo bot con `/newbot`
3. Copia el token
4. Configura Hermes:
```bash
hermes gateway setup
```

### Paso 6: Iniciar

```bash
hermes gateway start
```

Abre Telegram y envía `/start` a tu bot.

---

## Instalación Manual (Desarrollo)

```bash
# 1. Clonar repo
git clone https://github.com/cuentadeservicio377-cell/hermes-business-os.git
cd hermes-business-os

# 2. Instalar skills
hbos install --path .

# 3. Configurar
cp config/empresa.yaml.example config/empresa.yaml
# Edita config/empresa.yaml con tus datos

# 4. Instalar dependencias Python
pip install pyyaml google-api-python-client google-auth-httplib2 google-auth-oauthlib weasyprint

# 5. Iniciar
hermes gateway start
```

---

## Verificación

```bash
hbos doctor
```

Esto verifica:
- ✅ Hermes Agent instalado
- ✅ Skills instalados
- ✅ Configuración presente
- ✅ Dependencias Python
- ✅ Google Workspace (opcional)

---

## Actualización

```bash
hbos update
```

O manualmente:
```bash
cd ~/.hermes-business-os
git pull origin main
hbos install
```

---

## Desinstalación

```bash
# Eliminar skills de Hermes
rm -rf ~/.hermes/skills/hermes-*

# Eliminar HBOS
rm -rf ~/.hermes-business-os
rm ~/.local/bin/hbos
```

---

## Solución de Problemas

### "Hermes Agent not found"

Instala Hermes primero:
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc
```

### "Python dependencies missing"

```bash
pip install --user pyyaml google-api-python-client google-auth-httplib2 google-auth-oauthlib weasyprint
```

### "Google Workspace not working"

1. Verifica que el archivo JSON de cuenta de servicio existe
2. Asegúrate de haber compartido los Sheets/Drive con el email de la cuenta
3. Verifica que las APIs estén habilitadas en Google Cloud Console

### "Skills not loading"

```bash
hbos install
hermes config set skills.auto_load true
```

---

## Soporte

- 📖 Documentación: [docs/USER-GUIDE.md](USER-GUIDE.md)
- 🐛 Issues: GitHub Issues
- 💬 Comunidad: Discord de Hermes Agent
