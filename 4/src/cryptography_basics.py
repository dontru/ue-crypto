import logging as log

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def symmetric():
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(b'my secret')
    log.info(token)
    log.info(f.decrypt(token))


def asymmetric_private_and_public_key():
    # Private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    log.info(f'Private key: {pem}')

    # Public key
    pub_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    log.info(f'Public key: {pub_pem}')


def asymmetric():
    # Encrypt and decrypt
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    clear_text = 'Ala has a cat'.encode('utf-8')

    for _ in range(2):
        ciphertext = public_key.encrypt(clear_text, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ))
        log.info(f'Ciphertext: {ciphertext.hex()}')


def main():
    log.basicConfig(level=log.DEBUG)
    symmetric()
    asymmetric_private_and_public_key()
    asymmetric()


if __name__ == '__main__':
    main()
