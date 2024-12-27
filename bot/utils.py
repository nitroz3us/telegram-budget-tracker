from openpyxl import load_workbook
import pandas as pd
from datetime import datetime
from decimal import Decimal

REQUIRED_COLUMNS = ['date', 'amount', 'category', 'description', 'running_balance', 'created_at']
VALID_CATEGORIES = ['Food', 'Transport', 'Shopping', 'Entertainment', 'Bills', 'Health', 'Income', 'Others']

def validate_import_data(df):
    errors = []
    
    # Check required columns
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        errors.append(f"Missing required columns: {', '.join(missing_cols)}")
    
    # Validate dates (both date and created_at)
    try:
        df['date'] = pd.to_datetime(df['date'])
        df['created_at'] = pd.to_datetime(df['created_at'])
    except Exception:
        errors.append("Invalid date format in 'date' or 'created_at' columns")
    
    # Validate amounts and running_balance
    if not pd.to_numeric(df['amount'], errors='coerce').notna().all():
        errors.append("Invalid amount values found")
    if not pd.to_numeric(df['running_balance'], errors='coerce').notna().all():
        errors.append("Invalid running_balance values found")
    
    # Validate categories
    invalid_categories = set(df['category']) - set(VALID_CATEGORIES)
    if invalid_categories:
        errors.append(f"Invalid categories found: {', '.join(invalid_categories)}")
    
    return errors

async def process_excel_import(file_path, db):
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Basic validation
        errors = validate_import_data(df)
        if errors:
            return False, "\n".join(errors)
        
        # Sort by date
        df = df.sort_values('date')
        
        successful_imports = 0
        
        for _, row in df.iterrows():
            # Convert row data to match database schema
            transaction = {
                "date": row['date'].isoformat(),
                "amount": float(row['amount']),
                "category": row['category'],
                "description": row['description'],
                "running_balance": float(row['running_balance']),
                "created_at": row['created_at'].isoformat()
            }
            
            # Add transaction to database
            result = db.client.table('transactions').insert(transaction).execute()
            if result.data:
                successful_imports += 1
        
        return True, f"Successfully imported {successful_imports} transactions"
        
    except Exception as e:
        return False, f"Error processing file: {str(e)}" 