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