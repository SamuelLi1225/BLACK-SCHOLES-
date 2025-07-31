from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

def black_scholes(S, K, T, r, sigma, option_type):
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))

    if option_type == 'Call':
        return round(S * N(d1) - K * math.exp(-r * T) * N(d2), 2)
    elif option_type == 'Put':
        return round(K * math.exp(-r * T) * N(-d2) - S * N(-d1), 2)
    else:
        raise ValueError("Invalid option type. Must be 'Call' or 'Put'.")

@app.route('/')
def home():
    return "Black-Scholes API is running!"

@app.route('/price', methods=['POST'])
def price():
    try:
        data = request.get_json()
        S = float(data['S'])
        K = float(data['K'])
        T = float(data['T'])
        r = float(data['r'])
        sigma = float(data['sigma'])
        option_type = data['option_type']

        price = black_scholes(S, K, T, r, sigma, option_type)
        return jsonify({'price': price})

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/price-table', methods=['POST'])
def price_table():
    try:
        data = request.get_json()
        S = float(data['S'])
        T = float(data['T'])
        r = float(data['r'])
        option_type = data['option_type']

        strikes = [i for i in range(int(S * 0.8), int(S * 1.2) + 1, 5)]
        volatilities = [round(i * 0.01, 2) for i in range(10, 51, 5)]  # 0.10 to 0.50 step 0.05

        table = []
        for sigma in volatilities:
            row = []
            for K in strikes:
                price = black_scholes(S, K, T, r, sigma, option_type)
                row.append(price)
            table.append(row)

        return jsonify({
            'strikes': strikes,
            'volatilities': volatilities,
            'table': table
        })

    except Exception as e:
        print(f"❌ ERROR in table: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
