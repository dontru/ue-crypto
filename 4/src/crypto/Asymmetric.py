from typing import Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


class Asymmetric:
    @staticmethod
    def generate_private_key() -> rsa.RSAPrivateKey:
        """
        Generate a new private key
        :return: RSA private key
        """
        return rsa.generate_private_key(public_exponent=65537, key_size=2048)

    @staticmethod
    def generate_key() -> Tuple[str, str]:
        """
        Generate a new private and public key
        :return: (hex private key, hex public key)
        """
        private_key = Asymmetric.generate_private_key()

        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        pub_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return pem.hex(), pub_pem.hex()

    @staticmethod
    def generate_key_openssh() -> Tuple[str, str]:
        """
        Generate a new private and public key in OpenSSH format
        :return: (hex private key, hex public key)
        """
        private_key = Asymmetric.generate_private_key()

        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.OpenSSH,
            encryption_algorithm=serialization.NoEncryption()
        )

        pub_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH
        )

        return pem.hex(), pub_pem.hex()

    @staticmethod
    def sign(text: str, private_key: str) -> str:
        """
        Sigh the text with private key
        :param text: Plaintext to sign
        :param private_key: Hex private key
        :return: Hex signature
        """
        key = serialization.load_pem_private_key(bytes.fromhex(private_key), password=None)
        signature = key.sign(
            data=text.encode('utf-8'),
            padding=padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            algorithm=hashes.SHA256()
        )
        return signature.hex()

    @staticmethod
    def verify(signature: str, text: str, public_key: str) -> bool:
        """
        Verify the signature of the text
        :param signature: Hex signature
        :param text: Plaintext
        :param public_key: Hex public key
        :return: Verification
        """
        key = serialization.load_pem_public_key(bytes.fromhex(public_key))
        try:
            key.verify(
                signature=bytes.fromhex(signature),
                data=text.encode('utf-8'),
                padding=padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                algorithm=hashes.SHA256()
            )
        except (ValueError, InvalidSignature):
            return False
        else:
            return True

    @staticmethod
    def encrypt(text: str, public_key: str) -> str:
        """
        Encrypt the text with the public key
        :param text: Plaintext
        :param public_key: Hex public key
        :return: Hex encrypted text
        """
        key = serialization.load_pem_public_key(bytes.fromhex(public_key))
        ciphertext = key.encrypt(
            plaintext=text.encode('utf-8'),
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return ciphertext.hex()

    @staticmethod
    def decrypt(text: str, private_key: str) -> str:
        """
        Decrypt the encrypted text with the private key
        :param text: Hex encrypted text
        :param private_key: Hex key
        :return: Plaintext
        """
        key = serialization.load_pem_private_key(bytes.fromhex(private_key), password=None)
        plaintext = key.decrypt(
            ciphertext=bytes.fromhex(text),
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return plaintext.decode('utf-8')
