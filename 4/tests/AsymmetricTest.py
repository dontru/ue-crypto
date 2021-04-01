import unittest

from cryptography.exceptions import InvalidSignature

from crypto.Asymmetric import Asymmetric


class AsymmetricTest(unittest.TestCase):

    def test_generate_key(self):
        private_key, public_key = Asymmetric.generate_key()
        self.assertNotEqual(private_key, '')
        self.assertNotEqual(public_key, '')
        self.assertNotEqual(private_key, public_key)
        try:
            int(private_key, 16)
            int(public_key, 16)
        except ValueError:
            self.fail()

    def test_generate_key_openssh(self):
        private_key, public_key = Asymmetric.generate_key_openssh()
        self.assertNotEqual(private_key, '')
        self.assertNotEqual(public_key, '')
        self.assertNotEqual(private_key, public_key)
        try:
            int(private_key, 16)
            int(public_key, 16)
        except ValueError:
            self.fail()

    def test_sign_verify(self):
        private_key, public_key = Asymmetric.generate_key()
        text = 'my text'
        signature = Asymmetric.sign(text, private_key)
        try:
            Asymmetric.verify(signature, text, public_key)
        except InvalidSignature:
            self.fail()

    def test_sign_verify_different_key(self):
        private_key, _ = Asymmetric.generate_key()
        _, public_key = Asymmetric.generate_key()
        text = 'my text'
        signature = Asymmetric.sign(text, private_key)
        with self.assertRaises(InvalidSignature):
            Asymmetric.verify(signature, text, public_key)

    def test_encryption(self):
        private_key, public_key = Asymmetric.generate_key()
        encrypted = Asymmetric.encrypt('my secret', public_key)
        decrypted = Asymmetric.decrypt(encrypted, private_key)
        self.assertEqual(decrypted, 'my secret')


if __name__ == '__main__':
    unittest.main()
