<div align="center">

# Hermes Business OS

### **El Sistema Operativo de IA para Pequeñas Empresas en Latinoamérica**

[![Powered by Hermes Agent](https://img.shields.io/badge/Powered%20by-Hermes%20Agent-6366f1?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyIDJDNi40NzcgMiAyIDYuNDc3IDIgMTJzNC40NzcgMTAgMTAgMTAgMTAtNC40NzcgMTAtMTBTMTcuNTIzIDIgMTIgMnptMCAxOGMtNC40MTggMC04LTMuNTgyLTgtOHMzLjU4Mi04IDgtOCA4IDMuNTgyIDggOC0zLjU4MiA4LTggOHptLTEtMTN2N2w1LjUgMy41TDE3LjUgMTRsLTQuNS0yLjVWN2wtMSAxeiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=)](https://github.com/NousResearch/hermes-agent)
[![Tests](https://img.shields.io/badge/Tests-73%2F73%20passing-22c55e?style=flat-square)](scripts/test.sh)
[![License: MIT](https://img.shields.io/badge/License-MIT-f59e0b?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-15-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org)

**[📄 English](README.md)** · **[📖 Docs](docs/)** · **[🔬 Research Paper (EN)](docs/RESEARCH-PAPER.en.md)** · **[🔬 Research Paper (ES)](docs/RESEARCH-PAPER.md)** · **[🚀 Inicio Rápido](#inicio-rápido)**

</div>

---

## ¿Qué es esto?

**Hermes Business OS** es una **distribución de skills nativos** para [Hermes Agent](https://github.com/NousResearch/hermes-agent) (de Nous Research) que transforma al agente de IA en el **sistema operativo de tu pequeña empresa**.

**No** es una app separada. **No** es un servidor backend. Es un conjunto de skills de inteligencia de negocio que se conectan directamente a Hermes Agent — igual que un tema convierte un teléfono en algo personal, HBOS convierte a Hermes en tu socio de negocios.

<div align="center">

```
┌────────────────────────────────────────────────────────────┐
│  Tú envías un mensaje por WhatsApp o Telegram              │
│       ↓                                                    │
│  Hermes Agent (Nous Research) entiende tu intención        │
│       ↓                                                    │
│  HBOS enruta al skill de negocio correcto                  │
│       ↓                                                    │
│  Tus datos se guardan · Documentos se generan · Seguimientos│
│     se programan · Reportes están listos                   │
└────────────────────────────────────────────────────────────┘
```

</div>

### Tres cosas que lo hacen diferente

| 🗣️ **Habla, no hagas clicks** | 📱 **WhatsApp es tu dashboard** | 💰 **Cero costo de licencia** |
|:---|:---|:---|
| No hay menús. No hay entrenamiento. Hablas con tu negocio como hablas con un socio. "¿Cuánto facturamos este mes?" | El 70% de las pequeñas empresas latinoamericanas vende por WhatsApp. HBOS vive donde ya estás. | Código abierto (MIT). Sin costos por usuario. Sin suscripciones mensuales. Solo pagas por el modelo de IA que elijas. |

---

## ¿Para quién es esto?

Fue construido para el **99.5%** de las empresas latinoamericanas que son pequeñas — las que generan el **60-67% del empleo formal** pero aportan solo el **~25% del PIB** porque están atrapadas haciendo administración a mano.

- ✅ Dueños de negocios con 1–20 empleados
- ✅ Negocios con procesos repetitivos (eventos, legal, retail, consultoría)
- ✅ Personas que son esclavas de su propia administración
- ✅ Cualquiera que quiere dejar de perder clientes por falta de seguimiento
- ✅ Equipos que venden por WhatsApp y llevan finanzas en Excel

> **No es para:** Emprendedores que están aprendiendo su industria, o empresas que buscan una plataforma lista sin personalizar.

---

## Un día con Hermes

> **Tú:** "Buenos días, ¿qué tengo hoy?"  
> **Hermes:** "Tienes 3 tareas pendientes: confirmar el lugar para la boda Martínez, enviar la cotización a González, y registrar el pago del proyecto López. El pago de López vence mañana. ¿Envío recordatorio?"
>
> **Tú:** "Registra un cliente nuevo: Carlos Ruiz, quiere XV años para 80 personas en febrero."  
> **Hermes:** "Listo. Carlos Ruiz registrado como prospecto. Generando cotización con paquete intermedio... Total: $35,000 MXN. ¿La envío?"
>
> **Tú:** "¿Cómo va la boda Martínez?"  
> **Hermes:** "Progreso: 65%. Tareas completadas: 8/12. Pendiente: confirmar catering (vence hoy) y prueba de sonido (mañana). ¿Marco catering como en progreso?"
>
> **Tú:** "¿Cuánto facturamos este mes?"  
> **Hermes:** "$127,500 MXN cobrados, $45,000 pendientes. Tienes 2 pagos vencidos: García ($12,000, 5 días) y Díaz ($8,500, 3 días). ¿Envío recordatorios?"

**Esa es toda la interfaz.** Un chat. Cero clicks.

---

## Lo que obtienes

### 6 skills de negocio

| Skill | Qué hace | Para quién |
|-------|----------|------------|
| **Ventas** (`hermes-ventas`) | CRM, cotizaciones automáticas, seguimiento de pipeline | Cualquiera que venda servicios |
| **Operaciones** (`hermes-operaciones`) | Proyectos, tareas, checklists, deadlines | Cualquiera que entregue proyectos |
| **Documentos** (`hermes-documentos`) | PDFs profesionales, contratos, propuestas | Cualquiera que envíe cotizaciones o contratos |
| **Finanzas** (`hermes-finanzas`) | Presupuestos, pagos, flujo de caja, alertas de vencimiento | Cualquiera que maneje dinero |
| **RRHH** (`hermes-rrhh`) | Equipo, asistencia, nómina por proyecto | Cualquiera que contrata personal por evento |
| **Core** (`hermes-business-core`) | Configuración de empresa, routing, Google Workspace | Todos |

### Funcionalidades clave

- 🧠 **Memoria persistente** — Hermes recuerda cada cliente, cada proyecto, cada preferencia
- 📄 **Documentos automáticos** — Cotizaciones, contratos, reportes generados por comando de chat
- 📊 **Sync con Google Workspace** — Datos viven en Sheets que tú controlas; documentos en Drive
- 🎨 **Dashboard web** — Dashboard en Next.js 15 para visión general (opcional)
- 🏭 **Templates por industria** — Pre-configurado para eventos, legal, consultoría, retail
- 🔧 **Onboarding conversacional** — "Cuéntame de tu negocio" — listo en 15 minutos

---

## Arquitectura

```
Hermes Agent (oficial Nous Research — se instala por separado)
├── AI Core, Memory, Gateway, CLI
├── Telegram / WhatsApp / Discord / Slack integration
└── Native Skills System (SKILL.md + Python tools)
    └── HERMES BUSINESS OS (este repo)
        ├── hermes-business-core/     ← Config, routing, Google Workspace
        ├── hermes-ventas/            ← CRM, cotizador, pipeline
        ├── hermes-operaciones/       ← Proyectos, tareas, checklists
        ├── hermes-documentos/        ← Kami v3 PDF engine, templates
        ├── hermes-finanzas/          ← Presupuestos, pagos, reportes
        └── hermes-rrhh/              ← Equipos, asistencia, nómina
```

**Regla de diseño crítica:** HBOS NO es un backend separado. NO es un fork de Hermes. Son skills nativos de Hermes + herramientas Python. Esto significa que recibes actualizaciones de Nous Research automáticamente — sin merge hell.

---

## Inicio Rápido

### Requisitos previos

- **macOS**, **Linux**, o **WSL2** (Windows)
- **Hermes Agent** instalado (ver Paso 1)
- Un **token de bot de Telegram** (gratis vía [@BotFather](https://t.me/BotFather))
- *(Opcional)* Cuenta de **Google Workspace** para sync de Sheets/Drive

### Paso 1 — Instalar Hermes Agent (prerrequisito obligatorio)

HBOS es un paquete de skills para Hermes Agent. Debes instalar Hermes primero.

```bash
# Instalador de una línea (instala Python 3.11, Node.js, todas las dependencias)
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# Recarga tu shell
source ~/.bashrc   # o: source ~/.zshrc

# Verifica
hermes --version
```

> 📖 [Documentación completa de Hermes Agent →](https://hermes-agent.nousresearch.com/docs/)

### Paso 2 — Instalar HBOS

```bash
# Clona este repositorio
git clone https://github.com/cuentadeservicio377-cell/hermes-business-os.git

# Instala los skills de HBOS en Hermes
cd hermes-business-os
bash scripts/install.sh

# O manualmente copia los skills al directorio de skills de Hermes
cp -r skills/* ~/.hermes/skills/
```

### Paso 3 — Configura tu empresa

```bash
# Ejecuta el wizard de configuración conversacional
hbos setup
```

El wizard te preguntará:
- Nombre de tu empresa
- Industria (eventos, legal, consultoría, retail, o personalizado)
- Tamaño del equipo
- Moneda
- Qué departamentos activar

Luego genera `config/empresa.yaml` y configura tus archivos de datos automáticamente.

### Paso 4 — Inicia el gateway

```bash
# Configura Telegram (una sola vez)
hermes gateway setup

# Inicia el gateway (Hermes ahora está vivo en Telegram)
hermes gateway start
```

Abre Telegram y envía `/start` a tu bot. Hermes te saludará e iniciará el onboarding de negocio.

### Paso 5 — (Opcional) Dashboard web

```bash
cd dashboard
npm install
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000) para una visión general visual.

---

## Métodos de instalación

| Método | Cuándo usar | Comando |
|--------|-------------|---------|
| **Instalación rápida** | Primera vez, sistema limpio | `bash scripts/install.sh` |
| **Instalación manual** | Desarrolladores, personalización | Copiar `skills/` a `~/.hermes/skills/` |
| **Docker** | Despliegue en servidor | `docker-compose -f docker/docker-compose.yml up` |

---

## Documentación

| Documento | Descripción |
|-----------|-------------|
| [📖 Guía de Instalación](docs/es/INSTALL.md) | Setup detallado, troubleshooting, config de Google Workspace |
| [👤 Guía de Usuario](docs/es/USER-GUIDE.md) | Ejemplos de uso diario por departamento |
| [⚙️ Guía de Admin](docs/es/ADMIN-GUIDE.md) | Configuración avanzada, backup, seguridad |
| [🔌 Referencia API](docs/es/API.md) | API Python de herramientas para desarrolladores |
| [📄 Research Paper](docs/RESEARCH-PAPER.md) | Por qué existe esto: inclusión digital en Latinoamérica |
| [📝 Changelog](CHANGELOG.md) | Historial de versiones |
| [🤝 Contributing](CONTRIBUTING.md) | Cómo agregar skills, reportar issues, enviar PRs |

---

## Por qué construimos esto

> Latinoamérica no necesita más emprendedores. Ya los tiene — el **99.5%** de su economía está compuesta por ellos.
>
> Lo que necesita es **infraestructura**. La misma infraestructura que las grandes corporaciones han tenido por décadas: sistemas que les permitan saber quién les debe, qué proyectos van atrasados, cuánto cuesta cada servicio, y qué oportunidades están perdiendo.
>
> El software empresarial existente es demasiado caro, demasiado complejo, y demasiado extranjero. Un dueño de negocio mexicano no debería necesitar aprender inglés, contratar un consultor de TI, o pagar $100/usuario/mes para administrar 5 empleados.
>
> **Hermes Business OS no es la solución. Es la prueba de que la solución es posible.**

Lee el paper completo: **[Inclusión Digital en Latinoamérica](docs/RESEARCH-PAPER.md)**

---

## Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| **Agent Core** | [Hermes Agent](https://github.com/NousResearch/hermes-agent) (Python, MIT) |
| **Skills** | SKILL.md nativos + herramientas Python |
| **Dashboard** | Next.js 15 + React 19 + TypeScript + Tailwind CSS |
| **Documentos** | Python + WeasyPrint (Kami v3) |
| **Datos** | Google Sheets + JSON local |
| **Comunicación** | Telegram (primario) + WhatsApp + Dashboard |

---

## Contribuir

Bienvenidas las contribuciones. Ve [CONTRIBUTING.md](CONTRIBUTING.md) para guías.

**Áreas prioritarias:**
- 🏭 Más templates por industria (salud, construcción, agricultura)
- 🌍 Traducciones (portugués para Brasil)
- 📱 Mejoras al dashboard móvil
- 🔗 Integraciones con pasarelas de pago
- 🗣️ Transcripción de notas de voz

---

## Créditos

- **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** — Framework core por [Nous Research](https://nousresearch.com)
- **[WS Capital AI Lab](https://wsc.lat)** — Adaptación de skills empresariales e investigación
- **Negocios reales** — Paola Meneses Decoración, Willow Narváez Legal, y más

---

## Licencia

MIT License — Libre para usar, modificar y distribuir.

---

<div align="center">

**El humano piensa. Hermes ejecuta. El humano revisa. Hermes aprende.**

_Hecho con ❤️ en Latinoamérica para el 99.5%_

[⬆ Volver arriba](#hermes-business-os)

</div>
