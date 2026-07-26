from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# ============================================
# 🔥 GANTI DENGAN API KEY KAMU
# ============================================
genai.configure(api_key="AQ.Ab8RN6loIxGhLVLXDPYvbdUIBetJj9WpyWZ7hlwcNFsLbL1BSA")

DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": [], "designs": []}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def root():
    return jsonify({"message": "🚀 API AI JALAN!"})

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    db = load_db()
    for user in db["users"]:
        if user["email"] == data.get("email"):
            return jsonify({"success": False, "message": "Email sudah terdaftar"}), 400
    db["users"].append({
        "id": len(db["users"]) + 1,
        "email": data.get("email"),
        "password": data.get("password"),
        "name": data.get("name") or data.get("email").split("@")[0]
    })
    save_db(db)
    return jsonify({"success": True, "message": "Registrasi berhasil"})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    db = load_db()
    for user in db["users"]:
        if user["email"] == data.get("email") and user["password"] == data.get("password"):
            return jsonify({"success": True, "message": "Login berhasil", "user": user})
    return jsonify({"success": False, "message": "Email atau password salah"}), 401

@app.route("/api/ai", methods=["POST"])
def ai():
    data = request.json
    prompt = data.get("prompt", "")

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"❌ Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
