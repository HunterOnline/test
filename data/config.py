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

POSTGRES_URI = f"postgresql://postgres:N9a4sY59da1ibQGAKTfV@containers-us-west-200.railway.app:7428/railway"

#POSTGRES_URI = f"postgresql://{PG_USER}:{PG_PASS}@{db_host}/{DATABASE}"