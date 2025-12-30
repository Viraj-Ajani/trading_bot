from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import trading_bot
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
CORS(app)

# Store bot instances per session (in production, use Redis or similar)
bot_instances = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/connect', methods=['POST'])
def connect():
    """Connect to Binance with API credentials."""
    try:
        data = request.json
        api_key = data.get('api_key')
        api_secret = data.get('api_secret')
        
        if not api_key or not api_secret:
            return jsonify({'success': False, 'error': 'API credentials required'}), 400
        
        # Create bot instance
        bot = trading_bot.BasicBot(api_key, api_secret)
        
        # Store in session
        session_id = os.urandom(16).hex()
        bot_instances[session_id] = bot
        session['bot_id'] = session_id
        
        # Get initial balance
        balance = bot.get_account_balance()
        
        return jsonify({
            'success': True,
            'balance': balance,
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/balance', methods=['GET'])
def get_balance():
    """Get account balance."""
    try:
        bot = get_bot_instance()
        balance = bot.get_account_balance()
        return jsonify({'success': True, 'balance': balance})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/symbol-info/<symbol>', methods=['GET'])
def get_symbol_info(symbol):
    """Get trading constraints for a symbol."""
    try:
        bot = get_bot_instance()
        info = bot.get_symbol_info(symbol.upper())
        current_price = bot.get_current_price(symbol.upper())
        
        return jsonify({
            'success': True,
            'info': info,
            'current_price': current_price
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/positions', methods=['GET'])
def get_positions():
    """Get open positions."""
    try:
        bot = get_bot_instance()
        positions = bot.get_open_positions()
        return jsonify({'success': True, 'positions': positions})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/validate-order', methods=['POST'])
def validate_order():
    """Validate order before placing."""
    try:
        bot = get_bot_instance()
        data = request.json
        
        symbol = data.get('symbol', '').upper()
        quantity = float(data.get('quantity'))
        price = float(data.get('price')) if data.get('price') else None
        
        is_valid, message = bot.validate_order(symbol, quantity, price)
        
        return jsonify({
            'success': True,
            'valid': is_valid,
            'message': message
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/place-order', methods=['POST'])
def place_order():
    """Place a trading order."""
    try:
        bot = get_bot_instance()
        data = request.json
        
        order_type = data.get('order_type')
        symbol = data.get('symbol', '').upper()
        side = data.get('side', '').upper()
        quantity = float(data.get('quantity'))
        
        if order_type == 'MARKET':
            order = bot.place_market_order(symbol, side, quantity)
        elif order_type == 'LIMIT':
            price = float(data.get('price'))
            order = bot.place_limit_order(symbol, side, quantity, price)
        elif order_type == 'STOP_LIMIT':
            price = float(data.get('price'))
            stop_price = float(data.get('stop_price'))
            order = bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
        else:
            return jsonify({'success': False, 'error': 'Invalid order type'}), 400
        
        return jsonify({
            'success': True,
            'order': order
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/recent-trades/<symbol>', methods=['GET'])
def get_recent_trades(symbol):
    """Get recent trades for a symbol."""
    try:
        bot = get_bot_instance()
        limit = request.args.get('limit', 10, type=int)
        trades = bot.get_recent_trades(symbol.upper(), limit)
        return jsonify({'success': True, 'trades': trades})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

def get_bot_instance():
    """Get bot instance from session."""
    session_id = session.get('bot_id')
    if not session_id or session_id not in bot_instances:
        raise Exception('Not connected. Please connect with API credentials first.')
    return bot_instances[session_id]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)