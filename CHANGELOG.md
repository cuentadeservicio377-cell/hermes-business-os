# Changelog — Hermes Business OS

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] — 2025-05-15

### Added
- **FASE 1**: Project foundation — 6 native Hermes skills, CLI installer (`hbos`), config loader, intent router, Google Workspace scaffold
- **FASE 2**: Core departments — `hermes-ventas` (CRM, Cotizador, Pipeline), `hermes-operaciones` (Proyectos, Tareas, Checklists), `hermes-documentos` (Kami v3 PDF engine)
- **FASE 3**: Web Dashboard — Next.js 15 app with 6 views (Dashboard, Clientes, Pipeline, Proyectos, Tareas, Configuración), responsive Nav, StatCards
- **FASE 4**: Onboarding Wizard — Interactive `setup_wizard.py`, automated `onboarding_engine.py` (creates JSON data files, industry catalogs, sample data, Google Drive folders, Sheets masters, welcome guide)
- **FASE 5**: Document Engine — Kami v3 + 5 HTML templates (eventos, legal, consultoría, retail, base)
- **FASE 6**: Finanzas + RRHH — Production tools for `hermes-finanzas` (Presupuestos, Pagos, Reportes) and `hermes-rrhh` (Equipos, Asistencia/Nómina)
- 60 automated tests covering file structure, skill loading, Python imports, templates, dashboard, and functional workflows
- Industry-specific catalogs: eventos, legal, consultoría, retail

### Changed
- `hermes-finanzas` and `hermes-rrhh` skills promoted from `beta` to `stable`

### Fixed
- `docs/WELCOME.md` generation now creates parent directories if missing

## [1.0.0] — 2025-04-01

### Added
- Initial concept and architecture design
- Proof-of-concept with FastAPI backend (later abandoned per architectural decision)
- Native Hermes skill format validation
