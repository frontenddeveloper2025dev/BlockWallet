"""
Flask Web Application for Blockchain Wallet
Minimalist visual interface for wallet operations
"""

from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for
import os
import json
from datetime import datetime
from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'blockchain_wallet_secret_key_change_in_production')

# Global wallet instance
wallet = Wallet()

@app.route('/')
def index():
    """Main dashboard page."""
    wallet_info = None
    if wallet.address:
        try:
            # For faster health check responses, use a lighter check
            wallet_info = {
                'address': wallet.address,
                'unlocked': wallet.is_unlocked,
                'balance': wallet.get_balance() if wallet.is_unlocked else 0
            }
        except:
            wallet_info = None
    
    return render_template('index.html', wallet_info=wallet_info)

@app.route('/create_wallet', methods=['GET', 'POST'])
def create_wallet():
    """Create new wallet page."""
    if request.method == 'POST':
        try:
            wallet.generate_new_wallet()
            password = request.form.get('password')
            if password:
                wallet.save_wallet(password)
                flash('Wallet created and saved successfully!', 'success')
            else:
                flash('Wallet created but not saved (no password provided)', 'warning')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error creating wallet: {str(e)}', 'error')
    
    return render_template('create_wallet.html')

@app.route('/load_wallet', methods=['GET', 'POST'])
def load_wallet():
    """Load existing wallet page."""
    if request.method == 'POST':
        try:
            password = request.form.get('password')
            if password:
                wallet.load_wallet(password)
                flash('Wallet loaded successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Password required to load wallet', 'error')
        except Exception as e:
            flash(f'Error loading wallet: {str(e)}', 'error')
    
    return render_template('load_wallet.html')

@app.route('/send_transaction', methods=['GET', 'POST'])
def send_transaction():
    """Send transaction page."""
    if request.method == 'POST':
        try:
            if not wallet.is_unlocked:
                flash('Wallet is locked. Please load a wallet first.', 'error')
                return redirect(url_for('load_wallet'))
            
            recipient = request.form.get('recipient')
            amount = float(request.form.get('amount', 0))
            fee = float(request.form.get('fee', 0.001))
            message = request.form.get('message', '')
            
            transaction = wallet.send_transaction(recipient, amount, fee, message)
            flash('Transaction sent successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error sending transaction: {str(e)}', 'error')
    
    # Get current balance for display
    balance = 0
    if wallet.address:
        try:
            balance = wallet.get_balance()
        except:
            balance = 0
    
    return render_template('send_transaction.html', balance=balance)

@app.route('/mine_block', methods=['POST'])
def mine_block():
    """Mine a new block."""
    try:
        if not wallet.address:
            flash('No wallet loaded. Please create or load a wallet first.', 'error')
            return redirect(url_for('index'))
        
        success = wallet.mine_block()
        if success:
            flash('Block mined successfully!', 'success')
        else:
            flash('No pending transactions to mine.', 'info')
            
    except Exception as e:
        flash(f'Error mining block: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/transaction_history')
def transaction_history():
    """Transaction history page."""
    transactions = []
    if wallet.address:
        try:
            transactions = wallet.get_transaction_history(20)
        except:
            transactions = []
    
    return render_template('transaction_history.html', transactions=transactions)

@app.route('/blockchain_info')
def blockchain_info():
    """Blockchain information page."""
    blockchain_data = {}
    if wallet.blockchain:
        try:
            blockchain_data = wallet.blockchain.get_blockchain_info()
            # Get recent blocks
            recent_blocks = []
            for i in range(max(0, len(wallet.blockchain.chain) - 5), len(wallet.blockchain.chain)):
                block = wallet.blockchain.chain[i]
                recent_blocks.append({
                    'index': block.index,
                    'hash': block.hash,
                    'transactions': len(block.transactions),
                    'timestamp': block.get_formatted_timestamp()
                })
            blockchain_data['recent_blocks'] = recent_blocks
        except:
            blockchain_data = {}
    
    return render_template('blockchain_info.html', blockchain_data=blockchain_data)

@app.route('/features')
def features():
    """Features showcase page."""
    return render_template('features.html')

@app.route('/health')
def health_check():
    """Health check endpoint for deployment monitoring."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/api/wallet_status')
def api_wallet_status():
    """API endpoint for wallet status."""
    if wallet.address:
        try:
            wallet_info = wallet.get_wallet_info()
            return jsonify({
                'loaded': True,
                'address': wallet.address,
                'balance': wallet_info['balance'],
                'unlocked': wallet.is_unlocked
            })
        except:
            return jsonify({'loaded': False})
    else:
        return jsonify({'loaded': False})

@app.route('/lock_wallet', methods=['POST'])
def lock_wallet():
    """Lock the wallet."""
    try:
        wallet.lock_wallet()
        flash('Wallet locked successfully!', 'success')
    except Exception as e:
        flash(f'Error locking wallet: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)