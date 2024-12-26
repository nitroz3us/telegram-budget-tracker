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
# ... other message templates ...