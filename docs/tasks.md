# Hermes Business OS — Tasks Detail

## Fase 1: Fundación

### F1.1 Crear estructura de directorios
**Asignado:** wsimplementer
**Dependencias:** Ninguna
**Evidencia:** `tree /root/ws-capital/hermes-business-os`

Estructura objetivo:
```
hermes-business-os/
├── docs/                    # Documentación
│   ├── spec.md
│   ├── plan.md
│   ├── tasks.md
│   ├── quickstart.md
│   └── architecture.md
├── backend/                 # FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── deps.py
│   │   └── departments/
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── integrations/
│   │   ├── google_workspace.py
│   │   └── telegram.py
│   ├── models/
│   │   ├── company.py
│   │   ├── client.py
│   │   ├── project.py
│   │   └── document.py
│   └── utils/
│       ├── templates.py
│       └── helpers.py
├── frontend/                # Dashboard (futuro)
├── skills/                  # Skills modulares
│   ├── ventas/
│   ├── operaciones/
│   ├── finanzas/
│   ├── rrhh/
│   ├── inventario/
│   └── documentos/
├── config/                  # Configuración
│   ├── client.yaml.example
│   └── integrations.yaml
├── docker/                  # Docker configs
│   ├── Dockerfile
│   └── docker-compose.yml
├── scripts/                 # Utilidades
│   ├── setup.sh
│   └── migrate.sh
├── paper/                   # Paper de investigación
│   └── research-paper.md
├── examples/                # Ejemplos por industria
│   ├── eventos/
│   ├── legal/
│   ├── retail/
│   └── consultoria/
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

### F1.2 Generar spec.md
**Asignado:** wsspecarchitect
**Dependencias:** F1.1
**Evidencia:** Archivo spec.md completo

### F1.3 Generar plan.md
**Asignado:** wsspecarchitect
**Dependencias:** F1.2
**Evidencia:** Archivo plan.md con fases y milestones

### F1.4 Generar tasks.md
**Asignado:** wsspecarchitect
**Dependencias:** F1.3
**Evidencia:** Archivo tasks.md (este documento)

### F1.5 Generar quickstart.md
**Asignado:** wsspecarchitect
**Dependencias:** F1.4
**Evidencia:** Developer nuevo instala en <30 min

Contenido mínimo:
- Requisitos previos (Docker, Python 3.10+)
- Instalación paso a paso
- Configuración de .env
- Primeros pasos (crear empresa, agregar departamento)
- Troubleshooting común

### F1.6 Generar research-paper.md
**Asignado:** wsspecarchitect
**Dependencias:** F1.5
**Evidencia:** Paper completo, listo para PDF

## Fase 2: Implementación Core

### F2.1 Backend FastAPI base
**Asignado:** wsimplementer
**Dependencias:** F1.6
**Evidencia:** `curl http://localhost:8000/health` → `{"status":"ok"}`

Requisitos:
- FastAPI con auto-docs (/docs)
- Estructura modular (routers, services, models)
- Configuración desde .env y YAML
- Logging estructurado
- Manejo de errores consistente

### F2.2 Sistema de skills modular
**Asignado:** wsimplementer
**Dependencias:** F2.1
**Evidencia:** Nuevo skill funciona con 3 líneas de registro

Requisitos:
- Clase base `BaseSkill`
- Registro automático desde `skills/<dept>/`
- Cada skill expone: name, description, actions[], handler()
- Router FastAPI auto-generado por skill

### F2.3 Templates Kami v3
**Asignado:** wsimplementer
**Dependencias:** F2.2
**Evidencia:** Genera PDF desde template HTML con datos de prueba

Requisitos:
- WeasyPrint para PDF
- Templates HTML + CSS en `skills/<dept>/templates/`
- Variables templating (Jinja2)
- Output: PDF, Google Docs, Google Slides

### F2.4 Google Workspace integration
**Asignado:** wsimplementer
**Dependencias:** F2.3
**Evidencia:** Lee hoja de Sheets, crea Doc, sube a Drive

Requisitos:
- Service account auth
- Sheets: read/write ranges
- Docs: create from template
- Drive: upload/download
- Slides: create presentation

### F2.5 Config de Hermes genérica
**Asignado:** wsimplementer
**Dependencias:** F2.4
**Evidencia:** Cambiar `industry` en client.yaml cambia comportamiento

Requisitos:
- `config/client.yaml` define empresa completa
- Validación con Pydantic
- Hot-reload de config (sin restart)
- Herencia de defaults

### F2.6 Docker/docker-compose
**Asignado:** wsimplementer
**Dependencias:** F2.5
**Evidencia:** `docker-compose up -d` levanta todo funcional

Requisitos:
- Dockerfile multi-stage
- docker-compose.yml con: app, db, redis
- docker-compose.prod.yml con: nginx, ssl
- Volumes para datos persistentes
- Healthchecks

### F2.7 Telegram bot base
**Asignado:** wsimplementer
**Dependencias:** F2.6
**Evidencia:** Bot responde /start y reenvía mensajes al backend

Requisitos:
- python-telegram-bot o aiogram
- Webhook o polling
- Voice-to-text (whisper local o API)
- File handling (photos, docs)
- Context routing al skill correcto

### F2.8 Department: Ventas
**Asignado:** wsimplementer
**Dependencias:** F2.7
**Evidencia:** Crea cotización, guarda en Sheets, genera PDF

Requisitos:
- CRUD clientes
- CRUD cotizaciones
- Generar propuesta (PDF/Slides)
- Seguimiento de estados
- Pipeline: lead → quote → negotiation → won/lost

### F2.9 Department: Operaciones
**Asignado:** wsimplementer
**Dependencias:** F2.8
**Evidencia:** Crea proyecto, asigna tareas, genera timeline

Requisitos:
- CRUD proyectos
- CRUD tareas
- Asignación de recursos
- Timeline/Gantt básico
- Checklists por proyecto

### F2.10 Department: Documentos
**Asignado:** wsimplementer
**Dependencias:** F2.9
**Evidencia:** Genera documento desde template con datos de empresa

Requisitos:
- Templates por tipo (contrato, carta, reporte)
- Variables: {{company.name}}, {{client.name}}, etc.
- Output: PDF, Google Doc
- Firma digital (futuro)

## Fase 3: QA

### F3.1 Probar instalación desde cero
**Asignado:** wsqaauditor
**Dependencias:** F2.10
**Evidencia:** VPS limpio con sistema funcionando

Pasos:
1. VPS nuevo (Ubuntu 22.04)
2. Instalar Docker
3. Clonar repo
4. Copiar .env.example → .env
5. docker-compose up -d
6. Verificar /health
7. Verificar Telegram bot responde

### F3.2 Verificar agente externo puede configurar
**Asignado:** wsqaauditor
**Dependencias:** F3.1
**Evidencia:** Otro AI (OpenCode, Codex, otro Hermes) logra deploy

Pasos:
1. Dar quickstart.md a agente externo
2. Verificar que completa instalación
3. Verificar que configura empresa de prueba
4. Documentar gaps en instrucciones

### F3.3 Revisar documentación completa
**Asignado:** wsqaauditor
**Dependencias:** F3.2
**Evidencia:** Checklist de documentación completo

Verificar:
- [ ] README.md claro y completo
- [ ] quickstart.md funciona
- [ ] spec.md actualizado
- [ ] Todos los .md sin typos graves
- [ ] Código comentado donde es necesario

### F3.4 Security audit
**Asignado:** wsqaauditor
**Dependencias:** F3.3
**Evidencia:** No secrets expuestos

Verificar:
- [ ] .env en .gitignore
- [ ] No API keys en código
- [ ] No passwords hardcodeados
- [ ] Service account JSON fuera de repo
- [ ] JWT secrets en .env

### F3.5 Performance test
**Asignado:** wsqaauditor
**Dependencias:** F3.4
**Evidencia:** <2s respuesta API en local

Pruebas:
- [ ] /health < 100ms
- [ ] CRUD cliente < 500ms
- [ ] Generar documento < 2s
- [ ] 10 requests concurrentes sin errores

## Fase 4: Deploy

### F4.1 Crear repo GitHub público
**Asignado:** wsimplementer
**Dependencias:** F3.5
**Evidencia:** URL pública accesible

Requisitos:
- README.md profesional
- LICENSE (MIT)
- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- .github/ISSUE_TEMPLATE/

### F4.2 Publicar release v0.1.0
**Asignado:** wsimplementer
**Dependencias:** F4.1
**Evidencia:** Tag v0.1.0 con release notes

Release notes:
- Features incluidos
- Known issues
- Roadmap próximo

### F4.3 Entregar paper de investigación
**Asignado:** wsspecarchitect
**Dependencias:** F4.2
**Evidencia:** PDF profesional

Requisitos:
- Formato académico/profesional
- Abstract, introducción, metodología, resultados, conclusiones
- Citas relevantes
- Gráficos/diagramas

### F4.4 Handoff completo
**Asignado:** Neo
**Dependencias:** F4.3
**Evidencia:** Pablo confirma que tiene todo

Entregables:
- [ ] Repo GitHub público
- [ ] Release v0.1.0
- [ ] Paper PDF
- [ ] Documentación completa
- [ ] Próximos pasos claros
