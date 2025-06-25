import os
from dotenv import load_dotenv

load_dotenv()

admin_user = os.getenv("ADMIN_USERNAME", "admin")
admin_pass = os.getenv("ADMIN_PASSWORD", "changeme")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.getenv("DB_PATH", os.path.join(BASE_DIR, "Database", "store.db"))
