import random

words = ["apple", "sun", "river", "cloud", "happy", "star", "blue", "green"]

num_words = int(input("How many words in password? "))

password = "-".join(random.choice(words) for _ in range(num_words))

print("Generated Password:", password)
