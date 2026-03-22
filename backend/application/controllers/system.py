from app import app   # import the actual app object
from flask import jsonify

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
