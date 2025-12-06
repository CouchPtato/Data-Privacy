# 1. `CaesarCipher.py` – Caesar cipher encryption/decryption.

def encrypt(text : str, key : int) -> str:
    result = ""

    for i in range(len(text)):
        char = text[i]

        if (char.isupper()):
            result += chr((ord(char) + key - 65) % 26 + 65)

        else:
            result += chr((ord(char) + key - 97) % 26 + 97)

    return result

def decrypt(text : str, key : int) -> str:
    result = ""

    for i in range(len(text)):
        char = text[i]

        if (char.isupper()):
            result += chr((ord(char) - key - 65) % 26 + 65)

        else:
            result += chr((ord(char) - key - 97) % 26 + 97)

    return result

text = "abcdefgh"
key = 4
cipher_text = encrypt(text,key)
print(cipher_text)
print(decrypt(cipher_text, key))

# 2. `RailFence.py` – Rail Fence cipher encryption/decryption.

def encryptRailFence(text : str, key : int) -> str:

    rail = [['*' for i in range(len(text))]
                for j in range(key)]
    
    dir_down = True
    row, col = 0, 0
    
    for i in range(len(text)):
        
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False

        rail[row][col] = text[i]
        col += 1
        
        if dir_down:
            row += 1
        else:
            row -= 1

    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '*':
                result.append(rail[i][j])
    ans = "".join(result)
    return ans
    
def decryptRailFence(cipher : str, key : int) -> str:
    n = len(cipher)
    pattern = []
    row = 0
    dir_down = True

    for i in range(n):
        pattern.append(row)
        if row == 0:
            dir_down = True
        elif row == key - 1:
            dir_down = False
        row += 1 if dir_down else -1

    per_row_counts = [pattern.count(r) for r in range(key)]

    rows = []
    idx = 0

    for count in per_row_counts:
        cipher_idx = idx + count
        rows.append(list(cipher[idx : cipher_idx]))
        idx += count

    result = []
    row_ptrs = [0] * key

    for r in pattern:
        result.append(rows[r][row_ptrs[r]])
        row_ptrs[r] += 1

    ans = "".join(result)
    return ans

def main():
    print(encryptRailFence("My name is Lasagna", 3))
    print(decryptRailFence("Maianynm sLsga e a", 3))

if __name__ == "__main__":
    main()

# 3. `SHA256.py` – SHA-256 password hashing.

import hashlib

str = "My password is : Password"

result = hashlib.sha256(str.encode())

print("The hexadecimal equivalent of SHA256 is : ")
print(result.hexdigest())

print ("\r")

str = "My password is : Password"

result = hashlib.sha384(str.encode())

print("The hexadecimal equivalent of SHA384 is : ")
print(result.hexdigest())

print ("\r")

str = "My password is : Password"

result = hashlib.sha224(str.encode())

print("The hexadecimal equivalent of SHA224 is : ")
print(result.hexdigest())

print ("\r")

str = "My password is : Password"

result = hashlib.sha512(str.encode())

print("The hexadecimal equivalent of SHA512 is : ")
print(result.hexdigest())

print ("\r")

str = "My password is : Password"

result = hashlib.sha1(str.encode())

print("The hexadecimal equivalent of SHA1 is : ")
print(result.hexdigest())

# 4. `CheckPwned.py` – Check leaked passwords via Have I Been Pwned.
# 5. `RandomPassword.py` – Generate passphrase-style passwords from dictionary words.
# 6. `BruteForceAttack.py` – Simulated brute-force attack on simple passwords.



