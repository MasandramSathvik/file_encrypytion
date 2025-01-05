from flask import Flask, render_template, request
from cryptography.fernet import Fernet, InvalidToken
import os

app = Flask(__name__)

def generate_key():
    key = Fernet.generate_key()
    with open("Secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("Secret.key", "rb").read()

def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
        encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
        try:
            decrypted_data = f.decrypt(encrypted_data)
        except InvalidToken:
            return None
    return decrypted_data

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        choice = request.form.get("choice")
        filename = request.files["file"]
        if choice == "encrypt":
            if filename:
                generate_key()
                key = load_key()
                encrypt(filename.filename, key)
                message = "File Encrypted Successfully!!!"
            else:
                message = "Please select a file."
        elif choice == "decrypt":
            if filename:
                key = load_key()
                decrypted_data = decrypt(filename.filename, key)
                if decrypted_data:
                    with open("decrypted_" + filename.filename, "wb") as file:
                        file.write(decrypted_data)
                    message = "File Decrypted Successfully!!!"
                else:
                    message = "Invalid key or file is not encrypted."
            else:
                message = "Please select a file."
        return render_template("index.html", message=message)
    return render_template("index.html", message="")

if __name__ == "__main__":
    app.run(debug=True)
