from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/tool/calculate_solar", methods=["POST"])
def calculate_solar():
    data = request.json
    consumption_kwh = float(data["consumption_kwh"])
    rate_per_kwh = float(data["rate_per_kwh"])

    monthly_cost = consumption_kwh * rate_per_kwh
    estimated_savings = round(monthly_cost * 0.7, 2)  # 70% savings assumption

    return jsonify({
        "estimated_savings": estimated_savings
    })

if __name__ == "__main__":
    app.run(port=5000)
