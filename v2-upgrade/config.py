import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

admin_user = os.getenv("ADMIN_USERNAME", "admin").strip()
admin_pass = os.getenv("ADMIN_PASSWORD", "changeme").strip()

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "Database" / "store.db"))
RECEIPT_PATH = Path(os.getenv("RECEIPT_PATH", str(BASE_DIR / "Receipts")))