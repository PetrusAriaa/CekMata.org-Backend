# This function is built because db initialization
# and alembic migration cannot read data from loaded
# .env file in main.py

# Currently it only used by db.py and alembic/env.py

# Function may not be used in production.
# Set env variables using docker-compose.yml instead.

# from dotenv import load_dotenv

import os

# load_dotenv('.env.development')

def get_env(key: str) -> str:
    return os.getenv(key)