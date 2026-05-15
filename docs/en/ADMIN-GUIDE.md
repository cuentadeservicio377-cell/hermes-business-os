# Guía de Administración — Hermes Business OS

## Configuración Avanzada

### Estructura de Configuración

```
config/
├── empresa.yaml              ← Configuración principal de la empresa
├── empresa.yaml.example      ← Plantilla
├── google-service-account.json  ← Cuenta de servicio de Google
└── industrias/
    ├── eventos.yaml
    ├── legal.yaml
    ├── retail.yaml
    └── consultoria.yaml
```

### Configuración por Empresa (`empresa.yaml`)

```yaml
empresa:
  nombre: "Mi Empresa"
  industria: "eventos"
  tamano_equipo: 5
  moneda: "MXN"
  iva_incluido: true

departamentos:
  ventas: true
  operaciones: true
  documentos: true
  finanzas: true
  rrhh: true

integraciones:
  google_workspace:
    activa: true
    drive_folder_id: ""
    sheets_master_id: ""
  telegram:
    activa: true

plantilla:
  color_primario: "#4F46E5"
  color_secundario: "#10B981"
  logo_url: ""
```

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `HBOS_CONFIG_PATH` | Ruta al config YAML | `./config/empresa.yaml` |
| `HBOS_DATA_DIR` | Directorio de datos JSON | `./data` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Ruta a JSON de cuenta de servicio | — |

---

## Gestión de Datos

### Archivos JSON Locales

Todos los datos se almacenan en `data/*.json`:

| Archivo | Skill | Contenido |
|---------|-------|-----------|
| `clients.json` | hermes-ventas | Clientes y prospectos |
| `quotes.json` | hermes-ventas | Cotizaciones generadas |
| `pipeline.json` | hermes-ventas | Pipeline de ventas |
| `projects.json` | hermes-operaciones | Proyectos activos |
| `tasks.json` | hermes-operaciones | Tareas |
| `checklists.json` | hermes-operaciones | Checklists de proyecto |
| `budgets.json` | hermes-finanzas | Presupuestos |
| `payments.json` | hermes-finanzas | Pagos y transacciones |
| `team.json` | hermes-rrhh | Miembros del equipo |
| `attendance.json` | hermes-rrhh | Registros de asistencia |
| `catalog.json` | hermes-ventas | Catálogo de servicios |

### Backup

```bash
# Backup manual
cp -r data data-backup-$(date +%Y%m%d)

# Backup automático (cron diario)
0 2 * * * cd /path/to/hbos && tar czf backups/data-$(date +\%Y\%m\%d).tar.gz data/
```

---

## Mantenimiento

### Verificación de Salud

```bash
hbos doctor
```

Verifica:
- ✅ Hermes Agent instalado
- ✅ Skills presentes
- ✅ Configuración válida
- ✅ Dependencias Python
- ✅ Google Workspace (opcional)

### Logs

Hermes Agent logs:
```bash
hermes logs
```

Dashboard logs (desarrollo):
```bash
cd dashboard && npm run dev
```

### Actualización

```bash
# Automática
hbos update

# Manual
git pull origin main
bash scripts/test.sh
hbos install
```

---

## Troubleshooting

### Skills no se cargan

```bash
# Verificar estructura
ls ~/.hermes/skills/hermes-*

# Reinstalar
hbos install

# Verificar permisos
chmod -R 755 skills/
```

### Datos corruptos

```bash
# Verificar JSON
python3 -c "import json; json.load(open('data/clients.json'))"

# Restaurar desde backup
cp data-backup-YYYYMMDD/clients.json data/clients.json
```

### Google Workspace desconectado

1. Verificar archivo JSON: `ls config/google-service-account.json`
2. Verificar APIs habilitadas en Google Cloud Console
3. Verificar compartición de Drive/Sheets con el email de la cuenta de servicio
4. Re-run onboarding: `hbos onboarding`

---

## Seguridad

- **Nunca** compartas `config/google-service-account.json`
- **Nunca** commitees `empresa.yaml` real (usa `.gitignore`)
- Rotar tokens de Telegram periódicamente
- Backup diario de `data/` recomendado

---

## Escalabilidad

Para equipos > 20 personas, considerar:
- Migrar JSON a PostgreSQL (misma interfaz Python)
- Redis para caché de sesiones
- Load balancer para múltiples instancias de Hermes Gateway
