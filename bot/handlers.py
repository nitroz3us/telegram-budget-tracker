"""
Telegram Bot Command Handlers

This module contains all the command handlers for the Budget Tracker Bot.
Each function corresponds to a specific command that users can invoke:

- /start: Welcome message and initial setup
- /setbalance: Set initial account balance
- /add: Add new transactions (income/expenses)
- /balance: Check current balance
- /report: Generate Excel report of transactions
- /monthly: View monthly expense breakdown
- /help: Display available commands

The module also handles database interactions through the Database class
and maintains global state for balance and transactions.
"""

from telegram import Update
from telegram.ext import ContextTypes
import pandas as pd
from datetime import datetime
from config import ALLOWED_USER_ID, REPORT_FILE_NAME
from database.supabase import db
from bot.messages import *
from typing import Optional
from telegram.constants import ParseMode
import os
from bot.utils import process_excel_import

# Global variables declaration first
starting_balance: Optional[float] = None
current_balance: Optional[float] = None
transactions = []

def initialize_from_db():
    """Initialize global variables from database"""
    global starting_balance, current_balance, transactions
    
    # Clear existing transactions
    transactions = []
    
    # Get starting balance from database
    starting_balance = db.get_starting_balance()
    if starting_balance is not None:
        current_balance = starting_balance  # Initialize current_balance
        
        # Get existing transactions
        response = db.get_transactions()
        if response.data:
            transactions.extend(response.data)
            # Calculate current balance including all transactions
            for transaction in transactions:
                current_balance += float(transaction['amount'])
    else:
        current_balance = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text(UNAUTHORIZED_MESSAGE)
        return
        
    global starting_balance, current_balance
    if starting_balance is None:
        await update.message.reply_text(WELCOME_NO_BALANCE_MESSAGE)
    else:
        # Format the balance with escaped decimal point
        balance_str = f"{current_balance:.2f}".replace(".", "\\.")
        await update.message.reply_text(
            WELCOME_MESSAGE.format(balance_str), 
            parse_mode=ParseMode.MARKDOWN_V2
        )

async def set_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("🚫 Sorry, this is a private bot.")
        return
        
    global starting_balance, current_balance
    try:
        if starting_balance is not None:
            await update.message.reply_text("❌ Initial balance has already been set!")
            return
            
        amount = float(context.args[0])
        starting_balance = amount
        current_balance = amount
        
        # Use the proper Database method
        db.update_starting_balance(amount)
        
        await update.message.reply_text(f"""
✅ Initial balance set to: ${amount:.2f}

You can now use:
➕ /add - Record transactions
💳 /balance - Check balance
❓ /help - More commands
""")
    except (IndexError, ValueError):
        await update.message.reply_text("""
❌ Usage: /setbalance <amount>
Example: /setbalance 7264.96
""")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("🚫 Sorry, this is a private bot.")
        return
        
    global current_balance
    if starting_balance is None:
        await update.message.reply_text("❌ Please set your initial balance first using /setbalance <amount>")
        return
    try:
        user_input = " ".join(context.args)
        if not context.args:
            raise ValueError("No arguments provided")
            
        amount, category, description = user_input.split(" ", 2)
        amount = float(amount)
        
        # Standardize category
        category = category.strip().title()
        
        # Valid categories list
        valid_categories = [
            "Food",
            "Transport",
            "Shopping",
            "Entertainment",
            "Bills",
            "Health",
            "Income",
            "Others"
        ]
        
        if category not in valid_categories:
            categories_str = "\n• ".join(valid_categories)
            await update.message.reply_text(f"""
❌ Invalid category. Please use one of:
• {categories_str}

Examples:
• /add -50 Food Lunch at hawker centre
• /add -20 Transport Grab to work
• /add 3000 Income March salary
""")
            return

        current_balance += amount
        db.add_transaction(amount, category, description, current_balance)
        
        emoji = "➕" if amount > 0 else "➖"
        amount_str = f"{abs(amount):.2f}".replace(".", "\\.")
        balance_str = f"{current_balance:.2f}".replace(".", "\\.")
        
        await update.message.reply_text(f"""
✅ Transaction added\!
{emoji} Amount: ${amount_str}
🏷️ Category: {category}
📝 Description: {description}
💰 New Balance: ||${balance_str}||
""", parse_mode=ParseMode.MARKDOWN_V2)
    except Exception as e:
        print(f"Debug - Error: {str(e)}")  # Debug print
        await update.message.reply_text("""
❌ Usage: /add <amount> <category> <description>

Examples:
• /add -50 Food Lunch at hawker centre
• /add -20 Transport Grab to work
• /add 3000 Income March salary
""")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("🚫 Sorry, this is a private bot.")
        return
    
    if current_balance is None:
        await update.message.reply_text("❌ Please set your initial balance first using /setbalance <amount>")
        return
    
    # Escape the decimal point for MarkdownV2
    balance_str = f"{current_balance:.2f}".replace(".", "\\.")
    await update.message.reply_text(f"💰 Current balance: ||${balance_str}||", parse_mode=ParseMode.MARKDOWN_V2)

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("🚫 Sorry, this is a private bot.")
        return

    # Get transactions from database instead of using global list
    response = db.get_transactions()
    if not response.data:
        await update.message.reply_text("❌ No transactions to report.")
        return

    # Convert to DataFrame and save to Excel
    df = pd.DataFrame(response.data)
    df.to_excel(REPORT_FILE_NAME, index=False)
    
    with open(REPORT_FILE_NAME, 'rb') as file:
        await update.message.reply_document(
            file,
            caption="✨ Here's your transaction report!"
        )

async def monthly_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("🚫 Sorry, this is a private bot.")
        return

    response = db.get_transactions()
    if not response.data:
        await update.message.reply_text("❌ No transactions to analyze.")
        return

    # Convert to DataFrame from Supabase response
    df = pd.DataFrame(response.data)
    
    target_month = datetime.now().month
    target_year = datetime.now().year
    
    if context.args:
        try:
            target_month = int(context.args[0])
            if len(context.args) > 1:
                target_year = int(context.args[1])
        except ValueError:
            await update.message.reply_text("❌ Invalid month/year format. Use: /monthly [month] [year]")
            return

    df['date'] = pd.to_datetime(df['date'])
    monthly_df = df[
        (df['date'].dt.month == target_month) & 
        (df['date'].dt.year == target_year) & 
        (df['amount'] < 0)
    ]

    if monthly_df.empty:
        month_name = datetime.strptime(str(target_month), "%m").strftime("%B")
        await update.message.reply_text(f"❌ No expenses found for {month_name} {target_year}")
        return

    # Calculate category totals
    category_totals = monthly_df.groupby('category')['amount'].sum().abs()
    total_expenses = category_totals.sum()
    
    # Create the report message
    month_name = datetime.strptime(str(target_month), "%m").strftime("%B")
    report = f"""
📈 Expense Report: {month_name} {target_year}

💹 Category Breakdown:"""

    # Add details for each category
    for category in category_totals.index:
        category_amount = category_totals[category]
        percentage = (category_amount / total_expenses) * 100
        
        # Get transactions for this category
        category_transactions = monthly_df[monthly_df['category'] == category]
        
        # Format amounts with escaped decimal points
        cat_amount_str = f"{category_amount:.2f}".replace(".", "\\.")
        percentage_str = f"{percentage:.1f}".replace(".", "\\.")
        
        report += f"\n\n🏷️ {category}: ${cat_amount_str} \\({percentage_str}%\\)"
        
        # Add transaction details
        for _, tx in category_transactions.iterrows():
            amount_str = f"{abs(tx['amount']):.2f}".replace(".", "\\.")
            date_str = pd.to_datetime(tx['date']).strftime('%d/%m')
            report += f"\n   • {date_str}: ${amount_str} \\- {tx['description']}"

    # Add total at the bottom
    total_str = f"{total_expenses:.2f}".replace(".", "\\.")
    report += f"\n\n💰 Total Expenses: ||${total_str}||"
    
    await update.message.reply_text(report, parse_mode=ParseMode.MARKDOWN_V2)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("🚫 Sorry, this is a private bot.")
        return
        
    help_text = """
📱 Available commands:

🎉 /start - Start the bot
💰 /setbalance <amount> - Set your initial balance
➕ /add <amount> <category> <description> - Add a transaction
💳 /balance - Check your current balance
📊 /report - Generate an Excel report
📈 /monthly [month] [year] - View monthly expenses
📥 /import - Import transactions from Excel file
❓ /help - Show this help message

💡 Examples:
• /setbalance 1000
• /add -50 Food Lunch
• /add 500 Income Salary
• /monthly 3 2024

📝 Import Guide:
1. Use /report to get an Excel file with the correct format
2. Use this as a template for your import file
3. Send the file with /import command

Required columns:
• date
• amount
• category
• description
• running_balance
• created_at
"""
    await update.message.reply_text(help_text)

async def import_excel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text(UNAUTHORIZED_MESSAGE)
        return
    
    # Check if file is attached
    if not update.message.document:
        await update.message.reply_text(
            "📤 Please attach an Excel file (.xlsx) with your transactions.\n"
            "The file should have these columns:\n"
            "- date (YYYY-MM-DD HH:MM:SS format)\n"
            "- amount (positive for income, negative for expenses)\n"
            "- category (must match valid categories)\n"
            "- description\n"
            "- running_balance (current balance after transaction)\n"
            "- created_at (YYYY-MM-DD HH:MM:SS format)\n\n"
            "💡 Tip: You can use /report to get an example of the correct format"
        )
        return
    
    # Verify file type
    if not update.message.document.file_name.endswith('.xlsx'):
        await update.message.reply_text("❌ Please send an Excel file (.xlsx)")
        return
    
    # Download the file
    file = await context.bot.get_file(update.message.document.file_id)
    temp_file = f"temp_{update.effective_user.id}.xlsx"
    await file.download_to_drive(temp_file)
    
    # Process the file
    try:
        status_message = await update.message.reply_text("📊 Processing your file...")
        success, message = await process_excel_import(temp_file, db)
        
        if success:
            # Reinitialize the global state after successful import
            initialize_from_db()
            await status_message.edit_text(f"✅ {message}")
        else:
            await status_message.edit_text(f"❌ Import failed:\n{message}")
    
    except Exception as e:
        await status_message.edit_text(f"❌ Error: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

__all__ = [
    'start',
    'set_balance',
    'add',
    'balance',
    'report',
    'monthly_expenses',
    'help_command',
    'initialize_from_db',
    'import_excel'
]


