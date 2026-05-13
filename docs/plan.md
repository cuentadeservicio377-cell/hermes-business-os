# Hermes Business OS — Implementation Plan

## Fase 1: Fundación (Spec & Arquitectura)
**Duración:** 1 semana
**Objetivo:** Estructura base lista para que cualquier agente de codificación continúe.

| ID | Tarea | Worker | Acceptance |
|----|-------|--------|------------|
| F1.1 | Crear estructura de directorios | wsimplementer | `tree` muestra árbol completo |
| F1.2 | Generar spec.md | wsspecarchitect | Documento completo, revisable |
| F1.3 | Generar plan.md | wsspecarchitect | Fases definidas con milestones |
| F1.4 | Generar tasks.md | wsspecarchitect | Tareas con dependencias |
| F1.5 | Generar quickstart.md | wsspecarchitect | Developer puede instalar en <30 min |
| F1.6 | Generar research-paper.md | wsspecarchitect | Paper listo para publicación |

## Fase 2: Implementación Core
**Duración:** 2-3 semanas
**Objetivo:** Sistema funcional con 3 departamentos base.

| ID | Tarea | Worker | Acceptance |
|----|-------|--------|------------|
| F2.1 | Backend FastAPI base | wsimplementer | `curl /health` responde 200 |
| F2.2 | Sistema de skills modular | wsimplementer | Nuevo skill se registra en 3 líneas |
| F2.3 | Templates Kami v3 | wsimplementer | Genera PDF desde template HTML |
| F2.4 | Google Workspace integration | wsimplementer | Lee/Escribe Sheets y Docs |
| F2.5 | Config de Hermes genérica | wsimplementer | `client.yaml` define empresa |
| F2.6 | Docker/docker-compose | wsimplementer | `docker-compose up` levanta todo |
| F2.7 | Telegram bot base | wsimplementer | Bot responde /start y eco |
| F2.8 | Department: Ventas | wsimplementer | Cotizaciones + CRM básico |
| F2.9 | Department: Operaciones | wsimplementer | Proyectos + tareas |
| F2.10 | Department: Documentos | wsimplementer | Genera docs desde templates |

## Fase 3: QA & Validación
**Duración:** 1 semana
**Objetivo:** Sistema probado, documentado, listo para open source.

| ID | Tarea | Worker | Acceptance |
|----|-------|--------|------------|
| F3.1 | Probar instalación desde cero | wsqaauditor | Instala en VPS limpio sin errores |
| F3.2 | Verificar agente externo puede configurar | wsqaauditor | Otro AI sigue quickstart y logra deploy |
| F3.3 | Revisar documentación completa | wsqaauditor | Todos los .md son coherentes |
| F3.4 | Security audit | wsqaauditor | No secrets en repo, .env.example completo |
| F3.5 | Performance test | wsqaauditor | <2s respuesta API en local |

## Fase 4: Deploy & Publicación
**Duración:** 3-5 días
**Objetivo:** Repo público, release, paper publicado.

| ID | Tarea | Worker | Acceptance |
|----|-------|--------|------------|
| F4.1 | Crear repo GitHub público | wsimplementer | Repo accesible, README completo |
| F4.2 | Publicar release v0.1.0 | wsimplementer | Tag + release notes |
| F4.3 | Entregar paper de investigación | wsspecarchitect | PDF profesional listo |
| F4.4 | Handoff completo | Neo | Pablo tiene todo, sabe qué sigue |

## Dependencias

```
F1.1 → F1.2 → F1.3 → F1.4 → F1.5 → F1.6
  ↓
F2.1 → F2.2 → F2.3 → F2.4 → F2.5 → F2.6
  ↓
F2.7 → F2.8 → F2.9 → F2.10
  ↓
F3.1 → F3.2 → F3.3 → F3.4 → F3.5
  ↓
F4.1 → F4.2 → F4.3 → F4.4
```

## Milestones

| Milestone | Fecha Target | Deliverable |
|-----------|-------------|-------------|
| M1: Spec Completo | Día 7 | spec.md, plan.md, tasks.md, quickstart.md |
| M2: Backend Funcional | Día 21 | API corriendo, 3 departamentos operativos |
| M3: QA Passed | Día 28 | Checklist QA completo, sin bloqueos |
| M4: Release Pública | Día 32 | Repo GitHub, release v0.1.0, paper |

## Riesgos

| Riesgo | Mitigación |
|--------|-----------|
| Complejidad excesiva | MVP enfocado, features se agregan post-v0.1 |
| Documentación pobre | Quickstart probado por agente externo |
| Dependencia de Google | Abstract integration layer, swappable |
| Escalabilidad | Diseño modular desde día 1 |
