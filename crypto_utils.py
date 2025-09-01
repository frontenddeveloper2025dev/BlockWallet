"""
Cryptographic utilities for the blockchain wallet.
Handles key generation, signing, and address creation.
"""

import hashlib
import secrets
import base58
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class CryptoUtils:
    """Utility class for cryptographic operations."""
    
    @staticmethod
    def generate_private_key():
        """Generate a new private key using SECP256k1 curve."""
        try:
            # Generate a cryptographically secure random private key
            private_key = SigningKey.generate(curve=SECP256k1)
            return private_key
        except Exception as e:
            raise Exception(f"Failed to generate private key: {e}")
    
    @staticmethod
    def private_key_to_hex(private_key):
        """Convert private key to hexadecimal string."""
        try:
            return private_key.to_string().hex()
        except Exception as e:
            raise Exception(f"Failed to convert private key to hex: {e}")
    
    @staticmethod
    def private_key_from_hex(hex_string):
        """Create private key from hexadecimal string."""
        try:
            private_key_bytes = bytes.fromhex(hex_string)
            return SigningKey.from_string(private_key_bytes, curve=SECP256k1)
        except Exception as e:
            raise Exception(f"Failed to create private key from hex: {e}")
    
    @staticmethod
    def get_public_key(private_key):
        """Get public key from private key."""
        try:
            return private_key.get_verifying_key()
        except Exception as e:
            raise Exception(f"Failed to get public key: {e}")
    
    @staticmethod
    def create_address(public_key):
        """Create a wallet address from public key."""
        try:
            # Get the public key in compressed format
            public_key_bytes = public_key.to_string()
            
            # SHA256 hash of the public key
            sha256_hash = hashlib.sha256(public_key_bytes).digest()
            
            # RIPEMD160 hash of the SHA256 hash
            ripemd160 = hashlib.new('ripemd160')
            ripemd160.update(sha256_hash)
            hash160 = ripemd160.digest()
            
            # Add version byte (0x00 for main network)
            versioned_payload = b'\x00' + hash160
            
            # Double SHA256 for checksum
            checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
            
            # Combine payload and checksum
            binary_address = versioned_payload + checksum
            
            # Encode in Base58
            address = base58.b58encode(binary_address).decode('utf-8')
            
            return address
        except Exception as e:
            raise Exception(f"Failed to create address: {e}")
    
    @staticmethod
    def sign_message(private_key, message):
        """Sign a message with the private key."""
        try:
            # Convert message to bytes if it's a string
            if isinstance(message, str):
                message = message.encode('utf-8')
            
            # Sign the message
            signature = private_key.sign(message)
            return signature.hex()
        except Exception as e:
            raise Exception(f"Failed to sign message: {e}")
    
    @staticmethod
    def verify_signature(public_key, message, signature_hex):
        """Verify a signature with the public key."""
        try:
            # Convert message to bytes if it's a string
            if isinstance(message, str):
                message = message.encode('utf-8')
            
            # Convert signature from hex
            signature = bytes.fromhex(signature_hex)
            
            # Verify the signature
            return public_key.verify(signature, message)
        except Exception as e:
            return False
    
    @staticmethod
    def hash_transaction(transaction_data):
        """Create a hash of transaction data."""
        try:
            # Convert transaction data to string if it's not already
            if not isinstance(transaction_data, str):
                transaction_data = str(transaction_data)
            
            # Create SHA256 hash
            return hashlib.sha256(transaction_data.encode('utf-8')).hexdigest()
        except Exception as e:
            raise Exception(f"Failed to hash transaction: {e}")
    
    @staticmethod
    def derive_key_from_password(password, salt=None):
        """Derive encryption key from password using PBKDF2."""
        try:
            if salt is None:
                salt = os.urandom(16)
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            return key, salt
        except Exception as e:
            raise Exception(f"Failed to derive key from password: {e}")
    
    @staticmethod
    def encrypt_data(data, key):
        """Encrypt data using Fernet symmetric encryption."""
        try:
            fernet = Fernet(key)
            if isinstance(data, str):
                data = data.encode('utf-8')
            encrypted_data = fernet.encrypt(data)
            return encrypted_data
        except Exception as e:
            raise Exception(f"Failed to encrypt data: {e}")
    
    @staticmethod
    def decrypt_data(encrypted_data, key):
        """Decrypt data using Fernet symmetric encryption."""
        try:
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            raise Exception(f"Failed to decrypt data: {e}")
