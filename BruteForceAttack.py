import itertools
import string

password = input("Enter a small password: ")
chars = string.ascii_lowercase

found = False
attempts = 0

for length in range(1, len(password) + 1):
    for combo in itertools.product(chars, repeat=length):
        attempts += 1
        guess = "".join(combo)

        if guess == password:
            print("Password found:", guess)
            print("Attempts:", attempts)
            found = True
            break
    if found:
        break

if not found:
    print("Password not found within length limit.")
