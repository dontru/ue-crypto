from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization

from crypto.CryptoError import CryptoError


class Validator:
    @staticmethod
    def symmetric_key(key: str) -> None:
        """
        Check if the hex value of the key is correct
        :param key: Hex key
        :raise CryptoError: If the key is invalid
        """
        try:
            key_bytes = bytes.fromhex(key)
        except ValueError:
            raise CryptoError("Non-hexadecimal key")

        try:
            Fernet(key_bytes)
        except ValueError:
            raise CryptoError("Invalid key")

    @staticmethod
    def asymmetric_key(private_key: str, public_key: str) -> None:
        """
        Check if the hex value of the private and public key is correct
        :param private_key: Hex private key
        :param public_key: Hex public key
        :raise CryptoError: If the private or public key is invalid
        """
        try:
            private_key_bytes = bytes.fromhex(private_key)
            public_key_bytes = bytes.fromhex(public_key)
        except ValueError:
            raise CryptoError("Non-hexadecimal key")

        try:
            serialization.load_pem_private_key(private_key_bytes, password=None)
            serialization.load_pem_public_key(public_key_bytes)
        except ValueError:
            raise CryptoError("Invalid key")
