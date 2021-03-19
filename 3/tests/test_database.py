import sqlite3
import unittest

from src.Database import Database


class TestDatabase(unittest.TestCase):

    def test_init(self):
        database = Database()
        self.assertIsInstance(database, Database)

    def test_select(self):
        database = Database()
        sql = 'SELECT "Hello World!"'
        rows = database.execute(sql).fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(len(rows[0]), 1)
        self.assertEqual(rows[0][0], 'Hello World!')

    def test_users_if_exists(self):
        database = Database()
        sql = 'SELECT COUNT(name) FROM sqlite_master WHERE name="Users"'
        row = database.execute(sql).fetchone()
        self.assertEqual(row[0], 1)

    def test_users_select(self):
        try:
            database = Database()
            sql = 'SELECT * FROM Users'
            database.execute(sql).fetchall()
        except sqlite3.OperationalError:
            self.fail()

    def test_validate_username(self):
        database = Database()
        self.assertTrue(database.validate_username('username'))
        self.assertFalse(database.validate_username(''))
        self.assertFalse(database.validate_username('a' * 500))

    def test_validate_passwords(self):
        database = Database()
        self.assertTrue(database.validate_passwords('password', 'password'))
        self.assertFalse(database.validate_passwords('', ''))
        self.assertFalse(database.validate_passwords('password', 'asdf'))

    def test_validate_password(self):
        database = Database()
        self.assertTrue(database.validate_password('password'))
        self.assertFalse(database.validate_password(''))

    def test_create_user(self):
        try:
            database = Database()
            database.add_user('username', 'password')
            sql = 'SELECT COUNT(*) FROM Users WHERE Name="username"'
            row = database.execute(sql).fetchone()
            self.assertEqual(row[0], 1)
        except sqlite3.IntegrityError as e:
            self.assertEqual(str(e), 'UNIQUE constraint failed: Users.Name')

    def test_username_taken(self):
        try:
            database = Database()
            database.add_user('username', 'password')
            database.add_user('username', 'asdf')
        except sqlite3.IntegrityError:
            self.fail()

    def test_generate_salt(self):
        database = Database()
        salt_1 = database.generate_salt()
        salt_2 = database.generate_salt()
        self.assertNotEqual(salt_1, salt_2)

    def test_password_hash(self):
        database = Database()
        password_hash_1, salt_1 = database.password_hash('password')
        password_hash_2, salt_2 = database.password_hash('password')
        self.assertNotEqual(password_hash_1, password_hash_2)
        self.assertNotEqual(salt_1, salt_2)

    def test_password_verify(self):
        database = Database()
        database.add_user('username', 'password')
        self.assertTrue(database.password_verify('username', 'password'))


if __name__ == '__main__':
    unittest.main()
