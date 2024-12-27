"""
Message Templates for Budget Tracker Bot

This module contains all static message templates used throughout the bot.
Messages are formatted with emojis and proper Markdown V2 syntax.

Templates include:
- Unauthorized access messages
- Welcome messages (with and without balance)
- Command responses
- Error messages

Note: Some messages use format placeholders ({}) for dynamic content
and MarkdownV2 escape characters (\\) for special characters.
"""

UNAUTHORIZED_MESSAGE = "🚫 Sorry, this is a private bot."
WELCOME_NO_BALANCE_MESSAGE = """
🎉 Welcome to the Budget Tracker Bot!
Please set your initial balance using:
/setbalance <amount>
Example: /setbalance 1000.00
"""
WELCOME_MESSAGE = """
🎉 Welcome to the Budget Tracker Bot\!
💰 Your current balance is: ||${}||

Use:
➕ /add \- Add expenses or income
💳 /balance \- Check your balance
📊 /report \- View your transactions
❓ /help \- More commands
"""
HELP_MESSAGE = """
Available commands:
...
📤 /import - Import transactions from Excel file
...
"""
IMPORT_TEMPLATE_MESSAGE = """
📊 Excel Import Template Format:

Required columns:
• date: YYYY-MM-DD
• amount: Positive for income, negative for expenses
• category: Must be one of the valid categories
• description: Transaction description

Example:
date,amount,category,description
2024-03-15,-25.50,Food,Lunch at cafe
2024-03-15,1000.00,Income,Salary
"""
# ... other message templates ...