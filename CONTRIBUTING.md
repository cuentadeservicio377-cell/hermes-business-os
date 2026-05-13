# Contributing to Hermes Business OS

Thank you for your interest in contributing! This project is built for the community.

## How to Contribute

### Reporting Bugs

1. Check if the issue already exists
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Docker version, etc.)

### Suggesting Features

1. Open an issue with the `enhancement` label
2. Describe the use case
3. Explain why it benefits PYMES

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit PR with clear description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/hermes-business-os.git
cd hermes-business-os

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --reload
```

## Code Style

- Python: PEP 8
- Docstrings: Google style
- Type hints encouraged
- Comments in English, user-facing text in Spanish

## Areas Needing Help

- 🎨 Frontend dashboard (React/Vue)
- 🗣️ Voice transcription (Whisper)
- 📱 Mobile app
- 🌍 i18n (English, Portuguese)
- 📊 More industry-specific skills
- 🧪 Test coverage

## Code of Conduct

Be respectful, inclusive, and constructive. We're building this for PYMES who need our help.

## Questions?

Open an issue or reach out to the maintainers.
