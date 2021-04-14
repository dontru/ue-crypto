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
        self.assertEqual(cipher.encrypt('12345678'), '21346578')
        self.assertEqual(cipher.decrypt('21346578'), '12345678')

    def test_row_transpositions(self):
        cipher = Cipher(substitution={}, row_transpositions=[(2, 3), (6, 7)])
        self.assertEqual(cipher.encrypt('1\n2\n3\n4\n5\n6\n7\n8'), '1\n2\n4\n3\n5\n6\n8\n7')
        self.assertEqual(cipher.decrypt('1\n2\n4\n3\n5\n6\n8\n7'), '1\n2\n3\n4\n5\n6\n7\n8')

    def test_transpositions(self):
        cipher = Cipher(
            substitution={},
            col_transpositions=[(2, 3)],
            row_transpositions=[(0, 1)],
        )
        plaintext = 'abcdefgh12345678ijk'
        encrypted = '12435678\nabdcefgh\nij k'
        self.assertEqual(cipher.encrypt(plaintext), encrypted)
        self.assertEqual(cipher.decrypt(encrypted), plaintext)


if __name__ == '__main__':
    unittest.main()
