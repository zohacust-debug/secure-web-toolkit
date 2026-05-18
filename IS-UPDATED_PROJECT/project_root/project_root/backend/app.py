from flask import Flask, render_template, request, jsonify, send_file
import os
from services.crypto import encrypt_file, decrypt_file
from services.scan_manager import create_scan, get_scan_status
from services.chatbot import get_reply  # Now this will work

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- Pages ---------- #
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/scanner')
def scanner_page():
    return render_template("scanner.html")

@app.route('/encrypt')
def encrypt_page():
    return render_template("encrypt.html")

@app.route('/chatbot')
def chatbot_page():
    return render_template("chatbot.html")  # Make sure this is your blue UI

# ---------- API Routes ---------- #
@app.route("/api/scan_async", methods=["POST"])
def scan_async():
    data = request.json
    url = data.get("url")
    mode = data.get("mode", "fast")
    if not url:
        return jsonify({"error": "URL missing"}), 400
    scan_id = create_scan(url)
    return jsonify({"scan_id": scan_id})

@app.route("/api/scan_status/<scan_id>")
def scan_status(scan_id):
    status = get_scan_status(scan_id)
    return jsonify(status)

@app.route("/api/encrypt", methods=["POST"])
def encrypt_api():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    encrypted_path = encrypt_file(filepath)
    return send_file(encrypted_path, as_attachment=True)

@app.route("/api/decrypt", methods=["POST"])
def decrypt_api():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    decrypted_path = decrypt_file(filepath)
    return send_file(decrypted_path, as_attachment=True)

# ---------- Chatbot API ---------- #

@app.route("/api/chat", methods=["POST"])
def chat_api():
    msg = request.json.get("message", "").strip()
    if not msg:
        return jsonify({"reply": "Please enter a question."})
    reply = get_reply(msg)
    return jsonify({"reply": reply})


# ---------- Run App ---------- #
if __name__ == "__main__":
    app.run(debug=True)
