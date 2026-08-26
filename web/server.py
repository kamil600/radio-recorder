from flask import Flask, send_from_directory, render_template
import os

app = Flask(__name__)

RECORDINGS_DIR = "../worker/recordings"
LOG_FILE = "../worker/radio.log"

@app.route("/")
def index():
    files = []
    if os.path.exists(RECORDINGS_DIR):
        files = sorted(os.listdir(RECORDINGS_DIR))
    return render_template("index.html", files=files)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(RECORDINGS_DIR, filename, as_attachment=True)

@app.route("/logs")
def logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    return "Brak logów."

# Tryb lokalny (dev mode)
if __name__ == "__main__":
    print("Uruchamiasz aplikację lokalnie (dev mode).")
    app.run(host="0.0.0.0", port=5000, debug=True)
