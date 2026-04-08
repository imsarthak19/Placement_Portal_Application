from app import app   # import the actual app object
from flask import jsonify

@app.route("/")
def index():
    return "<h1>Welcome to the Placement Portal API</h1>" \
            "The Server is Running!" \
            "<p>Use /api/ for API endpoints.</p>" \
            "<p>Example: <a href='/api/health'>/api/health</a></p>" \
            "<p>Documentation: <a href='/api/docs'>/api/docs</a></p>" \

@app.route("/api/")
def home():
    return jsonify({
        "message": "Placement Portal API running"
    })

@app.route("/api/health")
def health():
    return jsonify({
        "status": "OK"
    })
