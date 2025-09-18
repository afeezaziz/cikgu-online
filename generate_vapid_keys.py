#!/usr/bin/env python3
"""
Generate VAPID keys for push notifications
Run this script to generate your VAPID public and private keys
"""

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64

def generate_vapid_keys():
    """Generate VAPID key pair for push notifications"""

    # Generate private key
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

    # Get public key
    public_key = private_key.public_key()

    # Serialize private key
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    # Convert to base64url format
    private_key_b64 = base64.urlsafe_b64encode(private_bytes).decode('utf-8').rstrip('=')
    public_key_b64 = base64.urlsafe_b64encode(public_bytes).decode('utf-8').rstrip('=')

    print("VAPID Keys Generated:")
    print("=" * 50)
    print(f"VAPID_PUBLIC_KEY={public_key_b64}")
    print(f"VAPID_PRIVATE_KEY={private_key_b64}")
    print("=" * 50)
    print("Add these keys to your .env file")

    return {
        'public_key': public_key_b64,
        'private_key': private_key_b64
    }

if __name__ == '__main__':
    generate_vapid_keys()