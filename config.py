import os
import sys

BOT_TOKEN = os.getenv("8233719276:AAFEUpZ7DsQ8jA18zuGLNZ6dIk5ld41NT7s")

print("DEBUG BOT_TOKEN =", BOT_TOKEN)

if not BOT_TOKEN:
    print("❌ BOT_TOKEN NOT FOUND")
    sys.exit(1)

CHECK_INTERVAL = 300
