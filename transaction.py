"""
Transaction handling for the blockchain wallet.
Manages transaction creation, validation, and processing.
"""

import json
import time
from datetime import datetime
from crypto_utils import CryptoUtils

class Transaction:
    """Represents a blockchain transaction."""
    
    def __init__(self, sender_address, recipient_address, amount, fee=0.001, message=""):
        """Initialize a new transaction."""
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.amount = float(amount)
        self.fee = float(fee)
        self.message = message
        self.timestamp = time.time()
        self.transaction_id = None
        self.signature = None
        self.status = "pending"
    
    def to_dict(self):
        """Convert transaction to dictionary."""
        return {
            "transaction_id": self.transaction_id,
            "sender_address": self.sender_address,
            "recipient_address": self.recipient_address,
            "amount": self.amount,
            "fee": self.fee,
            "message": self.message,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "status": self.status
        }
    
    def to_json(self):
        """Convert transaction to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    def get_transaction_data(self):
        """Get transaction data for signing (without signature)."""
        data = {
            "sender_address": self.sender_address,
            "recipient_address": self.recipient_address,
            "amount": self.amount,
            "fee": self.fee,
            "message": self.message,
            "timestamp": self.timestamp
        }
        return json.dumps(data, sort_keys=True)
    
    def calculate_hash(self):
        """Calculate the transaction hash."""
        transaction_data = self.get_transaction_data()
        return CryptoUtils.hash_transaction(transaction_data)
    
    def sign_transaction(self, private_key):
        """Sign the transaction with the sender's private key."""
        try:
            # Get transaction data for signing
            transaction_data = self.get_transaction_data()
            
            # Sign the transaction
            self.signature = CryptoUtils.sign_message(private_key, transaction_data)
            
            # Generate transaction ID
            self.transaction_id = self.calculate_hash()
            
            return True
        except Exception as e:
            raise Exception(f"Failed to sign transaction: {e}")
    
    def verify_signature(self, public_key):
        """Verify the transaction signature."""
        try:
            if not self.signature:
                return False
            
            transaction_data = self.get_transaction_data()
            return CryptoUtils.verify_signature(public_key, transaction_data, self.signature)
        except Exception as e:
            return False
    
    def is_valid(self):
        """Check if the transaction is valid."""
        try:
            # Check basic fields
            if not self.sender_address or not self.recipient_address:
                return False, "Invalid sender or recipient address"
            
            if self.amount <= 0:
                return False, "Amount must be positive"
            
            if self.fee < 0:
                return False, "Fee cannot be negative"
            
            if not self.signature:
                return False, "Transaction not signed"
            
            if not self.transaction_id:
                return False, "Invalid transaction ID"
            
            # Check if sender and recipient are different
            if self.sender_address == self.recipient_address:
                return False, "Sender and recipient cannot be the same"
            
            return True, "Transaction is valid"
            
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def get_formatted_timestamp(self):
        """Get formatted timestamp string."""
        return datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")

class TransactionPool:
    """Manages a pool of pending transactions."""
    
    def __init__(self):
        """Initialize transaction pool."""
        self.transactions = []
        self.confirmed_transactions = []
    
    def add_transaction(self, transaction):
        """Add a transaction to the pool."""
        try:
            # Validate transaction
            is_valid, message = transaction.is_valid()
            if not is_valid:
                raise Exception(f"Invalid transaction: {message}")
            
            # Check for duplicate transactions
            for tx in self.transactions:
                if tx.transaction_id == transaction.transaction_id:
                    raise Exception("Transaction already exists in pool")
            
            # Add to pending transactions
            self.transactions.append(transaction)
            return True
            
        except Exception as e:
            raise Exception(f"Failed to add transaction to pool: {e}")
    
    def get_pending_transactions(self):
        """Get all pending transactions."""
        return [tx for tx in self.transactions if tx.status == "pending"]
    
    def confirm_transaction(self, transaction_id):
        """Confirm a transaction and move it to confirmed list."""
        try:
            for i, tx in enumerate(self.transactions):
                if tx.transaction_id == transaction_id:
                    tx.status = "confirmed"
                    confirmed_tx = self.transactions.pop(i)
                    self.confirmed_transactions.append(confirmed_tx)
                    return True
            
            return False
        except Exception as e:
            raise Exception(f"Failed to confirm transaction: {e}")
    
    def get_transaction_by_id(self, transaction_id):
        """Get a transaction by its ID."""
        # Check pending transactions
        for tx in self.transactions:
            if tx.transaction_id == transaction_id:
                return tx
        
        # Check confirmed transactions
        for tx in self.confirmed_transactions:
            if tx.transaction_id == transaction_id:
                return tx
        
        return None
    
    def get_transactions_for_address(self, address):
        """Get all transactions involving a specific address."""
        address_transactions = []
        
        # Check pending transactions
        for tx in self.transactions:
            if tx.sender_address == address or tx.recipient_address == address:
                address_transactions.append(tx)
        
        # Check confirmed transactions
        for tx in self.confirmed_transactions:
            if tx.sender_address == address or tx.recipient_address == address:
                address_transactions.append(tx)
        
        return address_transactions
    
    def calculate_balance(self, address):
        """Calculate the balance for a specific address."""
        balance = 0.0
        
        # Process all confirmed transactions
        for tx in self.confirmed_transactions:
            if tx.recipient_address == address:
                balance += tx.amount
            elif tx.sender_address == address:
                balance -= (tx.amount + tx.fee)
        
        return balance
    
    def get_transaction_history(self, address, limit=10):
        """Get transaction history for an address."""
        address_transactions = self.get_transactions_for_address(address)
        
        # Sort by timestamp (most recent first)
        address_transactions.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Apply limit
        if limit > 0:
            address_transactions = address_transactions[:limit]
        
        return address_transactions
