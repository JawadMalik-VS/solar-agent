from flask import Flask, render_template, request, jsonify, send_from_directory
from agent import agent
import os

app = Flask(__name__, static_folder=".")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    prompt = request.json["prompt"]
    response = agent(prompt)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=8000, debug=True)
