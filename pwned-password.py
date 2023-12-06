import hashlib
import getpass
import requests

def check_pwned_passwords(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    first_five_digits = sha1[:5]
    print(f"[INFO] sending partial hash ({first_five_digits}) of your full hash ({sha1}) to troyhunt.com to check")

    url = f'https://api.pwnedpasswords.com/range/{first_five_digits}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.text
        count = 0
        if sha1[5:] in data:
            _, count_str = data.split(sha1[5:] + ':')
            count = int(count_str)
        return count
    else:
        print(f"[ERROR] Unable to retrieve data from the server. Status Code: {response.status_code}")
        return 0

def get_password_input():
    password = getpass.getpass("Enter your password to check: ")
    print("\n[INFO] don't worry, will only use the first 5 characters of your password hash")
    return password

# check the password against Troy's DB
password = get_password_input()
count = check_pwned_passwords(password)

if count > 0:
    print(f"[WARN] Oops, your password is found {count} times!")
else:
    print("[INFO] Good news, your password is not found")
