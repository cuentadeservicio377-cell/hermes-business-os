# Hermes Business OS

> **Tu socio operativo de inteligencia artificial.**
> Un sistema open source que se instala en tu empresa, aprende cómo trabajas, y automatiza lo repetitivo.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-00a393.svg)](https://fastapi.tiangolo.com)

---

## ¿Qué es Hermes Business OS?

Hermes Business OS es un **sistema operativo de inteligencia artificial** diseñado para pequeñas y medianas empresas (PYMES). A diferencia de las plataformas SaaS genéricas, Hermes:

- **Se adapta a TU negocio** — No al revés
- **Funciona en tu celular** — Voz y texto por Telegram
- **Automatiza lo repetitivo** — Tú revisas, la máquina ejecuta
- **Es open source** — Tu código, tu control, sin vendor lock-in
- **Cuesta menos de $3,000 USD** — Implementación completa en 12 semanas

### Casos de uso reales

| Industria | Antes | Después |
|-----------|-------|---------|
| **Eventos** | 2-3 horas por cotización | 15 minutos |
| **Legal** | Redacción manual de escritos | 70% más rápido |
| **Retail** | Inventario en Excel disperso | Control centralizado |
| **Consultoría** | Propuestas desde cero | Templates auto-generados |

---

## 🚀 Instalación rápida (5 minutos)

### Requisitos

- Docker y Docker Compose
- Cuenta de Google Workspace
- Bot de Telegram (crear con [@BotFather](https://t.me/BotFather))

### Pasos

```bash
# 1. Clonar
git clone https://github.com/ws-capital/hermes-business-os.git
cd hermes-business-os

# 2. Configurar
cp .env.example .env
cp config/client.yaml.example config/client.yaml
# Editar .env y config/client.yaml con tus datos

# 3. Levantar
docker-compose -f docker/docker-compose.yml up -d

# 4. Verificar
curl http://localhost:8000/api/v1/health
```

**Listo.** Tu asistente está en http://localhost:8000 y en Telegram.

📖 [Guía completa de instalación](docs/quickstart.md)

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────┐
│  Interface Layer                        │
│  ├── Telegram Bot (voz, texto)         │
│  ├── Dashboard Web (próximamente)      │
│  └── API REST (/docs)                   │
├─────────────────────────────────────────┤
│  Agent Core (Hermes)                    │
│  ├── Context Router                     │
│  ├── Memory System                      │
│  ├── Skill Engine                       │
│  └── Document Generator (Kami v3)       │
├─────────────────────────────────────────┤
│  Business Logic                         │
│  ├── Client OS (config por empresa)     │
│  ├── Department Skills                  │
│  └── Workflow Engine                    │
├─────────────────────────────────────────┤
│  Integrations                           │
│  ├── Google Workspace                   │
│  ├── Telegram                           │
│  └── External APIs                      │
└─────────────────────────────────────────┘
```

---

## 📦 Skills incluidos

Cada departamento es un skill independiente que puedes activar o desactivar:

| Skill | Qué hace | Estado |
|-------|----------|--------|
| **ventas** | CRM, cotizaciones, propuestas, seguimiento | ✅ v0.1 |
| **operaciones** | Proyectos, tareas, timelines, checklists | ✅ v0.1 |
| **documentos** | PDFs, Google Docs, Google Slides | ✅ v0.1 |
| **finanzas** | Presupuestos, reportes, pagos | 🚧 v0.2 |
| **rrhh** | Nómina, asistencia, equipos | 🚧 v0.2 |
| **inventario** | Stock, proveedores, compras | 🚧 v0.2 |

---

## 🛠️ Para desarrolladores

### Estructura del proyecto

```
hermes-business-os/
├── backend/          # FastAPI + SQLAlchemy
├── frontend/         # Dashboard (próximamente)
├── skills/           # Skills modulares por departamento
├── config/           # Configuración por empresa
├── docker/           # Docker + docker-compose
├── docs/             # Documentación
├── paper/            # Paper de investigación
└── examples/         # Ejemplos por industria
```

### Agregar un nuevo skill

```python
# skills/midepartamento/skill.py
from app.skills.base import BaseSkill, action

class MiDepartamentoSkill(BaseSkill):
    name = "midepartamento"
    description = "Mi nuevo departamento"
    
    def _register_actions(self):
        return {
            "mi_accion": self.mi_accion,
        }
    
    @action("Descripción de la acción")
    def mi_accion(self, parametro: str):
        return {"resultado": f"Hola {parametro}"}
```

Registra en `config/client.yaml`:
```yaml
departments:
  - name: "midepartamento"
    enabled: true
    skills:
      - mi_accion
```

---

## 📄 Paper de investigación

Este proyecto incluye un paper académico sobre la adopción digital de PYMES mediante IA:

📄 [Adopción Digital de Pequeñas y Medianas Empresas mediante Sistemas de IA Open Source](paper/research-paper.md)

**Hallazgos clave:**
- Reducción de carga administrativa: **60-80%**
- Tiempo de implementación: **12 semanas**
- Satisfacción del equipo (NPS): **+27 puntos**
- Documentos generados automáticamente: **>90%**

---

## 🤝 Contribuir

¡Bienvenidas las contribuciones! Lee [CONTRIBUTING.md](CONTRIBUTING.md) para empezar.

### Áreas donde necesitamos ayuda

- 🎨 Dashboard web (React/Vue)
- 🗣️ Transcripción de voz (Whisper integration)
- 📱 App móvil
- 🌍 Traducciones
- 📊 Más skills por industria

---

## 📜 Licencia

MIT License — Libre para usar, modificar y distribuir.

---

## 🙏 Agradecimientos

- **Paola Meneses Decoración** — Primer caso de estudio, sector eventos
- **Willow Narváez Legal** — Caso de estudio legal
- **Comunidad Hermes** — Framework base open source
- **WS Capital AI Lab** — Desarrollo y metodología

---

<p align="center">
  <strong>Hecho con ❤️ en Latinoamérica</strong><br>
  <em>El humano piensa. La máquina ejecuta. El humano revisa. La máquina aprende.</em>
</p>
