# Contributing to Hermes Business OS

Thank you for your interest in contributing! This project is a **distribution of native Hermes Agent skills** designed for small and medium businesses.

## Philosophy

> Hermes Business OS is NOT a separate backend. It is Hermes Agent + native SKILL.md skills + Python tools.

Keep it simple. Keep it native. No forks.

## How to Contribute

### 1. Report Issues

- Use GitHub Issues
- Include: Hermes version, OS, Python version, steps to reproduce
- Tag with `bug`, `feature`, `docs`, or `question`

### 2. Submit Pull Requests

1. Fork the repo
2. Create a branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `bash scripts/test.sh` (all must pass)
5. Commit with clear messages
6. Push and open a PR

### 3. Add a New Skill

Skills live in `skills/hermes-<name>/`:

```
skills/hermes-mi-skill/
├── SKILL.md          ← Required. Follow existing format
└── tools/
    ├── __init__.py
    └── mi_tool.py    ← Python tool classes
```

**SKILL.md requirements:**
- YAML frontmatter with `name`, `description`, `version`, `metadata.hermes`
- `status`: `stable` | `beta` | `experimental`
- `depends_on`: list of required skills
- Clear activation triggers
- Documented flows with tool references

**Python tool requirements:**
- Use `config_loader.get_config()` for company config
- Store data in `data/*.json` (local JSON persistence)
- Provide `format_*()` methods for human-readable output
- Use singleton pattern via `get_*()` functions
- Follow existing code style (PEP 8)

### 4. Add Industry Support

Industry configs live in `config/industrias/<industria>.yaml`:

```yaml
industria: mi_industria
servicios:
  - codigo: IND-001
    nombre: Servicio Base
    descripcion: Descripción del servicio
    precio_base: 1000
```

### 5. Improve Documentation

Docs live in `docs/`:
- `INSTALL.md` — Installation steps
- `USER-GUIDE.md` — End-user conversational examples
- `ADMIN-GUIDE.md` — Configuration and maintenance
- `API.md` — Tool API reference

## Development Setup

```bash
git clone https://github.com/cuentadeservicio377-cell/hermes-business-os.git
cd hermes-business-os
pip install pyyaml google-api-python-client google-auth-httplib2 google-auth-oauthlib weasyprint
bash scripts/test.sh
```

## Code Style

- Python: PEP 8, type hints encouraged
- TypeScript: Strict mode, functional components
- Skills: Follow existing SKILL.md structure
- Tests: Add tests for new tools in `scripts/test.sh`

## Areas Needing Help

- 🎨 Dashboard enhancements (more views, real-time updates)
- 🗣️ Voice transcription integration
- 📱 Mobile-responsive dashboard improvements
- 🌍 Spanish/English/Portuguese translations
- 📊 More industry templates
- 🔗 Additional payment gateway integrations

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
