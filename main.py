
from flask import Flask, request, jsonify
from urllib.parse import urlparse
import re
import os

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({
        "name": "Telegram File Downloader",
        "status": "online",
        "version": "1.0"
    })

@app.get("/api/download")
def download():
    url = request.args.get("url", "").strip()

    try:
        parsed = urlparse(url)

        if parsed.hostname not in (
            "t.me", "www.t.me",
            "telegram.me", "www.telegram.me"
        ):
            return jsonify({"error": "Invalid Telegram URL"}), 400

        match = re.match(
            r"^/(?:s/)?([A-Za-z0-9_]+)/(\d+)",
            parsed.path
        )

        if not match:
            return jsonify({"error": "Invalid post URL"}), 400

        channel, post_id = match.groups()

        return jsonify({
            "status": "pending",
            "channel": channel,
            "post_id": post_id,
            "message": "Telegram media handler is not connected yet"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
  
