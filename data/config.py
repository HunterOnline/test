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

POSTGRES_URI = f"postgres://med_bot_users_o7ga_user:pGYXHHAvXCslZLfG4K26pWUOLmWKNT4V@dpg-cmtukhen7f5s73b262rg-a.frankfurt-postgres.render.com/med_bot_users_o7ga"

#POSTGRES_URI = f"postgresql://{PG_USER}:{PG_PASS}@{db_host}/{DATABASE}"
