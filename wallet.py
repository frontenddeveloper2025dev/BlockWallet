"""
Blockchain Wallet implementation.
Handles wallet operations including key management, balance tracking, and transactions.
"""

import json
import os
import getpass
from datetime import datetime
from crypto_utils import CryptoUtils
from transaction import Transaction
from blockchain import Blockchain

class Wallet:
    """Blockchain wallet for managing keys, addresses, and transactions."""
    
    def __init__(self, blockchain=None):
        """Initialize a new wallet."""
        self.private_key = None
        self.public_key = None
        self.address = None
        self.blockchain = blockchain or Blockchain()
        self.wallet_file = "wallet.json"
        self.is_unlocked = False
    
    def generate_new_wallet(self):
        """Generate a new wallet with private key, public key, and address."""
        try:
            print("Generating new wallet...")
            
            # Generate private key
            self.private_key = CryptoUtils.generate_private_key()
            
            # Derive public key
            self.public_key = CryptoUtils.get_public_key(self.private_key)
            
            # Create address
            self.address = CryptoUtils.create_address(self.public_key)
            
            self.is_unlocked = True
            
            print("✓ New wallet generated successfully!")
            print(f"Address: {self.address}")
            print("⚠️  Make sure to save your private key securely!")
            
            return True
            
        except Exception as e:
            raise Exception(f"Failed to generate wallet: {e}")
    
    def import_wallet(self, private_key_hex):
        """Import wallet from private key."""
        try:
            print("Importing wallet from private key...")
            
            # Create private key from hex string
            self.private_key = CryptoUtils.private_key_from_hex(private_key_hex)
            
            # Derive public key
            self.public_key = CryptoUtils.get_public_key(self.private_key)
            
            # Create address
            self.address = CryptoUtils.create_address(self.public_key)
            
            self.is_unlocked = True
            
            print("✓ Wallet imported successfully!")
            print(f"Address: {self.address}")
            
            return True
            
        except Exception as e:
            raise Exception(f"Failed to import wallet: {e}")
    
    def save_wallet(self, password):
        """Save wallet to encrypted file."""
        try:
            if not self.private_key:
                raise Exception("No wallet to save")
            
            # Get private key as hex
            private_key_hex = CryptoUtils.private_key_to_hex(self.private_key)
            
            # Create wallet data
            wallet_data = {
                "address": self.address,
                "private_key": private_key_hex,
                "created_at": datetime.now().isoformat(),
                "version": "1.0"
            }
            
            # Derive encryption key from password
            key, salt = CryptoUtils.derive_key_from_password(password)
            
            # Encrypt wallet data
            encrypted_data = CryptoUtils.encrypt_data(json.dumps(wallet_data), key)
            
            # Save to file
            file_data = {
                "encrypted_wallet": encrypted_data.decode('latin-1'),
                "salt": salt.hex(),
                "version": "1.0"
            }
            
            with open(self.wallet_file, 'w') as f:
                json.dump(file_data, f, indent=2)
            
            print(f"✓ Wallet saved to {self.wallet_file}")
            return True
            
        except Exception as e:
            raise Exception(f"Failed to save wallet: {e}")
    
    def load_wallet(self, password):
        """Load wallet from encrypted file."""
        try:
            if not os.path.exists(self.wallet_file):
                raise Exception("Wallet file not found")
            
            # Load file data
            with open(self.wallet_file, 'r') as f:
                file_data = json.load(f)
            
            # Get salt and encrypted data
            salt = bytes.fromhex(file_data["salt"])
            encrypted_data = file_data["encrypted_wallet"].encode('latin-1')
            
            # Derive decryption key
            key, _ = CryptoUtils.derive_key_from_password(password, salt)
            
            # Decrypt wallet data
            decrypted_data = CryptoUtils.decrypt_data(encrypted_data, key)
            wallet_data = json.loads(decrypted_data)
            
            # Import wallet
            self.import_wallet(wallet_data["private_key"])
            
            print(f"✓ Wallet loaded from {self.wallet_file}")
            return True
            
        except Exception as e:
            raise Exception(f"Failed to load wallet: {e}")
    
    def get_private_key_hex(self):
        """Get private key as hexadecimal string."""
        if not self.private_key:
            raise Exception("No private key available")
        
        if not self.is_unlocked:
            raise Exception("Wallet is locked")
        
        return CryptoUtils.private_key_to_hex(self.private_key)
    
    def get_balance(self):
        """Get current wallet balance."""
        if not self.address:
            raise Exception("No wallet address available")
        
        return self.blockchain.get_balance(self.address)
    
    def send_transaction(self, recipient_address, amount, fee=0.001, message=""):
        """Send a transaction to another address."""
        try:
            if not self.is_unlocked:
                raise Exception("Wallet is locked")
            
            if not self.address:
                raise Exception("No wallet address available")
            
            # Check balance
            current_balance = self.get_balance()
            total_cost = float(amount) + float(fee)
            
            if current_balance < total_cost:
                raise Exception(f"Insufficient balance. Available: {current_balance}, Required: {total_cost}")
            
            # Create transaction
            transaction = Transaction(
                sender_address=self.address,
                recipient_address=recipient_address,
                amount=float(amount),
                fee=float(fee),
                message=message
            )
            
            # Sign transaction
            transaction.sign_transaction(self.private_key)
            
            # Add to blockchain
            self.blockchain.add_transaction(transaction)
            
            print("✓ Transaction created and added to pending transactions!")
            print(f"Transaction ID: {transaction.transaction_id}")
            print(f"Amount: {amount}")
            print(f"Fee: {fee}")
            print(f"Recipient: {recipient_address}")
            
            return transaction
            
        except Exception as e:
            raise Exception(f"Failed to send transaction: {e}")
    
    def get_transaction_history(self, limit=10):
        """Get transaction history for this wallet."""
        if not self.address:
            raise Exception("No wallet address available")
        
        return self.blockchain.get_transaction_history(self.address, limit)
    
    def mine_block(self):
        """Mine pending transactions."""
        try:
            if not self.address:
                raise Exception("No wallet address available")
            
            success = self.blockchain.mine_pending_transactions(self.address)
            
            if success:
                print("✓ Block mined successfully!")
                print(f"Mining reward of {self.blockchain.mining_reward} added to your wallet.")
            else:
                print("No pending transactions to mine.")
            
            return success
            
        except Exception as e:
            raise Exception(f"Failed to mine block: {e}")
    
    def get_wallet_info(self):
        """Get comprehensive wallet information."""
        if not self.address:
            return {"error": "No wallet loaded"}
        
        balance = self.get_balance()
        transaction_history = self.get_transaction_history(5)
        
        return {
            "address": self.address,
            "balance": balance,
            "is_unlocked": self.is_unlocked,
            "recent_transactions": len(transaction_history),
            "blockchain_info": self.blockchain.get_blockchain_info()
        }
    
    def lock_wallet(self):
        """Lock the wallet by clearing sensitive data."""
        self.private_key = None
        self.public_key = None
        self.is_unlocked = False
        print("✓ Wallet locked successfully!")
    
    def is_address_valid(self, address):
        """Check if an address is valid."""
        try:
            # Basic validation - check length and characters
            if not address or len(address) < 26 or len(address) > 35:
                return False
            
            # Check if it's valid base58
            import base58
            try:
                decoded = base58.b58decode(address)
                if len(decoded) != 25:  # 20 bytes hash + 1 byte version + 4 bytes checksum
                    return False
                return True
            except:
                return False
                
        except Exception:
            return False
    
    def backup_wallet(self, backup_file=None):
        """Create a backup of the wallet."""
        try:
            if not os.path.exists(self.wallet_file):
                raise Exception("No wallet file to backup")
            
            backup_file = backup_file or f"wallet_backup_{int(datetime.now().timestamp())}.json"
            
            # Copy wallet file
            import shutil
            shutil.copy2(self.wallet_file, backup_file)
            
            print(f"✓ Wallet backed up to {backup_file}")
            return backup_file
            
        except Exception as e:
            raise Exception(f"Failed to backup wallet: {e}")
