from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mortgage calculation function
def calculate_mortgage(principal, annual_rate, years):
    monthly_rate = annual_rate / 100 / 12
    total_months = years * 12
    if monthly_rate != 0:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** total_months) / ((1 + monthly_rate) ** total_months - 1)
    else:
        monthly_payment = principal / total_months
    total_payment = monthly_payment * total_months
    total_interest = total_payment - principal
    return monthly_payment, total_payment, total_interest


# API endpoint for mortgage calculation
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json  # Get JSON data from the request
        principal = float(data['principal'])
        annual_rate = float(data['annual_rate'])
        years = int(data['years'])
        
        # Perform calculation
        monthly_payment, total_payment, total_interest = calculate_mortgage(principal, annual_rate, years)

        # Return JSON response
        return jsonify({
            "monthly_payment": round(monthly_payment, 2),
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_interest, 2)
        })
    except (KeyError, ValueError) as e:
        return jsonify({"error": "Invalid input"}), 400

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
