from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]
PREFIX = os.environ.get("PREFIX", "!")
SERVIDOR_ID = os.environ.get("SERVIDOR_ID")

BELA_ID1 = int(os.environ["BELA_ID1"])
BELA_ID2 = int(os.environ["BELA_ID2"])
BELA = (BELA_ID1, BELA_ID2)

GOUTE_ID1 = int(os.environ["GOUTE_ID1"])
GOUTE_ID2 = int(os.environ["GOUTE_ID2"])
GOUTE = (GOUTE_ID1, GOUTE_ID2)
