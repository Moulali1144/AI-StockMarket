import os
import sys

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable not set")
    sys.exit(1)

CHECK_INTERVAL = 300
