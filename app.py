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
    # call your agent logic here
    response = "Agent response: " + prompt
    return jsonify({"response": response})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
