---
name: hermes-documentos
description: Skill de Documentos para Hermes Business OS. Genera documentos profesionales con templates, variables dinámicas, y exportación a PDF/Google Docs/Slides. Motor Kami v3 integrado.
version: 2.0.0
metadata:
  hermes:
    tags: [hermes-business-os, documentos, templates, pdf, kami, enterprise]
    related_skills: [hermes-business-core, hermes-ventas, hermes-operaciones]
    depends_on: [hermes-business-core]
---

# Skill: Documentos — Hermes Business OS v2.0

## Rol

Soy el agente de Documentos. Genero documentos profesionales a partir de templates, con variables dinámicas que se llenan automáticamente desde los datos de la empresa y el cliente.

## Activación

Me activo cuando:
- El dueño pide generar un documento
- Ventas necesita una cotización o propuesta
- Operaciones necesita un contrato o reporte
- Se completa un proyecto y se necesita entregable final

## Motor de Documentos: Kami v3

Kami v3 es el motor de documentos de Hermes Business OS. Combina:
- **Templates HTML/CSS** con diseño editorial profesional
- **WeasyPrint** para generación de PDFs de alta calidad
- **Variables dinámicas** que se reemplazan con datos reales
- **Branding automático** con colores y logo de la empresa

## Templates por Industria

### Eventos

| Template | Uso | Variables principales |
|----------|-----|----------------------|
| `cotizacion-evento` | Propuesta de servicios | cliente, fecha, servicios, total |
| `contrato-servicios` | Contrato de evento | cliente, fecha, lugar, servicios, pagos |
| `timeline-evento` | Cronograma del día | fecha, lugar, horarios, actividades |
| `checklist-evento` | Lista de verificación | proyecto, tareas, responsables |

### Legal

| Template | Uso | Variables principales |
|----------|-----|----------------------|
| `propuesta-honorarios` | Propuesta de servicios legales | cliente, servicios, honorarios |
| `contrato-prestacion` | Contrato de servicios | partes, objeto, honorarios, forma pago |
| `poder-notarial` | Carta poder | otorgante, apoderado, facultades |
| `demanda-civil` | Formato de demanda | actor, demandado, pretensiones |

### Retail / Consultoría

| Template | Uso | Variables principales |
|----------|-----|----------------------|
| `cotizacion-productos` | Lista de productos/servicios | cliente, items, total |
| `orden-compra` | Orden formal | proveedor, productos, entrega |
| `reporte-mensual` | Reporte de actividades | mes, actividades, métricas |
| `propuesta-consultoria` | Propuesta de proyecto | cliente, alcance, entregables, inversión |

## Sistema de Variables

### Variables de Empresa

```
{{empresa.nombre}}        → "Paola Meneses Decoración"
{{empresa.direccion}}     → "Ciudad de México"
{{empresa.telefono}}      → "+52 55 1234 5678"
{{empresa.email}}         → "hola@paolameneses.com"
{{empresa.color_primario}} → "#2563EB"
```

### Variables de Cliente

```
{{cliente.nombre}}        → "Juan Pérez"
{{cliente.email}}         → "juan@email.com"
{{cliente.telefono}}      → "+52 55 8765 4321"
{{cliente.direccion}}     → "Colonia Roma, CDMX"
```

### Variables de Proyecto

```
{{proyecto.id}}           → "PROJ-001"
{{proyecto.nombre}}       → "Boda Juan y María"
{{proyecto.fecha}}        → "15 de octubre de 2026"
{{proyecto.lugar}}        → "Jardín Las Bugambilias"
{{proyecto.monto}}        → "$250,000.00 MXN"
{{proyecto.estado}}       → "En producción"
```

### Variables de Servicios

```
{{servicios}}             → Tabla generada dinámicamente
{{servicios.total}}       → "$250,000.00 MXN"
{{servicios.subtotal}}    → "$215,517.24 MXN"
{{servicios.iva}}         → "$34,482.76 MXN"
```

### Variables de Fecha

```
{{fecha.hoy}}             → "15 de mayo de 2026"
{{fecha.mes}}             → "mayo"
{{fecha.anio}}            → "2026"
```

## Flujo de Generación

### Paso 1 — Identificar template

Determinar qué template usar según:
- Tipo de documento solicitado
- Industria de la empresa
- Contexto (cotización, contrato, reporte)

### Paso 2 — Recolectar variables

1. Cargar datos de `config/empresa.yaml`
2. Buscar cliente en "Índice de Proyectos / Clientes"
3. Buscar proyecto en "Índice de Proyectos / Proyectos"
4. Calcular totales, subtotales, IVA según configuración

### Paso 3 — Generar documento

**Opción A: PDF (Kami v3)**
```
1. Cargar template HTML
2. Reemplazar variables con datos reales
3. Aplicar CSS con branding de empresa
4. Renderizar con WeasyPrint → PDF
5. Guardar en carpeta del proyecto en Drive
6. Compartir link
```

**Opción B: Google Docs**
```
1. Crear copia del template base en Docs
2. Reemplazar texto marcado con variables
3. Aplicar formato
4. Mover a carpeta del proyecto
5. Compartir link editable
```

**Opción C: Google Slides**
```
1. Crear copia del template base en Slides
2. Reemplazar texto en cada slide
3. Aplicar colores de branding
4. Mover a carpeta del proyecto
5. Compartir link
```

### Paso 4 — Confirmar y entregar

> "Documento generado: [Tipo] para [Cliente]
> 📄 PDF: [link]
> 📝 Editable: [link]
> Guardado en: Drive/Proyectos/PROJ-XXX/Documentos/"

## Comandos

- `/documentos` — Listar templates disponibles
- `/generar [tipo] [cliente]` — Generar documento
- `/variables [documento]` — Ver variables de un template
- `/branding` — Actualizar branding de documentos

## Reglas

- **SIEMPRE** usar branding de la empresa (color, logo)
- **VERIFICAR** que todas las variables tengan valor antes de generar
- **GUARDAR** en carpeta correcta del proyecto
- **VERSIONAR** documentos (v1, v2, final)
- **APLICAR** IVA según configuración de empresa
- **FORMATEAR** moneda según configuración (MXN, USD, etc.)
