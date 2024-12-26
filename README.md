# Budget Tracker Bot

https://github.com/user-attachments/assets/fc4aa895-206c-478c-b90e-f74ca2ae467d

## 📝 Purpose

This is a Telegram bot that helps you track your expenses and income, manage your balance, and generate reports of your financial activity.

## ✨ Features

### 💰 Balance Management

- Set and track initial balance
- Real-time balance updates with each transaction
- Hidden balance display using spoiler tags for privacy
- Running balance tracking for each transaction

### 💳 Transaction Recording

- Add both expenses (negative) and income (positive)
- Standardized category system with validation:
  - Food
  - Transport
  - Shopping
  - Entertainment
  - Bills
  - Health
  - Income
  - Others
- Multi-word descriptions support
- Automatic date and time recording

### 📊 Reporting & Analysis

- Monthly expense breakdown by category
- Percentage analysis of spending per category
- Detailed transaction listing with dates
- Excel report generation with full transaction history
- Transaction sorting by date (newest first)

### 🔒 Security Features

- Private bot access (single user)
- User authentication via Telegram ID
- Secure credential management via .env
- Hidden sensitive information in messages

### 💾 Database Features

- Persistent data storage using Supabase
- Real-time transaction tracking
- Automatic timestamp recording
- Running balance maintenance

### 🎨 User Experience

- Emoji-rich interface
- Clear command structure
- Detailed help messages
- Informative error handling
- Example commands for easy learning

## Commands:

1. **/start**

   - Displays a welcome message and lists the available commands.

2. **/add `<amount>` `<category>` `<description>`**

   - Adds a transaction.
   - Example: `/add -50 Food Lunch`
   - It subtracts expenses (negative amounts) and adds income (positive amounts).

3. **/balance**

   - Displays the current balance.

4. **/report**

   - Generates and sends a report of all transactions in an Excel file.

5. **/monthly `[YYYY-MM]`**

   - Shows expenses for a specific month (defaults to the current month if no argument is provided).
   - Expenses are shown by category, with a breakdown of totals and percentages.

6. **/help**
   - Displays a list of available commands.

## Explanation of Code:

### Global Variables:

- `transactions`: Stores a list of all transactions.
- `starting_balance`: The initial balance when the bot is started.
- `current_balance`: Tracks the current balance as transactions are added.
- `file_name`: The name of the Excel file where transactions are stored.

### Functions:

- **`start(update, context)`**: Sends a welcome message and explains how to use the bot.
- **`add(update, context)`**: Parses user input to add a transaction. It updates the current balance and records the transaction with the amount, category, and description.
- **`balance(update, context)`**: Sends the current balance to the user.
- **`report(update, context)`**: Creates an Excel report of all transactions and sends it as a file to the user.
- **`monthly_expenses(update, context)`**: Displays a breakdown of expenses for a specific month, either from the provided month or the current month.
- **`help_command(update, context)`**: Lists all available commands for the user.

### Main Function:

The bot is initialized and commands are added to the dispatcher. It starts polling for messages and waits for user input.

## Conclusion:

This bot is useful for managing personal finances directly through Telegram, allowing you to track your expenses and income seamlessly.

## Database Setup

Create a Supabase project at [supabase.com](https://supabase.com) and run the following SQL to create the required tables:

```sql
-- Transactions table for storing all financial records
CREATE TABLE transactions (
    id int8 PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    date timestamptz NOT NULL,
    amount numeric NOT NULL,
    category varchar NOT NULL,
    description text,
    running_balance numeric NOT NULL,
    created_at timestamptz DEFAULT NOW()
);

-- Settings table for storing balance and other configurations
CREATE TABLE settings (
    key varchar PRIMARY KEY,
    value text,
    updated_at timestamptz DEFAULT NOW()
);

-- Initial settings entry for starting balance
INSERT INTO settings (key, value) VALUES ('starting_balance', null);
```

The tables will store:

**transactions**

- `id`: Unique identifier for each transaction
- `date`: When the transaction occurred
- `amount`: Transaction amount (positive for income, negative for expenses)
- `category`: Transaction category (e.g., Food, Transport)
- `description`: Additional transaction details
- `running_balance`: Balance after this transaction
- `created_at`: When the record was created

**settings**

- `key`: Setting identifier (e.g., 'starting_balance')
- `value`: Setting value
- `updated_at`: Last update timestamp

## Environment Setup

1. Create a `.env` file in the root directory with your credentials:

```env
# Telegram Bot Token (Get from @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
ALLOWED_USER_ID=your_telegram_user_id

# Supabase Credentials (Get from Supabase Dashboard)
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

2. How to get your credentials:

   **Telegram:**

   - Create a new bot with [@BotFather](https://t.me/botfather) and copy the bot token
   - Get your Telegram User ID from [@userinfobot](https://t.me/userinfobot)

   **Supabase:**

   - Go to your [Supabase Dashboard](https://app.supabase.com)
   - Select your project
   - Find credentials under Project Settings > API:
     - Project URL: Copy the URL under "Project URL"
     - API Key: Copy the anon/public key under "Project API keys"

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Run the bot:

```bash
python main.py
```

⚠️ **Security Note**:

- Never commit your `.env` file to version control
- Keep your Supabase and Telegram credentials private
- The bot will only respond to the Telegram user ID specified in `ALLOWED_USER_ID`

## 🚀 Latest Updates

### Version 1.1.0 (26 December 2024)

- ✨ Added spoiler tags to hide sensitive balance information
- 🎨 Improved monthly report formatting with transaction details
- 🔒 Added category validation to prevent typos
- 📝 Support for multi-word descriptions in transactions
- 🛠️ Fixed decimal point formatting in MarkdownV2

### Version 1.0.0 (20 December 2024)

- 🎉 Initial release
- 💰 Basic expense and income tracking
- 📊 Monthly expense analysis
- 📈 Excel report generation
- 🔐 Private bot with user authentication
- 💾 Supabase database integration

## Contributing

Found a bug or want to suggest a feature? Feel free to create an issue or submit a pull request!

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
