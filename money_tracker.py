"""
Main Money Tracker Application
A comprehensive financial tracking system with multi-user support.
"""
import os
from datetime import datetime
from typing import List, Optional
from user import User


class MoneyTracker:
    """Main application class for the Money Tracker."""
    
    def __init__(self):
        """Initialize the Money Tracker application."""
        self.users = {
            "Father": User("Father"),
            "Self": User("Self")
        }
        self.current_user: Optional[User] = None
        
        # Common expense categories
        self.categories = [
            "Food", "Rent", "Utilities", "Transportation", "Entertainment",
            "Healthcare", "Shopping", "Education", "Travel", "General"
        ]
    
    def display_header(self):
        """Display the application header."""
        print("\n" + "="*60)
        print("           💰 PERSONAL MONEY TRACKER 💰")
        print("="*60)
        if self.current_user:
            balance = self.current_user.get_balance_summary()
            print(f"Current User: {self.current_user.name}")
            print(f"Balance: ${balance['current_balance']:.2f}")
        print("="*60)
    
    def display_menu(self):
        """Display the main menu options."""
        print("\n📋 MAIN MENU:")
        print("1. 👤 Select User")
        print("2. ➕ Add Transaction")
        print("3. 📊 View Transactions")
        print("4. 💼 View Balance Summary")
        print("5. 📈 View Category Report")
        print("6. 📅 Monthly Report")
        print("7. 🚪 Exit")
        print("-" * 30)
    
    def select_user(self):
        """Allow user selection from available users."""
        print("\n👥 Available Users:")
        user_list = list(self.users.keys())
        
        for i, user_name in enumerate(user_list, 1):
            balance = self.users[user_name].get_balance_summary()
            print(f"{i}. {user_name} (Balance: ${balance['current_balance']:.2f})")
        
        print(f"{len(user_list) + 1}. Add New User")
        
        try:
            choice = int(input("\nSelect user (number): "))
            
            if 1 <= choice <= len(user_list):
                selected_user = user_list[choice - 1]
                self.current_user = self.users[selected_user]
                print(f"✅ Selected user: {selected_user}")
            elif choice == len(user_list) + 1:
                self.add_new_user()
            else:
                print("❌ Invalid selection!")
                
        except ValueError:
            print("❌ Please enter a valid number!")
    
    def add_new_user(self):
        """Add a new user to the system."""
        name = input("Enter new user name: ").strip()
        if name and name not in self.users:
            self.users[name] = User(name)
            print(f"✅ User '{name}' added successfully!")
        elif name in self.users:
            print("❌ User already exists!")
        else:
            print("❌ Invalid user name!")
    
    def add_transaction(self):
        """Add a new transaction for the current user."""
        if not self.current_user:
            print("❌ Please select a user first!")
            return
        
        print(f"\n💳 Adding transaction for {self.current_user.name}")
        
        # Get date (default to today)
        date_input = input(f"Date (YYYY-MM-DD, press Enter for today): ").strip()
        if not date_input:
            date_input = datetime.now().strftime("%Y-%m-%d")
        
        # Validate date format
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid date format! Using today's date.")
            date_input = datetime.now().strftime("%Y-%m-%d")
        
        # Get description
        description = input("Description: ").strip()
        if not description:
            print("❌ Description is required!")
            return
        
        # Get amount
        try:
            amount = float(input("Amount: $"))
            if amount <= 0:
                print("❌ Amount must be positive!")
                return
        except ValueError:
            print("❌ Invalid amount!")
            return
        
        # Get transaction type
        print("\nTransaction Type:")
        print("1. Income")
        print("2. Expense")
        
        try:
            type_choice = int(input("Select type (1 or 2): "))
            if type_choice == 1:
                transaction_type = "Income"
            elif type_choice == 2:
                transaction_type = "Expense"
            else:
                print("❌ Invalid selection!")
                return
        except ValueError:
            print("❌ Invalid selection!")
            return
        
        # Get category (only for expenses)
        category = "General"
        if transaction_type == "Expense":
            print(f"\n📂 Categories:")
            for i, cat in enumerate(self.categories, 1):
                print(f"{i}. {cat}")
            
            try:
                cat_choice = int(input("Select category (number): "))
                if 1 <= cat_choice <= len(self.categories):
                    category = self.categories[cat_choice - 1]
            except ValueError:
                pass  # Use default category
        
        # Add the transaction
        self.current_user.add_transaction(date_input, description, amount, transaction_type, category)
        print(f"✅ Transaction added successfully!")
        
        # Show updated balance
        balance = self.current_user.get_balance_summary()
        print(f"💰 New balance: ${balance['current_balance']:.2f}")
    
    def view_transactions(self):
        """Display transactions with optional filtering."""
        if not self.current_user:
            print("❌ Please select a user first!")
            return
        
        print(f"\n📊 Transactions for {self.current_user.name}")
        
        # Optional filtering
        print("\nFilter options (press Enter to skip):")
        start_date = input("Start date (YYYY-MM-DD): ").strip() or None
        end_date = input("End date (YYYY-MM-DD): ").strip() or None
        
        print("Transaction type:")
        print("1. All")
        print("2. Income only")
        print("3. Expenses only")
        
        try:
            filter_choice = int(input("Select (1-3): "))
            if filter_choice == 2:
                transaction_type = "Income"
            elif filter_choice == 3:
                transaction_type = "Expense"
            else:
                transaction_type = None
        except ValueError:
            transaction_type = None
        
        # Get filtered transactions
        transactions = self.current_user.get_transactions(start_date, end_date, transaction_type)
        
        if not transactions:
            print("📭 No transactions found with the specified filters.")
            return
        
        # Display transactions in table format
        print("\n" + "="*90)
        print(f"{'Date':<12} {'Description':<25} {'Amount':<12} {'Type':<10} {'Category':<15}")
        print("="*90)
        
        for transaction in transactions:
            amount_str = f"${abs(transaction.amount):.2f}"
            print(f"{transaction.date:<12} {transaction.description[:24]:<25} "
                  f"{amount_str:<12} {transaction.transaction_type:<10} {transaction.category:<15}")
        
        print("="*90)
        print(f"Total transactions shown: {len(transactions)}")
    
    def view_balance_summary(self):
        """Display detailed balance summary."""
        if not self.current_user:
            print("❌ Please select a user first!")
            return
        
        summary = self.current_user.get_balance_summary()
        
        print(f"\n💼 Balance Summary for {self.current_user.name}")
        print("="*40)
        print(f"💚 Total Income:     ${summary['total_income']:.2f}")
        print(f"💸 Total Expenses:   ${summary['total_expenses']:.2f}")
        print("-" * 40)
        print(f"💰 Current Balance:  ${summary['current_balance']:.2f}")
        print(f"📊 Total Transactions: {summary['transaction_count']}")
        print("="*40)
        
        # Show balance status
        if summary['current_balance'] > 0:
            print("✅ You're in the positive!")
        elif summary['current_balance'] < 0:
            print("⚠️  Warning: Negative balance!")
        else:
            print("⚖️  Balanced")
    
    def view_category_report(self):
        """Display spending by category."""
        if not self.current_user:
            print("❌ Please select a user first!")
            return
        
        categories = self.current_user.get_category_summary()
        
        if not categories:
            print("📭 No transactions found.")
            return
        
        print(f"\n📈 Category Report for {self.current_user.name}")
        print("="*70)
        print(f"{'Category':<15} {'Income':<12} {'Expenses':<12} {'Net':<12} {'Count':<8}")
        print("="*70)
        
        for category, data in sorted(categories.items()):
            net_amount = data['income'] - data['expenses']
            print(f"{category:<15} ${data['income']:<11.2f} "
                  f"${data['expenses']:<11.2f} ${net_amount:<11.2f} {data['count']:<8}")
        
        print("="*70)
    
    def monthly_report(self):
        """Display monthly spending report."""
        if not self.current_user:
            print("❌ Please select a user first!")
            return
        
        # Get year and month
        try:
            year = int(input("Enter year (YYYY): ") or datetime.now().year)
            month = int(input("Enter month (MM): ") or datetime.now().month)
        except ValueError:
            print("❌ Invalid date input!")
            return
        
        # Filter transactions for the specified month
        start_date = f"{year:04d}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1:04d}-01-01"
        else:
            end_date = f"{year:04d}-{month+1:02d}-01"
        
        transactions = self.current_user.get_transactions(start_date, end_date)
        
        if not transactions:
            print(f"📭 No transactions found for {year}-{month:02d}")
            return
        
        # Calculate monthly summary
        monthly_income = sum(t.amount for t in transactions if t.amount > 0)
        monthly_expenses = abs(sum(t.amount for t in transactions if t.amount < 0))
        monthly_net = monthly_income - monthly_expenses
        
        print(f"\n📅 Monthly Report for {year}-{month:02d}")
        print("="*40)
        print(f"💚 Income:    ${monthly_income:.2f}")
        print(f"💸 Expenses:  ${monthly_expenses:.2f}")
        print(f"💰 Net:       ${monthly_net:.2f}")
        print(f"📊 Transactions: {len(transactions)}")
        print("="*40)
    
    def run(self):
        """Main application loop."""
        print("🚀 Welcome to Personal Money Tracker!")
        print("Manage your finances with ease and precision.")
        
        while True:
            try:
                self.display_header()
                self.display_menu()
                
                choice = input("Enter your choice (1-7): ").strip()
                
                if choice == '1':
                    self.select_user()
                elif choice == '2':
                    self.add_transaction()
                elif choice == '3':
                    self.view_transactions()
                elif choice == '4':
                    self.view_balance_summary()
                elif choice == '5':
                    self.view_category_report()
                elif choice == '6':
                    self.monthly_report()
                elif choice == '7':
                    print("\n👋 Thank you for using Money Tracker!")
                    print("💾 All data has been saved automatically.")
                    break
                else:
                    print("❌ Invalid choice! Please select 1-7.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")


if __name__ == "__main__":
    app = MoneyTracker()
    app.run()