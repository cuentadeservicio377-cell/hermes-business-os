# Hermes Business OS — Plan Maestro v1.0

> **Objetivo**: Crear la distribución empresarial oficial de Hermes Agent. Tan pulida que Nous Research quiera adoptarla.

---

## Lecciones Aprendidas (Por qué fallaron los intentos anteriores)

| Intento | Error Crítico | Resultado |
|---------|--------------|-----------|
| `hermes-business-os` | Backend FastAPI SEPARADO con "skills" Python mock. NO usaba skills nativos de Hermes. | Dos sistemas que no se hablan. Duplicación total. |
| `hermes-os-empresarial` | Solo skills SKILL.md, sin frontend ni onboarding guiado. | Funcional pero incompleto para usuarios no técnicos. |
| `hermes-ws-business-os` | Fork COMPLETO de Hermes Agent (~50k líneas). | Imposible de mantener al día con Nous Research. |

**La regla de oro**: Hermes Business OS NO es un software separado. Es Hermes Agent + Skills Nativos + Dashboard + Onboarding. Nada más.

---

## Arquitectura Correcta

```
┌─────────────────────────────────────────────────────────────┐
│  CAPA 1: Hermes Agent (oficial Nous Research)               │
│  ├── AI Core, Memory, Gateway, CLI                          │
│  └── Se instala vía: curl -fsSL ... | bash                 │
├─────────────────────────────────────────────────────────────┤
│  CAPA 2: Skills de Negocio (este proyecto)                  │
│  ├── hermes-business-core/      ← Config, routing, GW       │
│  ├── hermes-ventas/             ← CRM, cotizaciones         │
│  ├── hermes-operaciones/        ← Proyectos, tareas         │
│  ├── hermes-documentos/         ← Kami v3, templates        │
│  ├── hermes-finanzas/           ← Presupuestos, pagos       │
│  └── hermes-rrhh/               ← Nómina, equipos           │
├─────────────────────────────────────────────────────────────┤
│  CAPA 3: Dashboard Web (Next.js 15)                         │
│  ├── Se comunica vía API de Hermes / webhooks               │
│  ├── Visualiza datos de Google Sheets                       │
│  └── Frontend personalizable por industria                  │
├─────────────────────────────────────────────────────────────┤
│  CAPA 4: Motor de Documentos (Python)                       │
│  ├── Kami v3: WeasyPrint → PDFs profesionales              │
│  ├── Google Docs/Slides API                                 │
│  └── Templates HTML/CSS por industria                       │
├─────────────────────────────────────────────────────────────┤
│  CAPA 5: Instalador & Onboarding                            │
│  ├── `hbos install` → configura todo automáticamente       │
│  ├── Wizard conversacional: "Cuéntame de tu empresa"       │
│  └── Genera `config/empresa.yaml` + estructura Drive        │
└─────────────────────────────────────────────────────────────┘
```

---

## Stack Tecnológico

| Componente | Tecnología | Justificación |
|------------|-----------|---------------|
| **Agent Core** | Hermes Agent oficial (Python) | No reinventar. Usar lo que Nous Research mantiene. |
| **Skills** | SKILL.md nativos + Python tools | Formato estándar de Hermes, portable a agentskills.io |
| **Dashboard** | Next.js 15 + React 19 + TypeScript + Tailwind + shadcn/ui | Moderno, rápido, fácil de personalizar por industria |
| **Document Engine** | Python + WeasyPrint | Kami v3 probado en producción (Legal Pro) |
| **Datos** | Google Sheets (maestros) + SQLite (local) | Las PYMES ya usan Sheets. No forzar nueva DB. |
| **Storage** | Google Drive API | Estructura de carpetas por cliente/proyecto |
| **Comunicación** | Telegram (primario) + Dashboard (secundario) | Voz en campo + visión en oficina |
| **Deploy** | Docker Compose / macOS nativo | Igual que Hermes oficial |

---

## Fases de Implementación

### FASE 1: Fundamentos (Semana 1-2)
- [ ] Estructura de directorios del proyecto
- [ ] Sistema de skills nativos compatible con Hermes Agent v0.12+
- [ ] Skill `hermes-business-core`: configuración, routing, Google Workspace
- [ ] Instalador CLI: `hbos install`, `hbos setup`, `hbos doctor`
- [ ] Configuración por empresa en YAML

### FASE 2: Departamentos Core (Semana 3-4)
- [ ] Skill `hermes-ventas`: intake, cotizaciones, pipeline
- [ ] Skill `hermes-operaciones`: proyectos, tareas, checklists
- [ ] Skill `hermes-documentos`: templates básicos, generación PDF
- [ ] Integración Google Sheets (índice maestro, catálogo de servicios)
- [ ] Integración Google Drive (estructura de carpetas)

### FASE 3: Dashboard Web (Semana 5-6)
- [ ] Next.js 15 app con autenticación
- [ ] Vista de clientes y pipeline
- [ ] Vista de proyectos y tareas
- [ ] Vista de documentos generados
- [ ] Configuración visual de empresa

### FASE 4: Onboarding Wizard (Semana 7)
- [ ] Flujo conversacional de bienvenida
- [ ] Extracción de datos de la empresa
- [ ] Configuración automática de Google Workspace
- [ ] Generación de templates base por industria
- [ ] Tutorial interactivo primer uso

### FASE 5: Document Engine & Templates (Semana 8)
- [ ] Motor Kami v3 integrado
- [ ] Templates por industria: eventos, legal, retail, consultoría
- [ ] Variables dinámicas: `{{cliente.nombre}}`, `{{empresa.nombre}}`
- [ ] Exportación: PDF, Google Docs, Google Slides

### FASE 6: Finanzas + RRHH (Semana 9-10)
- [ ] Skill `hermes-finanzas`: presupuestos, pagos, reportes
- [ ] Skill `hermes-rrhh`: nómina, asistencia, equipos
- [ ] Alertas automáticas de vencimientos

### FASE 7: Polish & Packaging (Semana 11-12)
- [ ] Testing end-to-end
- [ ] Documentación completa
- [ ] Video de demo
- [ ] Publicación en GitHub con README profesional
- [ ] Propuesta a Nous Research

---

## Estructura de Directorios

```
hermes-business-os/
├── README.md
├── PLAN.md                    ← Este archivo
├── CHANGELOG.md
├── LICENSE
│
├── installer/                 ← Instalador CLI
│   ├── hbos.py               ← Entry point
│   ├── install.py            ← Lógica de instalación
│   ├── setup_wizard.py       ← Onboarding conversacional
│   └── doctor.py             ← Diagnóstico
│
├── skills/                    ← Skills nativos de Hermes
│   ├── hermes-business-core/
│   │   ├── SKILL.md
│   │   └── tools/
│   │       ├── config_loader.py
│   │       ├── google_workspace.py
│   │       └── router.py
│   ├── hermes-ventas/
│   │   ├── SKILL.md
│   │   └── tools/
│   │       ├── crm.py
│   │       ├── cotizador.py
│   │       └── pipeline.py
│   ├── hermes-operaciones/
│   │   ├── SKILL.md
│   │   └── tools/
│   │       ├── proyectos.py
│   │       ├── tareas.py
│   │       └── checklists.py
│   ├── hermes-documentos/
│   │   ├── SKILL.md
│   │   └── tools/
│   │       ├── kami_engine.py
│   │       ├── templates/
│   │       └── variables.py
│   ├── hermes-finanzas/
│   │   ├── SKILL.md
│   │   └── tools/
│   └── hermes-rrhh/
│       ├── SKILL.md
│       └── tools/
│
├── dashboard/                 ← Frontend Next.js 15
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── styles/
│   └── package.json
│
├── config/
│   ├── empresa.yaml.example
│   └── industrias/
│       ├── eventos.yaml
│       ├── legal.yaml
│       ├── retail.yaml
│       └── consultoria.yaml
│
├── docs/
│   ├── INSTALL.md
│   ├── USER-GUIDE.md
│   ├── ADMIN-GUIDE.md
│   └── API.md
│
├── scripts/
│   ├── install.sh
│   ├── update.sh
│   └── test.sh
│
└── docker/
    ├── Dockerfile
    └── docker-compose.yml
```

---

## Métricas de Éxito

| Métrica | Objetivo |
|---------|----------|
| Instalación | < 5 minutos desde cero |
| Onboarding | < 15 minutos para configurar empresa |
| Reducción admin | 60-80% en tareas repetitivas |
| Documentos auto | > 90% generados sin intervención |
| Satisfacción | NPS > 50 de emprendedores |
| Estrellas GitHub | 1,000+ en primer mes |

---

## Próximo Paso

**FASE 1: Fundamentos**

Comenzar creando la estructura base, el instalador CLI, y el skill `hermes-business-core` con integración a Google Workspace.

---

*Documento vivo. Se actualiza al final de cada fase.*
