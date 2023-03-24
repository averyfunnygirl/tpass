import json
import base64
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class PasswordManager:
    def __init__(self, password):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(password.encode())
        key = base64.urlsafe_b64encode(digest.finalize())
        self.fernet = Fernet(key)
        try:
            with open('passwords.json', 'rb') as file:
                encrypted_data = file.read()
                decrypted_data = self.fernet.decrypt(encrypted_data)
                self.passwords = json.loads(decrypted_data)
        except FileNotFoundError:
            self.passwords = {}

    def view_passwords(self):
        if not self.passwords:
            print('No passwords saved')
        else:
            for name, password in self.passwords.items():
                print(f'{name}: {password}')

    def add_password(self, name, password):
        self.passwords[name] = password
        self._save_passwords()

    def delete_password(self, name):
        del self.passwords[name]
        self._save_passwords()

    def _save_passwords(self):
        with open('passwords.json', 'wb') as file:
            encrypted_data = self.fernet.encrypt(json.dumps(self.passwords).encode())
            file.write(encrypted_data)

def main():
    master_password = getpass('Enter master password: ')
    password_manager = PasswordManager(master_password)

    while True:
        print('What do you want to do?')
        print('1. Add a password')
        print('2. Delete a password')
        print('3. View passwords')
        print('4. Quit')
        choice = input('> ')

        if choice == '1':
            name = input('Enter name: ')
            password = input('Enter password: ')
            password_manager.add_password(name, password)
        elif choice == '2':
            name = input('Enter name: ')
            password_manager.delete_password(name)
        elif choice == '3':
            password_manager.view_passwords()
        elif choice == '4':
            break
        else:
            print('Invalid choice')

if __name__ == '__main__':
    main()
