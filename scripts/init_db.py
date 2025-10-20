#!/usr/bin/env python3
from app.core.db import init_db
from app.core.config import settings
print("Initializing DB...")
init_db()
print("DB initialized")
