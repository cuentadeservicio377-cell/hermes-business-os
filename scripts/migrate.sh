#!/bin/bash
# Database migration script

echo "🗄️  Hermes Business OS - Database Migration"

cd backend

# Run migrations
python -c "
from core.database import init_db
init_db()
print('✅ Database initialized')
"

echo "Migration complete"
