# Blockchain Wallet

## Overview

A Python-based educational blockchain wallet implementation that demonstrates core cryptocurrency concepts including key generation, transaction management, and basic blockchain operations. The project provides a command-line interface for users to create wallets, manage private keys, send transactions, and interact with a simplified blockchain network. This is designed as a learning tool to understand blockchain fundamentals rather than a production-ready cryptocurrency wallet.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Components

**Wallet Management**
- Uses ECDSA cryptography with SECP256k1 curve for key generation and signing
- Implements address creation through public key hashing with Base58 encoding
- Provides secure private key storage with password-based encryption using PBKDF2 and Fernet
- Supports wallet import/export functionality for key portability

**Transaction System**
- Implements digital signature-based transaction validation
- Includes transaction pooling mechanism for managing pending transactions
- Supports basic transaction features including amounts, fees, and optional messages
- Provides transaction history tracking and status management

**Blockchain Implementation**
- Simplified proof-of-work consensus mechanism with adjustable mining difficulty
- Block structure includes transaction data, timestamps, and cryptographic hashing
- Chain validation logic to ensure blockchain integrity
- Mining functionality with progress reporting and nonce-based hash targeting

**Command Line Interface**
- Interactive menu-driven user experience for wallet operations
- Real-time wallet status display including balance and unlock state
- Comprehensive error handling and user feedback
- Secure password input for sensitive operations

### Security Architecture

**Cryptographic Security**
- ECDSA digital signatures for transaction authenticity
- SHA-256 hashing for block and transaction integrity
- Secure random number generation for private key creation
- Password-based key derivation for wallet file encryption

**Access Control**
- Wallet lock/unlock mechanism to protect private keys in memory
- Encrypted wallet file storage with user-defined passwords
- Private key exposure controls with user confirmation requirements

### Data Storage

**File-Based Storage**
- JSON format for wallet data persistence
- Encrypted private key storage using cryptography library
- Transaction history maintained within wallet files
- Blockchain state persistence across sessions

## External Dependencies

**Cryptographic Libraries**
- `ecdsa` - Elliptic curve digital signature operations using SECP256k1
- `cryptography` - Advanced encryption, key derivation, and secure storage
- `base58` - Bitcoin-style address encoding for user-friendly addresses

**Standard Libraries**
- `hashlib` - SHA-256 hashing for blockchain operations
- `json` - Data serialization for wallet and transaction storage
- `secrets` - Cryptographically secure random number generation
- `getpass` - Secure password input without echo
- `time` - Timestamp generation for blocks and transactions

**Development Tools**
- Python 3.x runtime environment
- Standard library modules for file I/O, error handling, and system operations
