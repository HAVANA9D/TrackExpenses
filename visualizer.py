"""
Optional visualization module for generating charts and graphs.
Requires matplotlib to be installed: pip install matplotlib
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from collections import defaultdict
from typing import List
from user import User


class TransactionVisualizer:
    """Create visual representations of financial data."""
    
    def __init__(self, user: User):
        """Initialize visualizer with user data."""
        self.user = user
    
    def plot_income_vs_expenses(self, months: int = 12):
        """
        Create a bar chart comparing income vs expenses over time.
        
        Args:
            months: Number of months to include in the chart
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("❌ Matplotlib is required for visualization.")
            print("Install it with: pip install matplotlib")
            return
        
        # Group transactions by month
        monthly_data = defaultdict(lambda: {'income': 0, 'expenses': 0})
        
        for transaction in self.user.transactions:
            date_obj = datetime.strptime(transaction.date, "%Y-%m-%d")
            month_key = date_obj.strftime("%Y-%m")
            
            if transaction.amount > 0:
                monthly_data[month_key]['income'] += transaction.amount
            else:
                monthly_data[month_key]['expenses'] += abs(transaction.amount)
        
        # Prepare data for plotting
        months_list = sorted(monthly_data.keys())[-months:]
        income_data = [monthly_data[month]['income'] for month in months_list]
        expense_data = [monthly_data[month]['expenses'] for month in months_list]
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 6))
        x_pos = range(len(months_list))
        
        bars1 = ax.bar([x - 0.2 for x in x_pos], income_data, 0.4, 
                      label='Income', color='green', alpha=0.7)
        bars2 = ax.bar([x + 0.2 for x in x_pos], expense_data, 0.4, 
                      label='Expenses', color='red', alpha=0.7)
        
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')
        ax.set_title(f'Income vs Expenses - {self.user.name}')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(months_list, rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:.0f}', ha='center', va='bottom')
        
        for bar in bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:.0f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
    
    def plot_category_pie_chart(self, transaction_type: str = "Expense"):
        """
        Create a pie chart showing spending by category.
        
        Args:
            transaction_type: "Income" or "Expense"
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("❌ Matplotlib is required for visualization.")
            return
        
        # Get category data
        categories = self.user.get_category_summary()
        
        if transaction_type.lower() == "expense":
            data = {cat: info['expenses'] for cat, info in categories.items() if info['expenses'] > 0}
            title = f"Expenses by Category - {self.user.name}"
        else:
            data = {cat: info['income'] for cat, info in categories.items() if info['income'] > 0}
            title = f"Income by Category - {self.user.name}"
        
        if not data:
            print(f"❌ No {transaction_type.lower()} data found for visualization.")
            return
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(10, 8))
        
        labels = list(data.keys())
        sizes = list(data.values())
        colors = plt.cm.Set3(range(len(labels)))
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                         colors=colors, startangle=90)
        
        # Beautify the chart
        ax.set_title(title, fontsize=16, fontweight='bold')
        
        # Add legend with values
        legend_labels = [f'{label}: ${value:.2f}' for label, value in data.items()]
        ax.legend(wedges, legend_labels, title="Categories", loc="center left", 
                 bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.tight_layout()
        plt.show()
    
    def plot_balance_over_time(self):
        """Create a line chart showing balance changes over time."""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
        except ImportError:
            print("❌ Matplotlib is required for visualization.")
            return
        
        # Sort transactions by date
        sorted_transactions = sorted(self.user.transactions, key=lambda x: x.date)
        
        if not sorted_transactions:
            print("❌ No transactions found for visualization.")
            return
        
        # Calculate running balance
        dates = []
        balances = []
        running_balance = 0
        
        for transaction in sorted_transactions:
            running_balance += transaction.amount
            dates.append(datetime.strptime(transaction.date, "%Y-%m-%d"))
            balances.append(running_balance)
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dates, balances, linewidth=2, marker='o', markersize=4)
        
        # Format the plot
        ax.set_xlabel('Date')
        ax.set_ylabel('Balance ($)')
        ax.set_title(f'Balance Over Time - {self.user.name}')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.xticks(rotation=45)
        
        # Add horizontal line at zero
        ax.axhline(y=0, color='red', linestyle='--', alpha=0.7)
        
        # Color the area
        ax.fill_between(dates, balances, alpha=0.3, 
                       color='green' if balances[-1] >= 0 else 'red')
        
        plt.tight_layout()
        plt.show()


def create_visualization_menu(user: User):
    """Interactive menu for creating visualizations."""
    visualizer = TransactionVisualizer(user)
    
    while True:
        print(f"\n📊 Visualization Menu for {user.name}")
        print("="*40)
        print("1. Income vs Expenses Chart")
        print("2. Category Pie Chart (Expenses)")
        print("3. Category Pie Chart (Income)")
        print("4. Balance Over Time")
        print("5. Back to Main Menu")
        
        choice = input("\nSelect visualization (1-5): ").strip()
        
        if choice == '1':
            months = input("Number of months to show (default 12): ").strip()
            months = int(months) if months.isdigit() else 12
            visualizer.plot_income_vs_expenses(months)
        elif choice == '2':
            visualizer.plot_category_pie_chart("Expense")
        elif choice == '3':
            visualizer.plot_category_pie_chart("Income")
        elif choice == '4':
            visualizer.plot_balance_over_time()
        elif choice == '5':
            break
        else:
            print("❌ Invalid choice!")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    # Example usage
    user = User("Test User")
    create_visualization_menu(user)