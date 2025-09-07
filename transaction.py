"""
Transaction class to represent individual financial transactions.
"""
from datetime import datetime
from typing import Dict, Any


class Transaction:
    """Represents a single financial transaction."""
    
    def __init__(self, date: str, description: str, amount: float, 
                 transaction_type: str, category: str = "General"):
        """
        Initialize a new transaction.
        
        Args:
            date: Transaction date in YYYY-MM-DD format
            description: Description of the transaction
            amount: Transaction amount (positive for income, negative for expenses)
            transaction_type: "Income" or "Expense"
            category: Transaction category (optional)
        """
        self.date = date
        self.description = description
        self.amount = float(amount)
        self.transaction_type = transaction_type
        self.category = category
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary for JSON storage."""
        return {
            'date': self.date,
            'description': self.description,
            'amount': self.amount,
            'type': self.transaction_type,
            'category': self.category
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """Create transaction from dictionary data."""
        return cls(
            date=data['date'],
            description=data['description'],
            amount=data['amount'],
            transaction_type=data['type'],
            category=data.get('category', 'General')
        )
    
    def __str__(self) -> str:
        """String representation of the transaction."""
        return f"{self.date} | {self.description} | ${self.amount:.2f} | {self.transaction_type} | {self.category}"