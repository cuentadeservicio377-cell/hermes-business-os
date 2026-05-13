# Hermes Business OS — Quickstart Guide

## ¿Qué es Hermes Business OS?

Es tu socio operativo de inteligencia artificial. Un sistema que se instala en tu empresa, aprende cómo trabajas, y automatiza lo repetitivo para que tú te enfoques en lo importante.

**No necesitas saber de tecnología.** Si usas WhatsApp y Google, ya sabes enough.

## Requisitos Previos

- Una computadora o servidor (VPS) con Linux
- Docker instalado (te ayudamos)
- Una cuenta de Google Workspace
- Un bot de Telegram (te decimos cómo crearlo)

## Instalación en 5 Pasos

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/ws-capital/hermes-business-os.git
cd hermes-business-os
```

### Paso 2: Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus datos:

```
# Nombre de tu empresa
HBM_COMPANY_NAME="Mi Empresa"
HBM_COMPANY_INDUSTRY="retail"

# Telegram (crea tu bot con @BotFather)
TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."

# Google Workspace (descarga service account JSON)
GOOGLE_SERVICE_ACCOUNT_JSON="google-service-account.json"

# Base de datos (SQLite por defecto, PostgreSQL opcional)
DATABASE_URL="sqlite:///./data/business.db"
```

### Paso 3: Configurar tu empresa

```bash
cp config/client.yaml.example config/client.yaml
```

Edita `config/client.yaml`:

```yaml
company:
  name: "Mi Empresa"
  industry: "retail"  # retail | eventos | legal | consultoria | ...
  size: "small"       # solopreneur | small | medium

departments:
  - name: "ventas"
    enabled: true
    skills:
      - cotizaciones
      - seguimiento
  - name: "operaciones"
    enabled: true
    skills:
      - proyectos
      - tareas

templates:
  document_style: "professional"
  language: "es"
  currency: "MXN"
```

### Paso 4: Levantar el sistema

```bash
docker-compose up -d
```

Esto levanta:
- Backend API en http://localhost:8000
- Base de datos
- Bot de Telegram

### Paso 5: Verificar que funciona

```bash
curl http://localhost:8000/health
```

Deberías ver:
```json
{"status": "ok", "version": "0.1.0"}
```

## Primeros Pasos

### 1. Habla con tu agente en Telegram

Envía `/start` a tu bot. Te dará la bienvenida y te preguntará qué necesitas.

### 2. Crea tu primer cliente

Dile a tu agente:
> "Registra un cliente nuevo: Juan Pérez, juan@email.com, tel 555-1234"

### 3. Crea tu primera cotización

> "Cotiza 10 horas de consultoría para Juan Pérez a $500/hora"

Tu agente generará un PDF y te lo enviará.

### 4. Revisa tu dashboard

Abre http://localhost:8000/docs para ver la documentación de la API.

## Estructura de Skills

Cada departamento es un skill que puedes activar o desactivar:

| Skill | Qué hace | Ejemplo de uso |
|-------|----------|----------------|
| **ventas** | Clientes, cotizaciones, seguimiento | "Cotiza un proyecto de $10,000" |
| **operaciones** | Proyectos, tareas, calendario | "Crea proyecto 'Website Cliente X'" |
| **finanzas** | Pagos, presupuestos, reportes | "Genera reporte mensual" |
| **rrhh** | Nómina, asistencia, equipos | "Calcula nómina del mes" |
| **inventario** | Stock, proveedores, compras | "Revisa stock de laptops" |
| **documentos** | Contratos, cartas, reportes | "Genera contrato de servicios" |

## Personalización

### Agregar un departamento nuevo

1. Crea `skills/midepartamento/SKILL.md`
2. Define las acciones que puede hacer
3. Registra en `config/client.yaml`

### Cambiar templates de documentos

1. Edita `skills/documentos/templates/`
2. Usa variables: `{{client.name}}`, `{{company.name}}`, etc.
3. Recarga config: `docker-compose restart`

### Conectar otras herramientas

Hermes usa un sistema de integraciones. Para agregar una nueva:

1. Crea `backend/integrations/miservicio.py`
2. Implementa la interfaz base
3. Registra en `config/integrations.yaml`

## Troubleshooting

### El bot no responde
- Verifica `TELEGRAM_BOT_TOKEN` en `.env`
- Revisa logs: `docker-compose logs bot`

### No puedo conectar Google Workspace
- Verifica que el service account JSON existe
- Asegúrate de compartir las hojas con el email del service account

### Error al generar PDFs
- WeasyPrint necesita librerías GTK: `apt-get install libgtk-3-0`

## Soporte

- Documentación completa: `/docs`
- Issues: GitHub Issues
- Comunidad: Discord (próximamente)

## Próximos Pasos

1. Explora los ejemplos en `/examples`
2. Lee `docs/architecture.md` para entender el sistema
3. Contribuye: `CONTRIBUTING.md`

---

**Hecho con ❤️ por WS Capital AI Lab**
