import os
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    return key

def load_key(key_file):
    try:
        with open(key_file, "rb") as key_f:
            key = key_f.read()
        return key
    except FileNotFoundError:
        print("Key file not found.")
        return None

def encrypt(plaintext, password):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(plaintext.encode())
    with open(password + "_key.txt", "wb") as key_f:
        key_f.write(key)
    return cipher_text, key

def decrypt(cipher_text, key_file):
    key = load_key(key_file)
    if not key:
        return None
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text).decode()
    return plain_text

if __name__ == "__main__":
    print("1. Generate Key")
    print("2. Encrypt File")
    print("3. Decrypt File")
    choice = input("Enter your choice: ")

    if choice == "1":
        key_file = input("Enter the name of the file to store the key (without extension): ")
        key = generate_key()
        with open(key_file + "_key.txt", "wb") as key_f:
            key_f.write(key)
        print("Key generated and saved.")

    elif choice == "2":
        password = input("Enter password: ")
        algorithm = input("Choose an encryption algorithm (Fernet): ")
        file_path = input("Enter the path to the file you want to encrypt: ")
        
        if not os.path.exists(file_path):
            print("File does not exist.")
            exit()
        
        with open(file_path, "rb") as f:
            plaintext = f.read()

        cipher_text, key = encrypt(plaintext, password)
        print("File encrypted.")

    elif choice == "3":
        key_file = input("Enter the name of the file that contains the encryption key (without extension): ")
        algorithm = input("Choose an decryption algorithm (Fernet): ")
        file_path = input("Enter the path to the encrypted file: ")

        if not os.path.exists(file_path):
            print("File does not exist.")
            exit()

        with open(file_path, "rb") as f:
            cipher_text = f.read()

        plain_text = decrypt(cipher_text, key_file + "_key.txt")
        if not plain_text:
            print("Decryption failed. Key file not found.")
        else:
            print("File decrypted.")

    else:
        print("Invalid choice.")