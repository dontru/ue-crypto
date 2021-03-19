import hashlib
import logging
import random
import sqlite3
import string


class Database:
    DATABASE_NAME = 'database.db'
    LOGGING_CONFIG = {'level': logging.INFO}
    USERNAME_MIN_LEN = 3
    USERNAME_MAX_LEN = 16
    PASSWORD_MIN_LEN = 4
    SALT_LEN = 16
    SALT_ALPHABET = string.ascii_letters + string.digits + string.punctuation
    HASH_NAME = 'sha512'
    HASH_ITERATIONS = 10000
    CREATE_USERS = f"""
    CREATE TABLE Users (
        Id INT PRIMARY KEY,
        Name VARCHAR({USERNAME_MAX_LEN}) UNIQUE,
        Hash CHAR(128),
        Salt CHAR({SALT_LEN})
    );
    """

    def __init__(self):
        logging.basicConfig(**self.LOGGING_CONFIG)
        self.connection = sqlite3.connect(self.DATABASE_NAME)
        self.cursor = self.connection.cursor()

        # CREATE TABLE Users (if not exists)
        sql = 'SELECT COUNT(name) FROM sqlite_master WHERE name="Users"'
        table_users_exists = bool(self.cursor.execute(sql).fetchone()[0])
        if not table_users_exists:
            self.cursor.execute(self.CREATE_USERS)

    def shell(self) -> None:
        """Database interactive shell"""
        while True:
            print('1. Add user')
            print('2. Login')
            print('3. List of users')
            print('4. Quit')
            choice = input("Choice: ")

            if choice == "1":
                self.shell_add_user()
            elif choice == "2":
                self.shell_login()
            elif choice == "3":
                self.shell_list_of_users()
            elif choice == "4":
                break

            print('--------')

    def shell_add_user(self) -> None:
        """Ask user for username, password and repeat password"""
        username, password_1, password_2 = '', '', ''

        while not self.validate_username(username):
            username = input('Username: ')

        while not self.validate_passwords(password_1, password_2):
            password_1 = input('Password: ')
            password_2 = input('Repeat password: ')

        self.add_user(username=username, password=password_1)

    def validate_username(self, username: str) -> bool:
        return self.USERNAME_MIN_LEN <= len(username) < self.USERNAME_MAX_LEN

    def validate_passwords(self, password_1: str, password_2: str) -> bool:
        return self.validate_password(password_1) and password_1 == password_2

    def validate_password(self, password: str) -> bool:
        return len(password) >= self.PASSWORD_MIN_LEN

    def add_user(self, username: str, password: str) -> None:
        """Add user to the database"""
        try:
            hash_, salt = self.password_hash(password)
            self.execute('INSERT INTO Users VALUES (NULL, ?, ?, ?)', [username, hash_, salt])
            self.connection.commit()
            logging.info(f'User {username} added')
        except sqlite3.IntegrityError as e:
            if str(e) == 'UNIQUE constraint failed: Users.Name':
                logging.info(f'Username {username} is taken')
            else:
                logging.warning(f'Error while adding user: {e}')

    def password_hash(self, password: str) -> (str, str):
        """Generate hash and salt"""
        salt = self.generate_salt()
        hash_ = self.generate_hash(password=password, salt=salt)
        return hash_, salt

    def generate_salt(self) -> str:
        """Return random string"""
        return ''.join([random.choice(self.SALT_ALPHABET) for _ in range(self.SALT_LEN)])

    def generate_hash(self, password: str, salt: str) -> str:
        """Generate hash for given password and salt"""
        return hashlib.pbkdf2_hmac(
            hash_name=self.HASH_NAME,
            password=password.encode('utf-8'),
            salt=salt.encode('utf-8'),
            iterations=self.HASH_ITERATIONS,
        ).hex()

    def generate_hash_old(self, password: str, salt: str) -> str:
        """OLD: Generate hash for given password and salt"""
        return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

    def shell_login(self) -> None:
        """Ask user for username and password"""
        username, password = '', ''

        while not self.validate_username(username):
            username = input('Username: ')

        while not self.validate_password(password):
            password = input('Password: ')

        if self.password_verify(username=username, password=password):
            logging.info('Password verified')
        else:
            logging.info('Incorrect password ')

    def password_verify(self, username: str, password: str) -> bool:
        """Compare the password hash with the hash in database"""
        rows = self.execute('SELECT * FROM Users WHERE Name=?', [username]).fetchall()

        if len(rows) == 0:
            logging.warning(f'Username {username} does not exist')
            return False

        _, _, hash_, salt = rows[0]
        return hash_ == self.generate_hash(password=password, salt=salt)

    def shell_list_of_users(self) -> None:
        """View all users"""
        sql = 'SELECT * FROM Users'
        rows = self.execute(sql).fetchall()
        print(f'Username{" " * 8} Hash{" " * 12} Salt')
        for row in rows:
            print(f'{row[1]:16s} {row[2][:13]}... {row[3]}')

    def execute(self, *args, **kwargs) -> sqlite3.Cursor:
        """Execute an SQL statement"""
        return self.cursor.execute(*args, **kwargs)

    def __del__(self):
        self.connection.close()
