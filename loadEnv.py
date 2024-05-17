from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]
PREFIX = os.environ.get("PREFIX", "!")
SERVIDOR_ID = os.environ.get("SERVIDOR_ID")
