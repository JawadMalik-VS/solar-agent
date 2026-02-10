from flask import Flask, request, jsonify, send_from_directory
from mySolarAgent.agent import agent

app = Flask(__name__, static_folder=".")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/ask", methods=["POST"])
def ask():
    prompt = request.json["prompt"]
    response = agent(prompt)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=8000, debug=True)
