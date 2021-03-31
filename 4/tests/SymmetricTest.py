import unittest

from crypto.Symmetric import Symmetric


class SymmetricTest(unittest.TestCase):

    def test_generate_key_len(self):
        key = Symmetric.generate_key()
        self.assertEqual(len(key), 88)

    def test_generate_key_hex(self):
        key = Symmetric.generate_key()
        try:
            int(key, 16)
        except ValueError:
            self.fail()

    def test_encryption(self):
        key = Symmetric.generate_key()
        encrypted = Symmetric.encrypt('my secret', key)
        decrypted = Symmetric.decrypt(encrypted, key)
        self.assertEqual(decrypted, 'my secret')


if __name__ == '__main__':
    unittest.main()
