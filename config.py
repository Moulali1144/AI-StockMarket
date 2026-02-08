import os
import sys

BOT_TOKEN = os.getenv("8233719276:AAFEUpZ7DsQ8jA18zuGLNZ6dIk5ld41NT7s")

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable not set")
    sys.exit(1)

CHECK_INTERVAL = 300
