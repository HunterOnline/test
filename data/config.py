import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
ADMINS = 401041664
PG_USER = str(os.getenv("PG_USER"))
PG_PASS= str(os.getenv("PG_PASS"))
DATABASE = str(os.getenv("DATABASE"))
ip = os.getenv("ip")
db_host = ip
aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

POSTGRES_URI = 

#POSTGRES_URI = f"postgresql://{PG_USER}:{PG_PASS}@{db_host}/{DATABASE}"
# webhook settings
WEBHOOK_HOST = f"https://{ip}"
WEBHOOK_PORT = 8443
WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = os.getenv("WEBAPP_PORT")

WEBHOOK_SSL_CERT = "webhook_cert.pem"
WEBHOOK_SSL_PRIV = "webhook_pkey.pem"
