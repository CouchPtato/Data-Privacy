import hashlib
import requests

def check_password(password):
    # SHA-1 hash of password
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    # Call HIBP API
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    # Look for matching suffix
    for line in response.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)
    return 0


username = input("Enter username: ")
password = input("Enter password: ")

count = check_password(password)

if count > 0:
    print(f"{username}: ❌ Password found {count} times in data breaches.")
else:
    print(f"{username}: ✅ Password NOT found. Safe to use.")
