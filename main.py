#!/usr/bin/env python3
"""
Blockchain Wallet - Main Entry Point
A Python-based blockchain wallet with key generation, transaction simulation, and basic security features.
"""

import sys
import os
from cli import WalletCLI

def main():
    """Main entry point for the blockchain wallet application."""
    try:
        # Initialize the CLI interface
        wallet_cli = WalletCLI()
        
        # Start the interactive wallet session
        wallet_cli.run()
        
    except KeyboardInterrupt:
        print("\n\nWallet session terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
