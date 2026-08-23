from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import requests
import os

app = Flask(__name__, static_folder="../frontend")

# Database setup
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS searches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )""")
    conn.commit()
    conn.close()

init_db()

# Serve frontend index.html at root
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

# Serve static files (CSS, JS)
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Search API
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")

    # Save query to local DB
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO searches (query) VALUES (?)", (query,))
    conn.commit()
    conn.close()

    # DuckDuckGo Instant Answer API
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    try:
        response = requests.get(url)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    # Run with HTTPS using self-signed certs
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=("cert.pem", "key.pem"))
