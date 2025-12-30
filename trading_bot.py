import logging
import os
import sys
from binance.client import Client
from binance.exceptions import BinanceAPIException
from decimal import Decimal, ROUND_DOWN
import time

# Rich imports for CLI
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, FloatPrompt
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

class BasicBot:
    """
    Enhanced trading bot for Binance Futures Testnet with balance and limit checks.
    Supports both CLI and programmatic usage (for web interface).
    """

    def __init__(self, api_key, api_secret, cli_mode=False):
        # Configure Logging
        logging.basicConfig(
            filename='trading_bot.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger()
        self.cli_mode = cli_mode
        
        if self.cli_mode and RICH_AVAILABLE:
            console.print("[yellow]Connecting to Binance Futures Testnet...[/yellow]")
        
        try:
            # Initialize Client with Testnet=True
            self.client = Client(api_key, api_secret, testnet=True)
            self.client.API_URL = 'https://testnet.binancefuture.com'
            self.logger.info("Successfully connected to Binance Testnet")
            
            if self.cli_mode and RICH_AVAILABLE:
                console.print("[green]✓ Connected successfully![/green]")
        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            if self.cli_mode and RICH_AVAILABLE:
                console.print(f"[red]✗ Connection failed: {e}[/red]")
            raise Exception(f"Connection failed: {e}")

    def get_account_balance(self):
        """Get account balance and available funds."""
        try:
            account = self.client.futures_account()
            balance = {
                'total_wallet_balance': float(account.get('totalWalletBalance', 0)),
                'available_balance': float(account.get('availableBalance', 0)),
                'total_unrealized_profit': float(account.get('totalUnrealizedProfit', 0))
            }
            
            # Get individual asset balances
            assets = []
            for asset in account.get('assets', []):
                if float(asset['walletBalance']) > 0:
                    assets.append({
                        'asset': asset['asset'],
                        'wallet_balance': float(asset['walletBalance']),
                        'available_balance': float(asset['availableBalance'])
                    })
            
            balance['assets'] = assets
            self.logger.info(f"Account balance retrieved: {balance}")
            return balance
        except BinanceAPIException as e:
            self.logger.error(f"Failed to get balance: {e}")
            raise Exception(f"Failed to get balance: {e}")

    def get_symbol_info(self, symbol):
        """Get trading limits and constraints for a symbol."""
        try:
            exchange_info = self.client.futures_exchange_info()
            
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    filters = {}
                    for f in s['filters']:
                        if f['filterType'] == 'PRICE_FILTER':
                            filters['min_price'] = float(f['minPrice'])
                            filters['max_price'] = float(f['maxPrice'])
                            filters['tick_size'] = float(f['tickSize'])
                        elif f['filterType'] == 'LOT_SIZE':
                            filters['min_qty'] = float(f['minQty'])
                            filters['max_qty'] = float(f['maxQty'])
                            filters['step_size'] = float(f['stepSize'])
                        elif f['filterType'] == 'MIN_NOTIONAL':
                            filters['min_notional'] = float(f['notional'])
                    
                    filters['price_precision'] = s['pricePrecision']
                    filters['quantity_precision'] = s['quantityPrecision']
                    
                    self.logger.info(f"Symbol info for {symbol}: {filters}")
                    return filters
            
            raise Exception(f"Symbol {symbol} not found")
        except BinanceAPIException as e:
            self.logger.error(f"Failed to get symbol info: {e}")
            raise Exception(f"Failed to get symbol info: {e}")

    def get_current_price(self, symbol):
        """Get current market price for a symbol."""
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            self.logger.info(f"Current price for {symbol}: {price}")
            return price
        except BinanceAPIException as e:
            self.logger.error(f"Failed to get price for {symbol}: {e}")
            raise Exception(f"Failed to get price: {e}")

    def validate_order(self, symbol, quantity, price=None):
        """Validate order parameters against symbol constraints."""
        try:
            symbol_info = self.get_symbol_info(symbol)
            current_price = price if price else self.get_current_price(symbol)
            
            # Check minimum quantity
            if quantity < symbol_info['min_qty']:
                return False, f"Quantity below minimum: {symbol_info['min_qty']}"
            
            # Check maximum quantity
            if quantity > symbol_info['max_qty']:
                return False, f"Quantity above maximum: {symbol_info['max_qty']}"
            
            # Check step size
            qty_decimal = Decimal(str(quantity))
            step_decimal = Decimal(str(symbol_info['step_size']))
            if (qty_decimal % step_decimal) != 0:
                return False, f"Quantity must be multiple of step size: {symbol_info['step_size']}"
            
            # Check minimum notional value
            notional = quantity * current_price
            if 'min_notional' in symbol_info and notional < symbol_info['min_notional']:
                return False, f"Order value below minimum notional: {symbol_info['min_notional']} USDT"
            
            # Check price constraints if limit order
            if price:
                if price < symbol_info['min_price']:
                    return False, f"Price below minimum: {symbol_info['min_price']}"
                if price > symbol_info['max_price']:
                    return False, f"Price above maximum: {symbol_info['max_price']}"
            
            return True, "Valid"
        except Exception as e:
            return False, str(e)

    def get_open_positions(self):
        """Get all open positions."""
        try:
            positions = self.client.futures_position_information()
            open_positions = []
            
            for pos in positions:
                position_amt = float(pos['positionAmt'])
                if position_amt != 0:
                    open_positions.append({
                        'symbol': pos['symbol'],
                        'position_amt': position_amt,
                        'entry_price': float(pos['entryPrice']),
                        'unrealized_profit': float(pos['unRealizedProfit']),
                        'leverage': int(pos['leverage'])
                    })
            
            self.logger.info(f"Open positions: {open_positions}")
            return open_positions
        except BinanceAPIException as e:
            self.logger.error(f"Failed to get positions: {e}")
            raise Exception(f"Failed to get positions: {e}")

    def _display_order_cli(self, order):
        """Display order details in CLI mode using Rich."""
        if not self.cli_mode or not RICH_AVAILABLE:
            return
            
        table = Table(title=f"✓ Order Executed ({order.get('status', 'UNKNOWN')})")
        table.add_column("Symbol", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Side", style="green")
        table.add_column("Price", style="yellow")
        table.add_column("Qty", style="white")
        table.add_column("OrderId", style="blue")

        # Handling different price keys for Market vs Limit orders
        price = order.get('avgPrice', '0') if order['type'] == 'MARKET' else order.get('price', '0')

        table.add_row(
            order['symbol'],
            order['type'],
            order['side'],
            str(price),
            str(order['origQty']),
            str(order['orderId'])
        )
        console.print(table)

    def place_market_order(self, symbol, side, quantity):
        """Places a Market Order with validation."""
        try:
            # Validate order
            is_valid, message = self.validate_order(symbol, quantity)
            if not is_valid:
                if self.cli_mode and RICH_AVAILABLE:
                    console.print(f"[red]✗ Validation failed: {message}[/red]")
                raise Exception(f"Order validation failed: {message}")
            
            self.logger.info(f"Attempting MARKET {side} for {quantity} {symbol}")
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            self.logger.info(f"Order Executed: {order}")
            
            if self.cli_mode:
                self._display_order_cli(order)
            
            return order
        except BinanceAPIException as e:
            self.logger.error(f"Market Order Failed: {e}")
            if self.cli_mode and RICH_AVAILABLE:
                console.print(f"[red]✗ Market Order Failed: {e}[/red]")
            raise Exception(f"Market Order Failed: {e}")

    def place_limit_order(self, symbol, side, quantity, price):
        """Places a Limit Order with validation."""
        try:
            # Validate order
            is_valid, message = self.validate_order(symbol, quantity, price)
            if not is_valid:
                if self.cli_mode and RICH_AVAILABLE:
                    console.print(f"[red]✗ Validation failed: {message}[/red]")
                raise Exception(f"Order validation failed: {message}")
            
            self.logger.info(f"Attempting LIMIT {side} for {quantity} {symbol} at {price}")
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price
            )
            self.logger.info(f"Order Executed: {order}")
            
            if self.cli_mode:
                self._display_order_cli(order)
            
            return order
        except BinanceAPIException as e:
            self.logger.error(f"Limit Order Failed: {e}")
            if self.cli_mode and RICH_AVAILABLE:
                console.print(f"[red]✗ Limit Order Failed: {e}[/red]")
            raise Exception(f"Limit Order Failed: {e}")

    def place_stop_limit_order(self, symbol, side, quantity, price, stop_price):
        """Places a Stop-Limit Order with validation."""
        try:
            # Validate order
            is_valid, message = self.validate_order(symbol, quantity, price)
            if not is_valid:
                if self.cli_mode and RICH_AVAILABLE:
                    console.print(f"[red]✗ Validation failed: {message}[/red]")
                raise Exception(f"Order validation failed: {message}")
            
            self.logger.info(f"Attempting STOP_LIMIT {side} for {quantity} {symbol}. Stop: {stop_price}, Limit: {price}")
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                timeInForce='GTC',
                quantity=quantity,
                price=price,
                stopPrice=stop_price
            )
            self.logger.info(f"Order Executed: {order}")
            
            if self.cli_mode:
                self._display_order_cli(order)
            
            return order
        except BinanceAPIException as e:
            self.logger.error(f"Stop-Limit Order Failed: {e}")
            if self.cli_mode and RICH_AVAILABLE:
                console.print(f"[red]✗ Stop-Limit Order Failed: {e}[/red]")
            raise Exception(f"Stop-Limit Order Failed: {e}")

    def get_recent_trades(self, symbol, limit=10):
        """Get recent trades for a symbol."""
        try:
            trades = self.client.futures_account_trades(symbol=symbol, limit=limit)
            return trades
        except BinanceAPIException as e:
            self.logger.error(f"Failed to get trades: {e}")
            raise Exception(f"Failed to get trades: {e}")

    def display_balance_cli(self):
        """Display account balance in CLI mode."""
        if not self.cli_mode or not RICH_AVAILABLE:
            return
            
        try:
            balance = self.get_account_balance()
            
            table = Table(title="💰 Account Balance")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Total Balance", f"{balance['total_wallet_balance']:.2f} USDT")
            table.add_row("Available Balance", f"{balance['available_balance']:.2f} USDT")
            
            pnl = balance['total_unrealized_profit']
            pnl_color = "green" if pnl >= 0 else "red"
            table.add_row("Unrealized PnL", f"[{pnl_color}]{pnl:.2f} USDT[/{pnl_color}]")
            
            console.print(table)
        except Exception as e:
            console.print(f"[red]Failed to get balance: {e}[/red]")

    def display_positions_cli(self):
        """Display open positions in CLI mode."""
        if not self.cli_mode or not RICH_AVAILABLE:
            return
            
        try:
            positions = self.get_open_positions()
            
            if not positions:
                console.print("[yellow]No open positions[/yellow]")
                return
            
            table = Table(title="📈 Open Positions")
            table.add_column("Symbol", style="cyan")
            table.add_column("Size", style="white")
            table.add_column("Entry Price", style="yellow")
            table.add_column("Unrealized PnL", style="magenta")
            table.add_column("Leverage", style="blue")
            
            for pos in positions:
                pnl = pos['unrealized_profit']
                pnl_color = "green" if pnl >= 0 else "red"
                
                table.add_row(
                    pos['symbol'],
                    str(pos['position_amt']),
                    str(pos['entry_price']),
                    f"[{pnl_color}]{pnl:.2f}[/{pnl_color}]",
                    f"{pos['leverage']}x"
                )
            
            console.print(table)
        except Exception as e:
            console.print(f"[red]Failed to get positions: {e}[/red]")


# CLI-specific functions
def get_user_input():
    """
    Handles User Input via CLI.
    """
    if not RICH_AVAILABLE:
        print("Rich library not available. Install with: pip install rich")
        sys.exit(1)
        
    while True:
        console.print(Panel.fit(
            "1. Market Order\n"
            "2. Limit Order\n"
            "3. Stop-Limit Order\n"
            "4. View Balance\n"
            "5. View Positions\n"
            "6. Exit",
            title="📊 Main Menu"
        ))
        
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6"])

        if choice == "6":
            console.print("[yellow]👋 Exiting Bot...[/yellow]")
            sys.exit(0)
        
        if choice == "4":
            return choice, None, None, None
        
        if choice == "5":
            return choice, None, None, None

        # Common inputs for order types
        symbol = Prompt.ask("Enter Symbol (e.g., BTCUSDT)").upper()
        side = Prompt.ask("Enter Side", choices=["BUY", "SELL"]).upper() 
        quantity = FloatPrompt.ask("Enter Quantity")

        return choice, symbol, side, quantity


def main():
    """
    Main function for CLI mode.
    """
    if not RICH_AVAILABLE:
        print("Error: Rich library is required for CLI mode.")
        print("Install with: pip install rich")
        sys.exit(1)
    
    # Credentials Input
    console.print(Panel("🚀 Binance Futures Testnet Bot", subtitle="Enter API Credentials", style="bold blue"))
    api_key = Prompt.ask("Enter API Key")
    api_secret = Prompt.ask("Enter API Secret", password=True)

    bot = BasicBot(api_key, api_secret, cli_mode=True)

    # CLI Loop
    while True:
        try:
            choice, symbol, side, qty = get_user_input()

            if choice == "1":
                bot.place_market_order(symbol, side, qty)
            elif choice == "2":
                price = FloatPrompt.ask("Enter Limit Price")
                bot.place_limit_order(symbol, side, qty, price)
            elif choice == "3":
                price = FloatPrompt.ask("Enter Limit Price")
                stop_price = FloatPrompt.ask("Enter Stop Trigger Price")
                bot.place_stop_limit_order(symbol, side, qty, price, stop_price)
            elif choice == "4":
                bot.display_balance_cli()
            elif choice == "5":
                bot.display_positions_cli()
            
            if not Prompt.ask("Perform another action?", choices=["y", "n"]) == "y":
                break

        except KeyboardInterrupt:
            console.print("\n[yellow]Bot stopped by user.[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Unexpected Error: {e}[/red]")


if __name__ == "__main__":
    main()