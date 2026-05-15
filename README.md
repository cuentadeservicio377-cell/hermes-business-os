# Hermes Business OS

> **Tu socio operativo de inteligencia artificial.**
> Una distribución de Hermes Agent diseñada para transformar a pequeñas y medianas empresas.

[![Hermes Agent](https://img.shields.io/badge/Powered%20by-Hermes%20Agent-blue)](https://github.com/NousResearch/hermes-agent)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ¿Qué es?

Hermes Business OS es una **distribución de skills** para [Hermes Agent](https://github.com/NousResearch/hermes-agent) (Nous Research) que convierte al agente de IA en el **socio operativo** de tu empresa.

No es un software separado. Es Hermes mismo, con superpoderes de negocio:

- 🏢 **Configuración por empresa** — Hermes entiende TU negocio
- 💬 **Conversación natural** — Habla por Telegram como con un socio
- 📄 **Documentos automáticos** — Cotizaciones, contratos, reportes
- 📊 **Google Workspace integrado** — Sheets, Docs, Drive, Calendar
- 🧠 **Memoria persistente** — Recuerda cada cliente, cada proyecto
- 🎨 **Dashboard web** — Visualiza tu negocio en tiempo real

---

## Instalación Rápida (5 minutos)

```bash
# 1. Instalar Hermes Agent (si no lo tienes)
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 2. Instalar Hermes Business OS
curl -fsSL https://raw.githubusercontent.com/cuentadeservicio377-cell/hermes-business-os/main/scripts/install.sh | bash

# 3. Configurar tu empresa
hbos setup

# 4. Iniciar
hermes gateway start
```

**Listo.** Habla con tu agente por Telegram.

📖 [Guía completa de instalación](docs/INSTALL.md)

---

## Skills Incluidos

| Skill | Qué hace | Estado |
|-------|---------|--------|
| **hermes-business-core** | Configuración, routing, Google Workspace | ✅ |
| **hermes-ventas** | CRM, cotizaciones, propuestas, seguimiento | ✅ |
| **hermes-operaciones** | Proyectos, tareas, checklists, timelines | ✅ |
| **hermes-documentos** | Documentos con templates, PDFs, Google Docs/Slides | ✅ |
| **hermes-finanzas** | Presupuestos, pagos, reportes, flujo de caja | ✅ |
| **hermes-rrhh** | Nómina, equipos, asistencia | ✅ |

---

## Ejemplo de Conversación

> **Tú:** "Registré un cliente nuevo: Juan Pérez, quiere una boda para 100 personas"
>
> **Hermes:** "Listo. Juan Pérez registrado como prospecto. ¿Cuándo es el evento y qué presupuesto maneja?"
>
> **Tú:** "15 de octubre, alrededor de 250 mil pesos"
>
> **Hermes:** "Perfecto. Generando cotización con paquete intermedio... Listo: [link a Google Slides]. Total: $250,000 MXN. ¿La apruebas?"

---

## Arquitectura

```
Hermes Agent (oficial Nous Research)
├── Core: AIAgent, conversation loop, memory, tools
├── Gateway: Telegram, Discord, Slack
├── Skills Nativos
└── HERMES BUSINESS OS (este repo)
    ├── hermes-business-core
    ├── hermes-ventas
    ├── hermes-operaciones
    ├── hermes-documentos
    ├── hermes-finanzas
    └── hermes-rrhh
```

---

## Dashboard Web

Accede a tu negocio visualmente:

```bash
cd dashboard
npm install
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000)

---

## Documentación

- [📖 Instalación](docs/INSTALL.md)
- [👤 Guía de Usuario](docs/USER-GUIDE.md)
- [⚙️ Guía de Admin](docs/ADMIN-GUIDE.md)
- [🔌 API Reference](docs/API.md)
- [📝 Changelog](CHANGELOG.md)
- [🤝 Contributing](CONTRIBUTING.md)

---

## Para quién es

- ✅ Dueños de negocios con 1-20 empleados
- ✅ Negocios con procesos repetitivos (eventos, legal, retail, consultoría)
- ✅ Personas que quieren dejar de ser esclavas de su administración
- ❌ Emprendedores que están aprendiendo su industria
- ❌ Empresas que buscan una plataforma lista sin personalizar

---

## Contribuir

¡Bienvenidas las contribuciones! Lee [CONTRIBUTING.md](CONTRIBUTING.md) para empezar.

### Áreas donde necesitamos ayuda

- 🎨 Dashboard web (React/Next.js)
- 🗣️ Transcripción de voz (Whisper integration)
- 📱 App móvil
- 🌍 Traducciones
- 📊 Más skills por industria

---

## Créditos

- **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** — Framework base por Nous Research
- **[WS Capital AI Lab](https://github.com/ws-capital)** — Adaptación y skills empresariales
- **Clientes reales** — Paola Meneses Decoración, Willow Narváez Legal, y más

---

## Licencia

MIT License — Libre para usar, modificar y distribuir.

---

**El humano piensa. Hermes ejecuta. El humano revisa. Hermes aprende.**

_Hecho con ❤️ en Latinoamérica_
