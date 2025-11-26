import hashlib

document = input("Enter message to sign: ")

# Sender creates a signature
signature = hashlib.sha256(document.encode()).hexdigest()
print("Digital Signature:", signature)

# Receiver verifies
verify_text = input("Enter received message: ")
verify_signature = hashlib.sha256(verify_text.encode()).hexdigest()

if verify_signature == signature:
    print("Signature Verified ✔ Document is authentic.")
else:
    print("Verification Failed ✘ Document was changed.")
