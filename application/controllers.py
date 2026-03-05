from app import app   # import the actual app object

@app.route("/")
def home():
    return "Hello World!"