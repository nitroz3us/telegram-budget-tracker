from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Bot configuration
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID"))
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_API_TOKEN")

# Database configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# File configuration
REPORT_FILE_NAME = "budget_tracker.xlsx"