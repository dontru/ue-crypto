from caesar.cipher import encrypt
from caesar.breaker import break_code


def main():
    text = 'To be or not to be'
    rot = 10
    encrypted = encrypt(text, rot)

    print(f'Text: {text}')
    print(f'Encrypted text: {encrypted}')

    break_code(encrypted)


if __name__ == '__main__':
    main()
