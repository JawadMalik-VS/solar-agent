from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Root route – Railway needs this
@app.route("/")
def home():
    return render_template("index.html")  # your frontend file

# API route
@app.route("/ask", methods=["POST"])
def ask():
    prompt = request.form.get("prompt")
    return jsonify({"response": prompt})