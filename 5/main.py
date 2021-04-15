import logging
from collections import Counter

import homophonic


def main():
    logging.basicConfig(level=logging.INFO)

    substitution = {
        'a': ['0', '1'],
        'b': ['2'],
    }
    col_transpositions = [(0, 1)]
    row_transpositions = [(2, 3)]

    with open('plaintext.txt') as input_file, open('encrypted.txt', 'w+') as output_file:
        plaintext = input_file.read()
        cipher = homophonic.Cipher(substitution=substitution,
                                   col_transpositions=col_transpositions,
                                   row_transpositions=row_transpositions)
        encrypted = cipher.encrypt(plaintext)
        output_file.write(encrypted)

        logging.info(f'Encrypted lines: {len(encrypted.splitlines())}')
        logging.info(f'Encrypted len: {len(encrypted)}')
        logging.info('Encrypted len without newlines: {}'.format(len([c for c in encrypted if c != '\n'])))
        logging.info(f'Distribution: {Counter(encrypted)}')
        logging.info(f'Encrypted: \n{encrypted[:9 * 8 - 1]}...')
        logging.info(f'Decrypted: \n{cipher.decrypt(encrypted)[:9 * 8 - 1]}...')


if __name__ == '__main__':
    main()
