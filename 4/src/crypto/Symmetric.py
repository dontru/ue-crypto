from cryptography.fernet import Fernet


class Symmetric:
    @staticmethod
    def generate_key() -> str:
        """
        Generate a random key
        :return: Hex key
        """
        return Fernet.generate_key().hex()

    @staticmethod
    def encrypt(text: str, key: str) -> str:
        """
        Encrypt the text with the key
        :param text: Plaintext
        :param key: Hex key
        :return: Encrypted text
        """
        f = Fernet(bytes.fromhex(key))
        return f.encrypt(text.encode('utf-8')).decode('utf-8')

    @staticmethod
    def decrypt(text: str, key: str) -> str:
        """
        Decrypt the encrypted text with the key
        :param text: Encrypted text
        :param key: Hex key
        :return: Plaintext
        """
        f = Fernet(bytes.fromhex(key))
        return f.decrypt(text.encode('utf-8')).decode('utf-8')
