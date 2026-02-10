# server.py
# from flask import Flask, request, jsonify
# import math

# app = Flask(__name__)

# # Example: Solar savings tool
# def calculate_solar_savings(consumption_kwh: float, rate_per_kwh: float):
#     return round(consumption_kwh * rate_per_kwh * 0.8, 2)  # 20% savings assumption

# @app.route("/tool/calculate_solar", methods=["POST"])
# def solar_tool():
#     data = request.json
#     consumption = data.get("consumption_kwh")
#     rate = data.get("rate_per_kwh")
#     savings = calculate_solar_savings(consumption, rate)
#     return jsonify({"estimated_savings": savings})

# if __name__ == "__main__":
#     app.run(port=5000)


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
