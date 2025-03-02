from cryptography.fernet import Fernet

log_file = "keylog.txt"
key_file = "encryption_key.key"

# Load the saved key
with open(key_file, "rb") as f:
    key = f.read()

cipher = Fernet(key)

# Read and decrypt logs
with open(log_file, "r") as f:
    encrypted_logs = f.readlines()

print("\nDecrypted Logs:\n")
for line in encrypted_logs:
    try:
        decrypted_text = cipher.decrypt(line.strip().encode()).decode()
        print(decrypted_text, end="")
    except:
        print("\n[Error: Could not decrypt line]")