import unittest

from homophonic import Cipher


class CipherTest(unittest.TestCase):
    def test_encrypt(self):
        cipher = Cipher(substitution={'a': ['0', '1'], 'b': ['2']})
        encrypted = cipher.encrypt('abcd')
        self.assertTrue(encrypted == '02cd' or encrypted == '12cd')

    def test_decrypt(self):
        cipher = Cipher(substitution={'a': ['0', '1'], 'b': ['2']})
        self.assertEqual(cipher.decrypt('02cd'), 'abcd')
        self.assertEqual(cipher.decrypt('12cd'), 'abcd')

    def test_col_transpositions(self):
        cipher = Cipher(substitution={}, col_transpositions=[(0, 1), (4, 5)])
        plaintext = 'abcdefgh'
        encrypted = 'bacdfegh'
        self.assertEqual(cipher.encrypt(plaintext), encrypted)
        self.assertEqual(cipher.decrypt(encrypted), plaintext)

    def test_row_transpositions(self):
        cipher = Cipher(substitution={}, row_transpositions=[(2, 3), (6, 7)])
        plaintext = '\n'.join([c * 8 for c in 'abcdefgh'])
        encrypted = '\n'.join([c * 8 for c in 'abdcefhg'])
        self.assertEqual(cipher.encrypt(plaintext), encrypted)
        self.assertEqual(cipher.decrypt(encrypted), plaintext)

    def test_transpositions(self):
        cipher = Cipher(
            substitution={},
            col_transpositions=[(2, 3)],
            row_transpositions=[(0, 1)],
        )
        plaintext = 'abcdefgh\nmmmmmmmm\nijk'
        encrypted = 'mmmmmmmm\nabdcefgh\nij k'
        self.assertEqual(cipher.encrypt(plaintext), encrypted)
        self.assertEqual(cipher.decrypt(encrypted), plaintext)


if __name__ == '__main__':
    unittest.main()
