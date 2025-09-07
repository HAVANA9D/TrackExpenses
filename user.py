"""
User class to manage individual user data and transactions.
"""
import json
import os
from typing import List, Optional
from datetime import datetime
from transaction import Transaction


class User:
    """Manages transactions and data for a single user."""
    
    def __init__(self, name: str):
        """
        Initialize a new user.
        
        Args:
            name: User's name (used for file naming)
        """
        self.name = name
        self.transactions: List[Transaction] = []
        self.data_file = f"{name.lower().replace(' ', '_')}_transactions.json"
        self.load_transactions()
    
    def add_transaction(self, date: str, description: str, amount: float, 
                       transaction_type: str, category: str = "General"):
        """Add a new transaction for this user."""
        # Convert expense amounts to negative for easier calculations
        if transaction_type.lower() == "expense" and amount > 0:
            amount = -amount
        elif transaction_type.lower() == "income" and amount < 0:
            amount = abs(amount)
        
        transaction = Transaction(date, description, amount, transaction_type, category)
        self.transactions.append(transaction)
        self.save_transactions()
    
    def get_transactions(self, start_date: Optional[str] = None, 
                        end_date: Optional[str] = None, 
                        transaction_type: Optional[str] = None) -> List[Transaction]:
        """
        Get filtered transactions.
        
        Args:
            start_date: Filter from this date (YYYY-MM-DD)
            end_date: Filter to this date (YYYY-MM-DD)
            transaction_type: Filter by type ("Income" or "Expense")
        """
        filtered = self.transactions
        
        if start_date:
            filtered = [t for t in filtered if t.date >= start_date]
        
        if end_date:
            filtered = [t for t in filtered if t.date <= end_date]
        
        if transaction_type:
            filtered = [t for t in filtered if t.transaction_type.lower() == transaction_type.lower()]
        
        # Sort by date (newest first)
        return sorted(filtered, key=lambda x: x.date, reverse=True)
    
    def get_balance_summary(self) -> dict:
        """Calculate and return balance summary."""
        total_income = sum(t.amount for t in self.transactions if t.amount > 0)
        total_expenses = abs(sum(t.amount for t in self.transactions if t.amount < 0))
        current_balance = total_income - total_expenses
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'current_balance': current_balance,
            'transaction_count': len(self.transactions)
        }
    
    def get_category_summary(self) -> dict:
        """Get summary by category."""
        categories = {}
        for transaction in self.transactions:
            category = transaction.category
            if category not in categories:
                categories[category] = {'income': 0, 'expenses': 0, 'count': 0}
            
            if transaction.amount > 0:
                categories[category]['income'] += transaction.amount
            else:
                categories[category]['expenses'] += abs(transaction.amount)
            
            categories[category]['count'] += 1
        
        return categories
    
    def save_transactions(self):
        """Save transactions to JSON file."""
        try:
            data = {
                'user': self.name,
                'transactions': [t.to_dict() for t in self.transactions],
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=2)
        except Exception as e:
            print(f"Error saving transactions: {e}")
    
    def load_transactions(self):
        """Load transactions from JSON file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    self.transactions = [Transaction.from_dict(t) for t in data.get('transactions', [])]
        except Exception as e:
            print(f"Error loading transactions: {e}")
            self.transactions = []