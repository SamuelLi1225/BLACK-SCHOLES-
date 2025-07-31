from flask import Flask, request, jsonify
from flask_cors import CORS
import math
from scipy.stats import norm

app = Flask(__name__)
CORS(app)

def black_scholes(S, K, T, r, sigma, option_type):
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    else:
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

@app.route("/price", methods=["POST"])
def price():
    data = request.get_json()
    S = float(data["stockPrice"])
    K = float(data["strikePrice"])
    T = float(data["timeToMaturity"])
    r = float(data["interestRate"])
    sigma = float(data["volatility"])
    option_type = data["optionType"]
    result = black_scholes(S, K, T, r, sigma, option_type)
    return jsonify({"price": round(result, 2)})

@app.route("/")
def home():
    return "Black-Scholes API is running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
