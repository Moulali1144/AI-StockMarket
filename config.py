import os
import sys
from dotenv import load_dotenv

load_dotenv()  # load .env file

BOT_TOKEN = os.getenv("8233719276:AAFEUpZ7DsQ8jA18zuGLNZ6dIk5ld41NT7s")

if not BOT_TOKEN:
    print("❌ BOT_TOKEN NOT FOUND")
    sys.exit(1)

CHECK_INTERVAL = 300
