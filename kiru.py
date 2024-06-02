import firebase_admin
from firebase_admin import credentials
from flask import Flask, request, jsonify
from firebase_admin import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for your app

# Initialize Firebase Admin SDK with your credentials
cred = credentials.Certificate(
    "C:\\Users\\vitht\\PycharmProjects\\pythonProject4\\firebase_db_connection\\test-71f04-firebase-adminsdk-70vbu-7a05af999c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-71f04-default-rtdb.firebaseio.com/'
})


@app.route('/login', methods=['POST'])
def login():
    # Data comes from the client (e.g., Ionic app)
    data = request.get_json()

    # Check if required fields are present
    if "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400

    email = data['email']
    password = data['password']

    ref = db.reference('client')
    clients = ref.get()

    if clients:
        for client_id, client_data in clients.items():
            print("client_id", client_id)
            print("client_data: ", client_data)
            print("client_email: ", client_data.get("email"))
            print("client_password: ", client_data.get("password"))
            print("Email: ", email)
            print("password: ", password)
            if client_data.get('email') == email and client_data.get('password') == password:
                # Successful login
                print("Login successfully")
                return jsonify({"message": "Login successfully"})

    # If no matching credentials are found
    print("Incorrect email or password")
    return jsonify({"error": "Incorrect email or password"}), 401


if __name__ == '__main__':
    app.run("localhost", 8001)
