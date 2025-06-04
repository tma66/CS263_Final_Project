import argparse
from cryptography.fernet import Fernet

def generate_key(password):
    return Fernet.generate_key()

def load_key(key_path):
    with open(key_path, 'rb') as key_file:
        return key_file.read()

def encrypt_file(file_path, key):
    f = Fernet(key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(file_path, key):
    f = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a file.')
    parser.add_argument('action', choices=['encrypt', 'decrypt'], help='Action to perform on the file')
    parser.add_argument('file_path', type=str, help='Path to the file to encrypt or decrypt')
    parser.add_argument('--password', type=str, help='Password for encryption (not used in this example)')
    parser.add_argument('--key-path', type=str, required=True, help='Path to the key file')

    args = parser.parse_args()

    key = load_key(args.key_path)

    if args.action == 'encrypt':
        encrypt_file(args.file_path, key)
        print(f"File {args.file_path} has been encrypted.")
    elif args.action == 'decrypt':
        decrypt_file(args.file_path, key)
        print(f"File {args.file_path} has been decrypted.")

if __name__ == '__main__':
    main()