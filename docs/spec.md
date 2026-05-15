# Hermes Business OS — Specification v1.0

## 1. Vision

Hermes Business OS es un sistema operativo de inteligencia artificial open source para pequeñas y medianas empresas (PYMES). Toma el cerebro de un experto, lo digitaliza en agentes especializados por departamento, y lo conecta con las herramientas que ya usa el negocio: Google Workspace, Telegram, calendarios, hojas de cálculo.

**No es una plataforma. Es un laboratorio que se instala.**

## 2. Problem Statement

Las PYMES latinoamericanas enfrentan:
- Sobrecarga laboral y burnout por tareas repetitivas
- Falta de documentación de procesos
- Dependencia de personas clave
- Herramientas de AI genéricas que no entienden su negocio
- Soluciones enterprise que cuestan miles de dólares

## 3. Solution

Hermes Business OS:
1. **Captura el conocimiento experto** del dueño/gerente
2. **Crea agentes especializados** por área (ventas, operaciones, finanzas, RRHH)
3. **Automatiza lo repetitivo** (reportes, seguimientos, documentos)
4. **Mantiene al humano como revisor** — nunca como esclavo de la máquina
5. **Funciona en celular** — el dueño manda audios, recibe resultados

## 4. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    HERMES BUSINESS OS                        │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Interface                                          │
│  ├── Telegram Bot (voz, texto, archivos)                    │
│  ├── Dashboard Web (control central)                        │
│  └── API REST (integraciones externas)                      │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: Agent Core (Hermes)                                │
│  ├── Context Router (enruta mensajes a skills)              │
│  ├── Memory System (memoria a largo plazo por cliente)      │
│  ├── Skill Engine (skills modulares por departamento)       │
│  └── Document Generator (Kami v3 → PDF/Docs/Slides)         │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: Business Logic                                     │
│  ├── Client OS (configuración por empresa)                  │
│  ├── Department Modules (ventas, ops, finanzas, rrhh)       │
│  └── Workflow Engine (pipelines de aprobación)              │
├─────────────────────────────────────────────────────────────┤
│  Layer 4: Integrations                                       │
│  ├── Google Workspace (Sheets, Docs, Slides, Drive)         │
│  ├── Calendar (Google Calendar)                             │
│  ├── Notifications (Telegram, Email)                        │
│  └── External APIs (Stripe, WhatsApp Business, etc.)        │
├─────────────────────────────────────────────────────────────┤
│  Layer 5: Infrastructure                                     │
│  ├── FastAPI Backend (Python)                               │
│  ├── PostgreSQL / SQLite (datos)                            │
│  ├── Redis (cache/sessions)                                 │
│  └── Docker / Docker Compose (deploy)                       │
└─────────────────────────────────────────────────────────────┘
```

## 5. Core Components

### 5.1 Client OS
Cada empresa tiene un `client.yaml` que define:
- Nombre, industria, tamaño
- Departamentos activos
- Integraciones configuradas
- Flujos de aprobación
- Plantillas de documentos

### 5.2 Department Skills
Módulos independientes que se activan según el negocio:

| Skill | Propósito | Ejemplo Eventos | Ejemplo Legal |
|-------|-----------|-----------------|---------------|
| ventas | CRM, cotizaciones, seguimiento | Cotización boda | Propuesta de honorarios |
| operaciones | Proyectos, tareas, logística | Montaje de evento | Gestión de juicios |
| finanzas | Pagos, presupuestos, reportes | Control de pagos cliente | Control de honorarios |
| rrhh | Nómina, asistencia, equipos | Staff por evento | Asociados por materia |
| inventario | Stock, proveedores, compras | Mobiliario decoración | Archivo documental |
| documentos | Generación de documentos | Contrato, timeline | Demanda, escrito |

### 5.3 Document Generator (Kami v3)
Motor de documentos basado en WeasyPrint:
- Templates HTML + CSS editorial
- Salida: PDF, Google Docs, Google Slides
- Templates base: one-pager, long-doc, letter, portfolio, slides

### 5.4 Context Router
Enruta mensajes del usuario al skill correcto:
- "Cotiza una boda para 100 personas" → skill:ventas
- "Genera la nómina del mes" → skill:rrhh
- "Haz el reporte semanal" → skill:operaciones

## 6. Data Model

### 6.1 Core Entities
```
Company (id, name, industry, config)
  └── Departments[]
        └── Workflows[]
              └── Tasks[]
  └── Clients[] (CRM)
  └── Projects[] (Operaciones)
  └── Documents[] (Generados)
  └── Users[] (Empleados/Asociados)
```

### 6.2 Event-Driven Lifecycle
Todo en el sistema sigue un ciclo de vida:
```
INTAKE → QUOTE → APPROVAL → PLANNING → EXECUTION → REVIEW → CLOSE
```

## 7. Integration Points

### 7.1 Google Workspace
- Sheets: Base de datos operativa (maestros + por-proyecto)
- Docs: Documentos generados editables
- Slides: Presentaciones automáticas
- Drive: Almacenamiento de archivos
- Calendar: Citas y recordatorios

### 7.2 Telegram
- Bot como interfaz principal
- Voz a texto para captura en campo
- Archivos (fotos, documentos)
- Notificaciones push

### 7.3 API REST
- Endpoints para cada departamento
- Webhooks para integraciones externas
- Autenticación JWT

## 8. Configuration

### 8.1 Per-Company Config (`config/client.yaml`)
```yaml
company:
  name: "Mi Empresa"
  industry: "retail"  # eventos | legal | retail | consultoria | ...
  size: "small"       # solopreneur | small | medium

departments:
  - name: "ventas"
    enabled: true
    skills:
      - cotizaciones
      - seguimiento
      - propuestas
  - name: "operaciones"
    enabled: true
    skills:
      - proyectos
      - tareas
      - calendario

integrations:
  google_workspace:
    enabled: true
    service_account: "google-service-account.json"
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"

templates:
  document_style: "professional"
  language: "es"
  currency: "MXN"
```

### 8.2 Environment Variables (`.env`)
```
# Core
HBM_API_KEY=your-api-key
HBM_DATABASE_URL=sqlite:///./data/business.db

# Integrations
TELEGRAM_BOT_TOKEN=your-bot-token
GOOGLE_SERVICE_ACCOUNT_JSON=google-service-account.json

# AI Models
OPENAI_API_KEY=your-openai-key
# o llama, claude, etc.
```

## 9. Deployment

### 9.1 Local (Development)
```bash
git clone https://github.com/ws-capital/hermes-business-os.git
cd hermes-business-os
cp .env.example .env
# Editar .env con tus credenciales
docker-compose up -d
```

### 9.2 Production (VPS/Cloud)
```bash
# 1. Clonar repo
# 2. Configurar .env
# 3. docker-compose -f docker-compose.prod.yml up -d
# 4. Configurar nginx/ssl
# 5. Configurar systemd service
```

## 10. Security

- Secrets en `.env` (nunca en repo)
- Service account JSON fuera de repo
- JWT para API auth
- Rate limiting en endpoints
- Validación de inputs

## 11. Extensibility

### 11.1 Adding a New Department
1. Crear `skills/<department>/SKILL.md`
2. Crear `backend/app/departments/<department>.py`
3. Registrar en `config/client.yaml`
4. Crear templates en `skills/<department>/templates/`

### 11.2 Adding a New Integration
1. Crear `backend/integrations/<service>.py`
2. Implementar interfaz base
3. Registrar en `config/integrations.yaml`

## 12. Success Metrics

- Tiempo de implementación: 2-4 semanas por empresa
- Reducción de carga administrativa: 60-80%
- Satisfacción del cliente: medida por feedback
- Documentos generados automáticamente: >90%

## 13. Roadmap

### v0.1.0 (MVP)
- Backend FastAPI base
- 3 departamentos: ventas, operaciones, documentos
- Google Workspace integration
- Telegram bot
- Document generator básico

### v0.2.0
- Dashboard web
- 2 departamentos más: finanzas, rrhh
- Workflow engine
- Multi-empresa

### v0.3.0
- Inventario
- Calendario avanzado
- Notificaciones multi-canal
- API pública documentada

### v1.0.0
- Marketplace de skills
- Mobile app
- Analytics avanzados
- Enterprise features

## 14. License

MIT License — Open Source para la comunidad.

## 15. Authors

WS Capital AI Lab — Pablo Narváez y equipo.
Inspirado en los sistemas operativos creados para Paola Meneses Decoración y Willow Narváez Legal.
