import os
import sys
from dotenv import load_dotenv

load_dotenv()

secret = os.getenv("APP_SECRET")

if not secret:
    print("ERROR: APP_SECRET not found!")
    sys.exit(1)

secret_hash = secret[:3] + "**"

print(f"System started. Secret hash: {secret_hash}")