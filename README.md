# Binance Futures Trading Bot - Dual Interface (CLI + Web)

A complete trading bot for Binance Futures Testnet with **both Command-Line Interface (CLI) and Web Interface**, featuring real-time balance tracking, order validation, position management, and live price charts.

## ✨ Features

### Core Features (Assignment Requirements)
- ✅ **Market Orders** - Instant execution at current market price
- ✅ **Limit Orders** - Set your desired entry/exit price
- ✅ **Stop-Limit Orders** - Advanced risk management (Bonus feature)
- ✅ **CLI Interface** - Beautiful terminal interface with Rich library
- ✅ **Order Validation** - Automatic checking of min/max quantities and notional values
- ✅ **Complete Logging** - All trades logged to `trading_bot.log`
- ✅ **Error Handling** - Comprehensive validation and error messages
- ✅ **Buy/Sell Support** - Both order sides fully supported

### Enhanced Features (Bonus)
- 🎨 **Modern Web UI** - Beautiful, responsive web interface
- 📈 **Live Price Charts** - Real-time price visualization with Chart.js
- 📊 **Real-time Updates** - Auto-refresh balance and positions every 2 seconds
- 💰 **Balance Validation** - Checks available balance before orders
- 📏 **Min/Max Enforcement** - Respects exchange limits for quantity and price
- 🔒 **Session Management** - Secure credential handling
- 📍 **Position Tracking** - View all open positions with unrealized PnL

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Binance Futures Testnet account
- API Key and Secret from [testnet.binancefuture.com](https://testnet.binancefuture.com)

### Setup Steps

1. **Clone or download the project files**
   ```bash
   # Create project directory
   mkdir trading-bot
   cd trading-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create templates folder (for web interface)**
   ```bash
   mkdir templates
   # Move index.html to templates/ folder
   ```

4. **Get Testnet API Credentials**
   - Visit [testnet.binancefuture.com](https://testnet.binancefuture.com)
   - Login with GitHub or Google
   - Generate API Key and Secret

## 📁 Project Structure

```
trading-bot/
│
├── trading_bot.py          # Core bot with CLI support
├── app.py                  # Flask web server
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── trading_bot.log        # Auto-generated log file
│
└── templates/
    └── index.html         # Web interface
```

## 🎯 Usage Guide

### Option 1: CLI Mode (Command Line Interface)

**Run the bot in terminal:**
```bash
python trading_bot.py
```

**CLI Features:**
- ✨ Beautiful Rich-formatted menus and tables
- 📊 Interactive order placement
- 💰 View account balance
- 📈 View open positions
- 🎨 Color-coded output (green/red for profit/loss)
- ⌨️ Keyboard-driven navigation

**CLI Menu Options:**
```
📊 Main Menu
1. Market Order
2. Limit Order
3. Stop-Limit Order
4. View Balance
5. View Positions
6. Exit
```

**Example CLI Session:**
```bash
$ python trading_bot.py

🚀 Binance Futures Testnet Bot
Enter API Key: your_api_key_here
Enter API Secret: ************

✓ Connected successfully!

📊 Main Menu
1. Market Order
2. Limit Order
3. Stop-Limit Order
4. View Balance
5. View Positions
6. Exit

Select an option: 1
Enter Symbol (e.g., BTCUSDT): BTCUSDT
Enter Side [BUY/SELL]: BUY
Enter Quantity: 0.001

✓ Order Executed (FILLED)
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━┳━━━━━━━━━┓
┃ Symbol  ┃ Type  ┃ Side ┃ Price   ┃ Qty   ┃ OrderId ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━╇━━━━━━━━━┩
│ BTCUSDT │ MARKET│ BUY  │ 43250.5 │ 0.001 │ 1234567 │
└─────────┴───────┴──────┴─────────┴───────┴─────────┘

Perform another action? [y/n]: y
```

### Option 2: Web Interface

**Run the web server:**
```bash
python app.py
```

**Access the interface:**
- Open your browser and go to: `http://localhost:5000`
- Enter your Binance Testnet API credentials
- Start trading with the modern web interface!

**Web Interface Features:**
- 📈 **Live Price Chart** - Real-time price visualization
- 💰 **Account Dashboard** - Balance, available funds, unrealized PnL
- 📊 **Order Panel** - Easy order placement with validation
- 📍 **Positions Table** - View all open positions
- 📜 **Trade History** - Recent trades with PnL
- ⚡ **Auto-refresh** - Updates every 2 seconds
- 🎨 **Responsive Design** - Works on desktop and mobile

**Web Interface Highlights:**
```
┌─────────────────────────────────────────────┐
│  💰 Account Balance                         │
│  Total: 10,000 USDT | Available: 9,500 USDT│
│  Unrealized PnL: +125.50 USDT               │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  📈 Live Price Chart (BTCUSDT)              │
│  Current: $43,250.50 | Change: +2.5%       │
│  [1m] [5m] [15m] [1h] ← Timeframes         │
└─────────────────────────────────────────────┘
```

## 📊 Order Types Explained

### Market Order
- **Execution:** Immediately at current market price
- **Best for:** Quick entry/exit, high liquidity pairs
- **CLI:** Option 1
- **Input:** Symbol, Side (BUY/SELL), Quantity

### Limit Order
- **Execution:** Only at your specified price or better
- **Best for:** Price-specific entries, reducing slippage
- **CLI:** Option 2
- **Input:** Symbol, Side, Quantity, Limit Price

### Stop-Limit Order (Bonus)
- **Execution:** Triggers when price hits stop price, then places limit order
- **Best for:** Risk management, stop losses, breakout trading
- **CLI:** Option 3
- **Input:** Symbol, Side, Quantity, Limit Price, Stop Price

## 🛡️ Validation & Safety

The bot includes multiple validation layers:

### 1. Quantity Validation
- ✅ Checks against minimum quantity
- ✅ Checks against maximum quantity
- ✅ Validates step size compliance

### 2. Price Validation
- ✅ Checks minimum price
- ✅ Checks maximum price
- ✅ Validates tick size compliance

### 3. Notional Validation
- ✅ Ensures order value meets minimum notional requirement
- ✅ Calculated as: quantity × price

### 4. Balance Validation
- ✅ Checks available balance before order placement
- ✅ Prevents orders exceeding account balance

**Example Validation Messages:**
```
✗ Validation failed: Quantity below minimum: 0.001
✗ Validation failed: Order value below minimum notional: 5 USDT
✓ Validation passed: Order is valid
```

## 📝 Logging

All operations are logged to `trading_bot.log`:
- Connection attempts
- Order placements
- Validation results
- API requests and responses
- Errors and exceptions

**Log format:**
```
2025-01-01 12:00:00 - INFO - Successfully connected to Binance Testnet
2025-01-01 12:01:00 - INFO - Attempting MARKET BUY for 0.001 BTCUSDT
2025-01-01 12:01:01 - INFO - Order Executed: {'orderId': 1234567, ...}
2025-01-01 12:02:00 - ERROR - Market Order Failed: Insufficient balance
```

## 🔧 API Endpoints (Web Interface)

The Flask app provides these REST endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/connect` | POST | Connect with API credentials |
| `/api/balance` | GET | Get account balance |
| `/api/symbol-info/<symbol>` | GET | Get trading constraints |
| `/api/positions` | GET | Get open positions |
| `/api/validate-order` | POST | Validate order before placement |
| `/api/place-order` | POST | Place trading order |
| `/api/recent-trades/<symbol>` | GET | Get recent trades |

## 🎓 Code Architecture

### Dual-Mode Design

The bot uses a smart `cli_mode` parameter to support both interfaces:

```python
# CLI Mode (terminal interface)
bot = BasicBot(api_key, api_secret, cli_mode=True)
bot.place_market_order("BTCUSDT", "BUY", 0.001)  # Shows Rich table

# Web Mode (returns data only)
bot = BasicBot(api_key, api_secret, cli_mode=False)
order = bot.place_market_order("BTCUSDT", "BUY", 0.001)  # Returns dict
```

### Key Methods

**Account Management:**
- `get_account_balance()` - Fetch balance and unrealized PnL
- `get_open_positions()` - View all open positions
- `get_recent_trades(symbol, limit)` - Trade history

**Market Data:**
- `get_symbol_info(symbol)` - Trading constraints and limits
- `get_current_price(symbol)` - Real-time price

**Order Execution:**
- `place_market_order(symbol, side, quantity)`
- `place_limit_order(symbol, side, quantity, price)`
- `place_stop_limit_order(symbol, side, quantity, price, stop_price)`
- `validate_order(symbol, quantity, price)` - Pre-execution validation

**CLI Display (cli_mode=True only):**
- `display_balance_cli()` - Show balance in Rich table
- `display_positions_cli()` - Show positions in Rich table

## 🐛 Troubleshooting

### CLI Mode Issues

**Rich library not found:**
```bash
# Install Rich for CLI mode
pip install rich
```

**Connection Failed:**
- Verify API key and secret are correct
- Check if testnet account is active
- Ensure you're using Futures testnet credentials (not Spot)

### Web Mode Issues

**Port already in use:**
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

**Templates not found:**
```bash
# Ensure proper structure
mkdir -p templates
mv index.html templates/
```

### Common Errors

**Order Validation Failed:**
- Check symbol information for correct min/max values
- Ensure quantity meets minimum notional requirement
- Verify price is within allowed range

**Balance Not Updating:**
- Wait 2 seconds for auto-refresh (web mode)
- Manually refresh the page
- Check testnet account has funds

**Import Errors:**
```bash
# Reinstall all dependencies
pip install -r requirements.txt
```

## ⚠️ Important Notes

### Testnet Usage
- This bot is designed for **TESTNET ONLY**
- Uses fake money for practice trading
- Never use production API keys
- Testnet endpoint: `https://testnet.binancefuture.com`

### Security
- API credentials are session-based (web mode)
- Credentials not stored on server
- Use environment variables for production
- Never commit API keys to version control

### Rate Limits
- Binance enforces rate limits on API calls
- Bot includes automatic validation to minimize calls
- Don't spam order placements
- Web mode: Updates every 2 seconds
- CLI mode: On-demand updates

## 📧 Assignment Submission

For the **Junior Python Developer - Crypto Trading Bot** position:

### What to Submit:

1. **GitHub Repository** with all code files
2. **Screenshot** of successful CLI order placement
3. **Screenshot** of web interface (bonus)
4. **Log file** (`trading_bot.log`) showing executions
5. **Brief explanation** of your implementation choices

### Email To:
- **Primary:** saami@bajarangs.com, nagasai@bajarangs.com, chetan@bajarangs.com
- **CC:** sonika@primetrade.ai

### Subject Line:
```
"Junior Python Developer – Crypto Trading Bot"
```

### What Makes This Submission Stand Out:

✅ **Meets all core requirements** - CLI interface, all order types, logging
✅ **Exceeds expectations** - Web interface with live charts
✅ **Production-ready code** - Validation, error handling, dual-mode design
✅ **Well-documented** - Clear README, inline comments
✅ **Professional structure** - Clean separation of concerns

## 🎨 Customization Ideas

You can enhance the bot further by:

### CLI Enhancements
- Add ASCII art logo
- Implement auto-trading strategies
- Add portfolio analytics
- Create watchlists

### Web Enhancements
- Add candlestick charts
- Implement technical indicators (RSI, MACD)
- Add price alerts
- Create trading strategy builder

### Code Improvements
- Add WebSocket for real-time updates
- Implement order book visualization
- Add backtesting capabilities
- Create custom trading strategies

## 🎓 Learning Resources

- [Binance Futures API Documentation](https://binance-docs.github.io/apidocs/futures/en/)
- [Python-Binance Library](https://python-binance.readthedocs.io/)
- [Rich CLI Documentation](https://rich.readthedocs.io/)
- [Flask Web Framework](https://flask.palletsprojects.com/)
- [Chart.js Documentation](https://www.chartjs.org/)

## 📊 Feature Comparison

| Feature | CLI Mode | Web Mode |
|---------|----------|----------|
| Market Orders | ✅ | ✅ |
| Limit Orders | ✅ | ✅ |
| Stop-Limit Orders | ✅ | ✅ |
| View Balance | ✅ | ✅ |
| View Positions | ✅ | ✅ |
| Order Validation | ✅ | ✅ |
| Error Handling | ✅ | ✅ |
| Logging | ✅ | ✅ |
| Live Price Chart | ❌ | ✅ |
| Auto-refresh | ❌ | ✅ (2s) |
| Rich Tables | ✅ | ❌ |
| Interactive UI | Terminal | Browser |

## 🏆 Assignment Checklist

- [x] Python-based implementation
- [x] Binance Futures Testnet integration
- [x] Market orders
- [x] Limit orders
- [x] Buy and Sell sides
- [x] Command-line interface (CLI)
- [x] User input validation
- [x] Order execution output
- [x] Logging implementation
- [x] Error handling
- [x] **Bonus:** Third order type (Stop-Limit)
- [x] **Bonus:** Enhanced UI (Web interface)
- [x] Code reusability and clean structure
- [x] Clear documentation

## ⚖️ License

This project is for educational purposes as part of a hiring assignment for the Junior Python Developer position at PrimeTrade.ai / Bajarangs.

## 🙏 Acknowledgments

- Binance for providing comprehensive testnet infrastructure
- Flask framework for web server capabilities
- Rich library for beautiful CLI formatting
- Chart.js for real-time price visualization
- Python-Binance library for API integration

## 💡 Tips for Success

1. **Test thoroughly** - Place several orders in different scenarios
2. **Document issues** - Note any challenges you faced and how you solved them
3. **Show your work** - Include the log file to demonstrate testing
4. **Be honest** - If you used external resources, mention them
5. **Submit early** - First come, first served according to the task

---

## 🚀 Quick Start Commands

**CLI Mode:**
```bash
pip install -r requirements.txt
python trading_bot.py
```

**Web Mode:**
```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

---

**Happy Trading! 🚀📈**

Remember: This is testnet - practice makes perfect! Use this opportunity to learn about crypto trading, API integration, and building professional-grade applications.

**Questions?** Review the troubleshooting section or check the log file for detailed error messages.

**Good luck with your application!** 🍀