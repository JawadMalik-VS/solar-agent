from flask import Flask, request, render_template, jsonify

app = Flask(__name__, template_folder="templates", static_folder="static")

# Root route – Railway needs this
@app.route("/")
def home():
    return render_template("index.html")  # your frontend file

# API route
@app.route("/ask", methods=["POST"])
def ask():
    prompt = request.form.get("prompt")
    return jsonify({"response": prompt})
@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
