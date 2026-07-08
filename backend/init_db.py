# reinit_db.py
from src.integrations.database import init_db
init_db()
print("✅ Database recreated with new columns")