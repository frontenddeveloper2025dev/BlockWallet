"""
Command Line Interface for the Blockchain Wallet.
Provides an interactive terminal interface for wallet operations.
"""

import os
import sys
import getpass
from wallet import Wallet
from blockchain import Blockchain

class WalletCLI:
    """Command line interface for the blockchain wallet."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.wallet = Wallet()
        self.running = True
    
    def print_banner(self):
        """Print the application banner."""
        print("=" * 60)
        print("           BLOCKCHAIN WALLET v1.0")
        print("    Python-based Cryptocurrency Wallet")
        print("=" * 60)
        print()
    
    def print_menu(self):
        """Print the main menu."""
        print("\n" + "=" * 40)
        print("              MAIN MENU")
        print("=" * 40)
        if self.wallet.address:
            wallet_info = self.wallet.get_wallet_info()
            print(f"Address: {self.wallet.address[:20]}...")
            print(f"Balance: {wallet_info['balance']:.6f} coins")
            print(f"Status: {'Unlocked' if self.wallet.is_unlocked else 'Locked'}")
            print("-" * 40)
        
        print("1.  Create New Wallet")
        print("2.  Load Existing Wallet")
        print("3.  Import Wallet (Private Key)")
        print("4.  Show Wallet Info")
        print("5.  Show Private Key")
        print("6.  Check Balance")
        print("7.  Send Transaction")
        print("8.  View Transaction History")
        print("9.  Mine Block")
        print("10. Blockchain Info")
        print("11. Validate Blockchain")
        print("12. Save Wallet")
        print("13. Backup Wallet")
        print("14. Lock Wallet")
        print("15. Exit")
        print("=" * 40)
    
    def get_user_input(self, prompt, password=False):
        """Get user input with optional password masking."""
        try:
            if password:
                return getpass.getpass(prompt)
            else:
                return input(prompt).strip()
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return None
    
    def create_new_wallet(self):
        """Create a new wallet."""
        try:
            print("\n" + "=" * 40)
            print("          CREATE NEW WALLET")
            print("=" * 40)
            
            self.wallet.generate_new_wallet()
            
            # Ask if user wants to save the wallet
            save_wallet = self.get_user_input("Do you want to save this wallet? (y/n): ")
            if save_wallet and save_wallet.lower() == 'y':
                password = self.get_user_input("Enter password to encrypt wallet: ", password=True)
                if password:
                    password_confirm = self.get_user_input("Confirm password: ", password=True)
                    if password == password_confirm:
                        self.wallet.save_wallet(password)
                    else:
                        print("❌ Passwords don't match. Wallet not saved.")
                else:
                    print("❌ No password provided. Wallet not saved.")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def load_wallet(self):
        """Load an existing wallet."""
        try:
            print("\n" + "=" * 40)
            print("          LOAD WALLET")
            print("=" * 40)
            
            if not os.path.exists("wallet.json"):
                print("❌ No wallet file found. Please create a new wallet first.")
                return
            
            password = self.get_user_input("Enter wallet password: ", password=True)
            if password:
                self.wallet.load_wallet(password)
            else:
                print("❌ No password provided.")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def import_wallet(self):
        """Import wallet from private key."""
        try:
            print("\n" + "=" * 40)
            print("          IMPORT WALLET")
            print("=" * 40)
            print("⚠️  Warning: Only import private keys from trusted sources!")
            
            private_key = self.get_user_input("Enter private key (hex): ")
            if private_key:
                self.wallet.import_wallet(private_key)
                
                # Ask if user wants to save the wallet
                save_wallet = self.get_user_input("Do you want to save this wallet? (y/n): ")
                if save_wallet and save_wallet.lower() == 'y':
                    password = self.get_user_input("Enter password to encrypt wallet: ", password=True)
                    if password:
                        password_confirm = self.get_user_input("Confirm password: ", password=True)
                        if password == password_confirm:
                            self.wallet.save_wallet(password)
                        else:
                            print("❌ Passwords don't match. Wallet not saved.")
            else:
                print("❌ No private key provided.")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def show_wallet_info(self):
        """Display detailed wallet information."""
        try:
            print("\n" + "=" * 50)
            print("               WALLET INFO")
            print("=" * 50)
            
            if not self.wallet.address:
                print("❌ No wallet loaded. Please create or load a wallet first.")
                return
            
            wallet_info = self.wallet.get_wallet_info()
            
            print(f"Address: {self.wallet.address}")
            print(f"Balance: {wallet_info['balance']:.6f} coins")
            print(f"Status: {'Unlocked' if wallet_info['is_unlocked'] else 'Locked'}")
            print(f"Recent Transactions: {wallet_info['recent_transactions']}")
            
            print("\nBlockchain Information:")
            blockchain_info = wallet_info['blockchain_info']
            print(f"  Total Blocks: {blockchain_info['total_blocks']}")
            print(f"  Mining Difficulty: {blockchain_info['difficulty']}")
            print(f"  Mining Reward: {blockchain_info['mining_reward']} coins")
            print(f"  Pending Transactions: {blockchain_info['pending_transactions']}")
            print(f"  Blockchain Valid: {blockchain_info['is_valid']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def show_private_key(self):
        """Display the private key (with warning)."""
        try:
            print("\n" + "=" * 50)
            print("              PRIVATE KEY")
            print("=" * 50)
            print("⚠️  WARNING: Never share your private key with anyone!")
            print("⚠️  Anyone with this key can access your funds!")
            print("=" * 50)
            
            if not self.wallet.is_unlocked:
                print("❌ Wallet is locked. Please load or create a wallet first.")
                return
            
            confirm = self.get_user_input("Are you sure you want to display private key? (yes/no): ")
            if confirm.lower() == 'yes':
                private_key = self.wallet.get_private_key_hex()
                print(f"\nPrivate Key: {private_key}")
                print("\n⚠️  Make sure to store this securely!")
            else:
                print("Operation cancelled.")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def check_balance(self):
        """Check and display wallet balance."""
        try:
            print("\n" + "=" * 40)
            print("            BALANCE")
            print("=" * 40)
            
            if not self.wallet.address:
                print("❌ No wallet loaded. Please create or load a wallet first.")
                return
            
            balance = self.wallet.get_balance()
            print(f"Address: {self.wallet.address}")
            print(f"Balance: {balance:.6f} coins")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def send_transaction(self):
        """Send a transaction."""
        try:
            print("\n" + "=" * 40)
            print("          SEND TRANSACTION")
            print("=" * 40)
            
            if not self.wallet.is_unlocked:
                print("❌ Wallet is locked. Please load or create a wallet first.")
                return
            
            # Get current balance
            balance = self.wallet.get_balance()
            print(f"Current Balance: {balance:.6f} coins")
            
            if balance <= 0:
                print("❌ Insufficient balance to send transaction.")
                return
            
            # Get transaction details
            recipient = self.get_user_input("Recipient address: ")
            if not recipient:
                print("❌ No recipient address provided.")
                return
            
            if not self.wallet.is_address_valid(recipient):
                print("❌ Invalid recipient address format.")
                return
            
            amount_str = self.get_user_input("Amount to send: ")
            if not amount_str:
                print("❌ No amount provided.")
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    print("❌ Amount must be positive.")
                    return
            except ValueError:
                print("❌ Invalid amount format.")
                return
            
            fee_str = self.get_user_input("Transaction fee (default 0.001): ") or "0.001"
            try:
                fee = float(fee_str)
                if fee < 0:
                    print("❌ Fee cannot be negative.")
                    return
            except ValueError:
                print("❌ Invalid fee format.")
                return
            
            message = self.get_user_input("Message (optional): ")
            
            # Confirm transaction
            total_cost = amount + fee
            print(f"\nTransaction Summary:")
            print(f"  To: {recipient}")
            print(f"  Amount: {amount:.6f} coins")
            print(f"  Fee: {fee:.6f} coins")
            print(f"  Total Cost: {total_cost:.6f} coins")
            print(f"  Message: {message or 'None'}")
            
            confirm = self.get_user_input("Confirm transaction? (y/n): ")
            if confirm.lower() == 'y':
                transaction = self.wallet.send_transaction(recipient, amount, fee, message)
                print("\n✓ Transaction sent successfully!")
                print("Note: Transaction is pending until the next block is mined.")
            else:
                print("Transaction cancelled.")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def view_transaction_history(self):
        """View transaction history."""
        try:
            print("\n" + "=" * 60)
            print("              TRANSACTION HISTORY")
            print("=" * 60)
            
            if not self.wallet.address:
                print("❌ No wallet loaded. Please create or load a wallet first.")
                return
            
            limit_str = self.get_user_input("Number of transactions to show (default 10): ") or "10"
            try:
                limit = int(limit_str)
            except ValueError:
                limit = 10
            
            transactions = self.wallet.get_transaction_history(limit)
            
            if not transactions:
                print("No transactions found.")
                return
            
            for i, tx in enumerate(transactions, 1):
                tx_type = "Received" if tx.recipient_address == self.wallet.address else "Sent"
                amount_str = f"+{tx.amount:.6f}" if tx_type == "Received" else f"-{tx.amount:.6f}"
                
                print(f"\n{i}. {tx_type} Transaction")
                print(f"   ID: {tx.transaction_id}")
                print(f"   Amount: {amount_str} coins")
                print(f"   From: {tx.sender_address}")
                print(f"   To: {tx.recipient_address}")
                print(f"   Fee: {tx.fee:.6f} coins")
                print(f"   Status: {tx.status}")
                print(f"   Time: {tx.get_formatted_timestamp()}")
                if tx.message:
                    print(f"   Message: {tx.message}")
                print("-" * 50)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def mine_block(self):
        """Mine a new block."""
        try:
            print("\n" + "=" * 40)
            print("            MINE BLOCK")
            print("=" * 40)
            
            if not self.wallet.address:
                print("❌ No wallet loaded. Please create or load a wallet first.")
                return
            
            # Check if there are pending transactions
            pending_count = len(self.wallet.blockchain.pending_transactions)
            print(f"Pending transactions: {pending_count}")
            
            if pending_count == 0:
                print("No pending transactions to mine.")
                return
            
            print(f"Mining reward: {self.wallet.blockchain.mining_reward} coins")
            confirm = self.get_user_input("Start mining? (y/n): ")
            
            if confirm.lower() == 'y':
                print("Starting mining process...")
                self.wallet.mine_block()
            else:
                print("Mining cancelled.")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def show_blockchain_info(self):
        """Display blockchain information."""
        try:
            print("\n" + "=" * 50)
            print("              BLOCKCHAIN INFO")
            print("=" * 50)
            
            info = self.wallet.blockchain.get_blockchain_info()
            
            print(f"Total Blocks: {info['total_blocks']}")
            print(f"Mining Difficulty: {info['difficulty']}")
            print(f"Mining Reward: {info['mining_reward']} coins")
            print(f"Pending Transactions: {info['pending_transactions']}")
            print(f"Latest Block Hash: {info['latest_block_hash']}")
            print(f"Blockchain Valid: {info['is_valid']}")
            
            # Show recent blocks
            print(f"\nRecent Blocks:")
            for i in range(max(0, len(self.wallet.blockchain.chain) - 3), len(self.wallet.blockchain.chain)):
                block = self.wallet.blockchain.chain[i]
                print(f"  Block {block.index}: {len(block.transactions)} transactions")
                print(f"    Hash: {block.hash[:20]}...")
                print(f"    Time: {block.get_formatted_timestamp()}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def validate_blockchain(self):
        """Validate the blockchain integrity."""
        try:
            print("\n" + "=" * 40)
            print("         VALIDATE BLOCKCHAIN")
            print("=" * 40)
            
            print("Validating blockchain integrity...")
            is_valid, message = self.wallet.blockchain.is_chain_valid()
            
            if is_valid:
                print("✓ Blockchain is valid!")
            else:
                print(f"❌ Blockchain validation failed: {message}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def save_wallet(self):
        """Save the current wallet."""
        try:
            print("\n" + "=" * 40)
            print("            SAVE WALLET")
            print("=" * 40)
            
            if not self.wallet.is_unlocked:
                print("❌ No wallet to save. Please create or load a wallet first.")
                return
            
            password = self.get_user_input("Enter password to encrypt wallet: ", password=True)
            if password:
                password_confirm = self.get_user_input("Confirm password: ", password=True)
                if password == password_confirm:
                    self.wallet.save_wallet(password)
                else:
                    print("❌ Passwords don't match. Wallet not saved.")
            else:
                print("❌ No password provided.")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def backup_wallet(self):
        """Create a backup of the wallet."""
        try:
            print("\n" + "=" * 40)
            print("           BACKUP WALLET")
            print("=" * 40)
            
            backup_file = self.wallet.backup_wallet()
            print(f"Backup created: {backup_file}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def lock_wallet(self):
        """Lock the wallet."""
        try:
            print("\n" + "=" * 40)
            print("            LOCK WALLET")
            print("=" * 40)
            
            if not self.wallet.is_unlocked:
                print("Wallet is already locked.")
                return
            
            confirm = self.get_user_input("Are you sure you want to lock the wallet? (y/n): ")
            if confirm.lower() == 'y':
                self.wallet.lock_wallet()
            else:
                print("Lock operation cancelled.")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def run(self):
        """Run the main CLI loop."""
        self.print_banner()
        
        while self.running:
            try:
                self.print_menu()
                choice = self.get_user_input("Enter your choice (1-15): ")
                
                if choice == '1':
                    self.create_new_wallet()
                elif choice == '2':
                    self.load_wallet()
                elif choice == '3':
                    self.import_wallet()
                elif choice == '4':
                    self.show_wallet_info()
                elif choice == '5':
                    self.show_private_key()
                elif choice == '6':
                    self.check_balance()
                elif choice == '7':
                    self.send_transaction()
                elif choice == '8':
                    self.view_transaction_history()
                elif choice == '9':
                    self.mine_block()
                elif choice == '10':
                    self.show_blockchain_info()
                elif choice == '11':
                    self.validate_blockchain()
                elif choice == '12':
                    self.save_wallet()
                elif choice == '13':
                    self.backup_wallet()
                elif choice == '14':
                    self.lock_wallet()
                elif choice == '15':
                    print("\nThank you for using Blockchain Wallet!")
                    self.running = False
                else:
                    print("❌ Invalid choice. Please enter a number between 1 and 15.")
                
                if self.running:
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                input("Press Enter to continue...")
