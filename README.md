# 💰 Personal Money Tracker

A comprehensive Python application for tracking personal finances with multi-user support, transaction management, and optional data visualization.

## ✨ Features

### Core Features
- **Multi-User Support**: Manage finances for multiple users (Father, Self, etc.)
- **Transaction Management**: Add, view, and categorize income and expenses
- **Smart Data Storage**: Persistent JSON storage with automatic file management
- **Balance Tracking**: Real-time balance calculations and summaries
- **Category Organization**: Organize expenses by categories (Food, Rent, Utilities, etc.)
- **Date Filtering**: Filter transactions by date ranges and types
- **Monthly Reports**: Generate detailed monthly financial reports

### Advanced Features
- **Data Visualization**: Optional charts and graphs using matplotlib
- **Category Analysis**: Detailed breakdown of spending by category
- **Balance History**: Track balance changes over time
- **Export Capabilities**: JSON data format for easy backup and transfer

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Optional: matplotlib for visualizations

### Installation

1. **Clone or download the files:**
   - `money_tracker.py` - Main application
   - `user.py` - User management
   - `transaction.py` - Transaction handling
   - `visualizer.py` - Optional visualization features

2. **Install optional dependencies for visualizations:**
   ```bash
   pip install matplotlib
   ```

3. **Run the application:**
   ```bash
   python money_tracker.py
   ```

## 📖 Usage Guide

### Main Menu Options

1. **👤 Select User**
   - Choose from existing users (Father, Self)
   - Add new users as needed
   - View current balance for each user

2. **➕ Add Transaction**
   - Enter date (defaults to today)
   - Add description
   - Specify amount
   - Choose type (Income/Expense)
   - Select category (for expenses)

3. **📊 View Transactions**
   - Display all transactions in table format
   - Filter by date range
   - Filter by transaction type
   - Sorted by date (newest first)

4. **💼 View Balance Summary**
   - Total income and expenses
   - Current balance
   - Transaction count
   - Balance status indicator

5. **📈 View Category Report**
   - Spending breakdown by category
   - Income vs expenses per category
   - Transaction counts

6. **📅 Monthly Report**
   - Monthly income and expenses
   - Net monthly amount
   - Transaction summary

7. **🚪 Exit**
   - Safely close the application
   - All data is automatically saved

### Data Storage

Each user's data is stored in separate JSON files:
- `father_transactions.json`
- `self_transactions.json`
- Custom user files as needed

Files include:
- Transaction details
- User information
- Last updated timestamp

## 🎨 Visualization Features

If matplotlib is installed, you can create various charts:

### Available Visualizations
1. **Income vs Expenses Bar Chart**
   - Monthly comparison over time
   - Customizable time period
   - Color-coded bars with value labels

2. **Category Pie Charts**
   - Spending breakdown by category
   - Separate charts for income and expenses
   - Percentage and dollar amounts

3. **Balance Over Time Line Chart**
   - Running balance history
   - Visual trend analysis
   - Zero-line reference

### Using Visualizations
Run the visualizer module directly:
```bash
python visualizer.py
```

Or integrate into the main application by adding visualization menu options.

## 📁 File Structure

```
money_tracker/
├── money_tracker.py    # Main application
├── user.py            # User management class
├── transaction.py     # Transaction handling
├── visualizer.py      # Optional visualization
├── README.md          # This file
└── *_transactions.json # User data files (auto-generated)
```

## 🔧 Configuration

### Categories
Default expense categories include:
- Food
- Rent
- Utilities
- Transportation
- Entertainment
- Healthcare
- Shopping
- Education
- Travel
- General

Categories can be customized in `money_tracker.py`.

### Date Format
All dates use YYYY-MM-DD format (ISO 8601 standard).

## 📊 Data Format

Transactions are stored in JSON format:
```json
{
  "user": "Username",
  "transactions": [
    {
      "date": "2024-01-15",
      "description": "Grocery shopping",
      "amount": -75.50,
      "type": "Expense",
      "category": "Food"
    }
  ],
  "last_updated": "2024-01-15T10:30:00"
}
```

## 🛠️ Customization

### Adding New Users
Users are automatically created when selected from the menu. Data files are generated automatically.

### Adding Categories
Modify the `categories` list in the `MoneyTracker` class initialization.

### Changing Data Storage
The application uses JSON by default. To use CSV or other formats, modify the `save_transactions()` and `load_transactions()` methods in the `User` class.

## 🔒 Data Security

- All data is stored locally on your machine
- No network connections or cloud storage
- JSON files can be backed up manually
- No sensitive data is logged or transmitted

## 🐛 Troubleshooting

### Common Issues

1. **Date Format Errors**
   - Ensure dates are in YYYY-MM-DD format
   - The app will default to today's date for invalid entries

2. **File Permission Errors**
   - Ensure the application directory is writable
   - Check file permissions for JSON data files

3. **Visualization Not Working**
   - Install matplotlib: `pip install matplotlib`
   - Ensure Python has GUI support for displaying charts

4. **Data Not Saving**
   - Check disk space
   - Verify directory write permissions
   - Look for error messages in the console

### Error Recovery
- Data files are automatically created if missing
- Invalid transactions are skipped during loading
- The application continues running even if individual operations fail

## 📈 Future Enhancements

Potential improvements for the application:
- Budget setting and tracking
- Recurring transaction support
- Data export to CSV/Excel
- Mobile-friendly web interface
- Backup and sync features
- Advanced reporting and analytics
- Integration with bank APIs
- Multi-currency support

## 🤝 Contributing

This is a standalone educational project. Feel free to:
- Modify the code for your needs
- Add new features
- Improve the user interface
- Enhance data visualization
- Add new export formats

## 📄 License

This project is provided as-is for educational and personal use.

---

**Enjoy tracking your finances! 💰📊**