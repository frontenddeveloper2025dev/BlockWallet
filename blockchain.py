"""
Simple blockchain implementation for the wallet demonstration.
This is a simplified blockchain for educational purposes.
"""

import json
import time
import hashlib
from datetime import datetime
from transaction import Transaction, TransactionPool

class Block:
    """Represents a block in the blockchain."""
    
    def __init__(self, index, transactions, previous_hash, timestamp=None):
        """Initialize a new block."""
        self.index = index
        self.timestamp = timestamp or time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate the hash of the block."""
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """Mine the block with the given difficulty."""
        target = "0" * difficulty
        
        print(f"Mining block {self.index}...")
        start_time = time.time()
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
            
            # Print progress every 100000 attempts
            if self.nonce % 100000 == 0:
                print(f"Mining attempt: {self.nonce}")
        
        end_time = time.time()
        print(f"Block {self.index} mined in {end_time - start_time:.2f} seconds")
        print(f"Hash: {self.hash}")
        print(f"Nonce: {self.nonce}")
    
    def to_dict(self):
        """Convert block to dictionary."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }
    
    def get_formatted_timestamp(self):
        """Get formatted timestamp string."""
        return datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")

class Blockchain:
    """Simple blockchain implementation."""
    
    def __init__(self, difficulty=2):
        """Initialize the blockchain."""
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 10.0
        self.transaction_pool = TransactionPool()
    
    def create_genesis_block(self):
        """Create the genesis block."""
        genesis_transactions = []
        return Block(0, genesis_transactions, "0")
    
    def get_latest_block(self):
        """Get the latest block in the chain."""
        return self.chain[-1]
    
    def add_transaction(self, transaction):
        """Add a transaction to the pending transactions."""
        try:
            # Validate transaction
            is_valid, message = transaction.is_valid()
            if not is_valid:
                raise Exception(f"Invalid transaction: {message}")
            
            # Check if sender has sufficient balance
            sender_balance = self.get_balance(transaction.sender_address)
            required_amount = transaction.amount + transaction.fee
            
            if sender_balance < required_amount:
                raise Exception(f"Insufficient balance. Available: {sender_balance}, Required: {required_amount}")
            
            # Add to transaction pool
            self.transaction_pool.add_transaction(transaction)
            self.pending_transactions.append(transaction)
            
            return True
            
        except Exception as e:
            raise Exception(f"Failed to add transaction: {e}")
    
    def mine_pending_transactions(self, mining_reward_address):
        """Mine pending transactions into a new block."""
        try:
            if not self.pending_transactions:
                print("No pending transactions to mine.")
                return False
            
            # Create mining reward transaction
            reward_transaction = Transaction(
                sender_address="system",
                recipient_address=mining_reward_address,
                amount=self.mining_reward,
                fee=0,
                message="Mining reward"
            )
            reward_transaction.transaction_id = f"reward_{int(time.time())}"
            reward_transaction.signature = "system_signature"
            reward_transaction.status = "confirmed"
            
            # Add reward transaction to the list
            transactions_to_mine = self.pending_transactions.copy()
            transactions_to_mine.append(reward_transaction)
            
            # Create new block
            new_block = Block(
                index=len(self.chain),
                transactions=transactions_to_mine,
                previous_hash=self.get_latest_block().hash
            )
            
            # Mine the block
            new_block.mine_block(self.difficulty)
            
            # Add block to chain
            self.chain.append(new_block)
            
            # Confirm transactions in the pool
            for tx in self.pending_transactions:
                self.transaction_pool.confirm_transaction(tx.transaction_id)
            
            # Clear pending transactions
            self.pending_transactions = []
            
            print(f"Block {new_block.index} successfully mined and added to blockchain!")
            return True
            
        except Exception as e:
            raise Exception(f"Failed to mine block: {e}")
    
    def get_balance(self, address):
        """Calculate the balance for a given address."""
        balance = 0.0
        
        # Go through all blocks and transactions
        for block in self.chain:
            for transaction in block.transactions:
                # If this address received money
                if transaction.recipient_address == address:
                    balance += transaction.amount
                
                # If this address sent money
                if transaction.sender_address == address:
                    balance -= (transaction.amount + transaction.fee)
        
        return balance
    
    def get_transaction_history(self, address, limit=10):
        """Get transaction history for an address."""
        transactions = []
        
        # Go through all blocks
        for block in self.chain:
            for transaction in block.transactions:
                if (transaction.sender_address == address or 
                    transaction.recipient_address == address):
                    transactions.append(transaction)
        
        # Include pending transactions
        for transaction in self.pending_transactions:
            if (transaction.sender_address == address or 
                transaction.recipient_address == address):
                transactions.append(transaction)
        
        # Sort by timestamp (most recent first)
        transactions.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Apply limit
        if limit > 0:
            transactions = transactions[:limit]
        
        return transactions
    
    def is_chain_valid(self):
        """Validate the entire blockchain."""
        try:
            for i in range(1, len(self.chain)):
                current_block = self.chain[i]
                previous_block = self.chain[i - 1]
                
                # Check if current block hash is valid
                if current_block.hash != current_block.calculate_hash():
                    return False, f"Invalid hash at block {i}"
                
                # Check if block points to previous block
                if current_block.previous_hash != previous_block.hash:
                    return False, f"Invalid previous hash at block {i}"
                
                # Check if block is properly mined
                if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                    return False, f"Block {i} not properly mined"
            
            return True, "Blockchain is valid"
            
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def get_blockchain_info(self):
        """Get general information about the blockchain."""
        return {
            "total_blocks": len(self.chain),
            "difficulty": self.difficulty,
            "mining_reward": self.mining_reward,
            "pending_transactions": len(self.pending_transactions),
            "latest_block_hash": self.get_latest_block().hash,
            "is_valid": self.is_chain_valid()[0]
        }
    
    def get_block_by_index(self, index):
        """Get a block by its index."""
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None
    
    def search_transaction(self, transaction_id):
        """Search for a transaction by ID."""
        # Search in confirmed transactions (blockchain)
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.transaction_id == transaction_id:
                    return transaction, "confirmed"
        
        # Search in pending transactions
        for transaction in self.pending_transactions:
            if transaction.transaction_id == transaction_id:
                return transaction, "pending"
        
        return None, "not_found"
