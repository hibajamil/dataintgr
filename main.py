from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Function to fetch employee data from the simulated REST API
def get_employee_data():
    api_url = "https://65c767eee7c384aada6e7a22.mockapi.io/api/v1/user"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/get_employee_data", methods=["GET"])
def fetch_employee_data():
    employee_data = get_employee_data()
    if employee_data:
        return jsonify(employee_data)
    else:
        return jsonify({"error": "Failed to fetch employee data"})

if __name__ == "__main__":
    app.run(debug=True)
