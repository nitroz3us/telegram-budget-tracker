"""
Supabase Database Interface

This module handles all database operations for the Budget Tracker Bot using Supabase.
The Database class provides methods for:

- Managing starting balance (get/update)
- Adding new transactions
- Retrieving transaction history
- Generating monthly expense reports

Tables used:
- settings: Stores bot configuration (e.g., starting_balance)
- transactions: Stores all financial transactions with date, amount, category

All database interactions are encapsulated in this class to maintain
clean separation of concerns and consistent database operations.
"""

from supabase import create_client
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY

class Database:
    def __init__(self):
        self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
    def get_starting_balance(self):
        result = self.client.table('settings').select('value').eq('key', 'starting_balance').execute()
        if result.data and result.data[0]['value'] is not None:
            return float(result.data[0]['value'])
        return None
        
    def update_starting_balance(self, amount):
        return self.client.table('settings').update({'value': str(amount)}).eq('key', 'starting_balance').execute()
        
    def add_transaction(self, amount, category, description, running_balance):
        transaction = {
            "date": datetime.now().isoformat(),
            "amount": amount,
            "category": category,
            "description": description,
            "running_balance": running_balance
        }
        return self.client.table('transactions').insert(transaction).execute()
        
    def get_transactions(self):
        return self.client.table('transactions').select('*').order('date.desc').execute()
        
    def get_monthly_expenses(self, start_date, end_date):
        return self.client.table('transactions')\
            .select('*')\
            .lt('date', end_date)\
            .gte('date', start_date)\
            .lt('amount', 0)\
            .execute()

# Create a singleton instance
db = Database()