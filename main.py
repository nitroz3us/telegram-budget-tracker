"""
Budget Tracker Bot - Main Entry Point

This is the main entry point for the Telegram Budget Tracker Bot.
It initializes the bot, sets up command handlers, and starts the bot polling.

Features:
- Initializes bot with Telegram token
- Sets up database connection
- Registers command handlers:
  • /start - Welcome and setup
  • /setbalance - Initial balance
  • /add - Record transactions
  • /balance - Check balance
  • /report - Excel report
  • /monthly - Monthly analysis
  • /help - Command list

The bot uses python-telegram-bot for Telegram interactions
and Supabase for database operations.
"""

from telegram.ext import Application, CommandHandler
from config import TELEGRAM_BOT_TOKEN
from bot.handlers import *
from database.supabase import db

def main():
    # Initialize bot
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("No token provided")

    # Initialize state from database
    initialize_from_db()

    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setbalance", set_balance))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("report", report))
    application.add_handler(CommandHandler("monthly", monthly_expenses))
    application.add_handler(CommandHandler("help", help_command))

    # Start the bot
    print("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    main()