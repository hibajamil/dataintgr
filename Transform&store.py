from flask import Flask, render_template, jsonify
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
import requests
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='employee_processing.log', level=logging.INFO)

# Database setup
Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    identifier = Column(String)
    fullName = Column(String)
    dateOfBirth = Column(Date)
    age = Column(Integer)

# Configure SQLAlchemy to use SQLite database
engine = create_engine('sqlite:///users-db.db')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)

# Function to fetch employee data from the simulated REST API
def get_employee_data():
    api_url = "https://65c767eee7c384aada6e7a22.mockapi.io/api/v1/user"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to calculate age from date of birth
def calculate_age(dob):
    today = datetime.now().date()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

# Function to process and store employee data
def process_and_store_employees():
    employee_data = get_employee_data()
    if employee_data:
        session = Session()
        for employee in employee_data:
            # Parse date with updated format
            dob = datetime.strptime(employee['dateOfBirth'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
            age = calculate_age(dob)
            if age > 18:
                full_name = employee['firstName'] + ' ' + employee['lastName']
                identifier = employee['id']
                # Create Employee object
                new_employee = Employee(identifier=identifier, fullName=full_name, dateOfBirth=dob, age=age)
                # Add to the session
                session.add(new_employee)
                # Log the processed employee
                logging.info(f"Processed employee - ID: {identifier}, Full Name: {full_name}, Age: {age}, Date: {datetime.now()}")
        # Commit changes to the database
        session.commit()
        # Close the session
        session.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_employee_data", methods=["GET"])
def fetch_employee_data():
    employee_data = get_employee_data()
    if employee_data:
        return jsonify(employee_data)
    else:
        return jsonify({"error": "Failed to fetch employee data"})

@app.route("/process_and_store_employees", methods=["GET"])
def process_and_store_employees_route():
    process_and_store_employees()
    return jsonify({"message": "Employees processed and stored successfully."})
# Function to process and store employee data

def process_and_store_employees():
    employee_data = get_employee_data()
    if employee_data:
        session = Session()
        for employee in employee_data:
            # Parse date with updated format
            dob = datetime.strptime(employee['dateOfBirth'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
            age = calculate_age(dob)
            if age > 18:
                full_name = employee['firstName'] + ' ' + employee['lastName']
                identifier = employee['id']
                # Create Employee object
                new_employee = Employee(identifier=identifier, fullName=full_name, dateOfBirth=dob, age=age)
                # Add to the session
                session.add(new_employee)
                # Log the processed employee
                logging.info(f"Processed employee - ID: {identifier}, Full Name: {full_name}, Age: {age}, Date: {datetime.now()}")
        # Commit changes to the database
        session.commit()
        # Close the session
        session.close()

if __name__ == "__main__":
    app.run(debug=True)
