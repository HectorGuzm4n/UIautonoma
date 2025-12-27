# config.py
import os

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Base de datos local (SQLite)
DB_PATH = os.path.join(BASE_DIR, "comandas.db")

# Carpeta donde se guardan imágenes escaneadas
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Puerto donde escucha el módulo del escáner
API_HOST = "0.0.0.0"
API_PORT = 6000

# Endpoint de la base de datos remota (se completa después)
REMOTE_API_URL = "https://API_REMOTA_AQUI"

# Token o API key para subir comandas (opcional)
REMOTE_API_TOKEN = None

# Timeouts de red (segundos)
HTTP_TIMEOUT = 10
