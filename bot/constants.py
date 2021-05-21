import os
from dotenv import load_dotenv

load_dotenv()

PREFIX = os.getenv("PREFIX") or ":)"
TOKEN = os.getenv("TOKEN")
