import csv
import requests

# Define the URL for the POST route
POST_URL = "http://127.0.0.1:5000/students"

# Read data from the CSV file
with open("sample_data.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Prepare the data to send in the POST request
        customer_data = {
            "name": row["name"],
            "email": row["email"],
            "date_of_birth": row["dob"],
        }

        # Send a POST request to create the scooter
        response = requests.post(POST_URL, json=customer_data)

        # Check if the request was successful
        if response.status_code == 201:
            print(f"Student with id {row['id']} successfully created")
        else:
            print(f"Failed to create student with id {row['id']}: {response.text}")
