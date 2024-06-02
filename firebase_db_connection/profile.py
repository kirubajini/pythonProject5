import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for your app

# Initialize Firebase Admin SDK
cred = credentials.Certificate("C:\\Users\\vitht\\PycharmProjects\\pythonProject4\\firebase_db_connection\\test-71f04-firebase-adminsdk-70vbu-7a05af999c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-71f04-default-rtdb.firebaseio.com/'
})

@app.route('/save_profile', methods=['POST'])
def save_profile():
    # Get the JSON data from the request
    data = request.get_json()
    print("Profile data received: ", data)

    # Check if required fields are present
    if "fullName" not in data or "email" not in data or "phoneNumber" not in data or "address" not in data or "dob" not in data:
        return jsonify({"error": "Missing details"}), 400

    fullName = data['fullName']
    email = data['email']
    phoneNumber = data['phoneNumber']
    address = data['address']
    dob = data['dob']

    # Reference to the profiles node in Firebase
    ref = db.reference('profiles')

    # Save the profile data to Firebase
    new_profile_ref = ref.push({
        'fullName': fullName,
        'email': email,
        'phoneNumber': phoneNumber,
        'address': address,
        'dob': dob
    })

    # Return a success response
    return jsonify({"message": "Profile data saved successfully", "profile_id": new_profile_ref.key}), 200

if __name__ == '__main__':
    app.run("localhost", 3000)
