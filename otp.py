import firebase_admin
from firebase_admin import credentials
from flask import Flask, request, jsonify
from firebase_admin import db
import smtplib
import re
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for your app

cred = credentials.Certificate(
    "C:\\Users\\vitht\\PycharmProjects\\pythonProject4\\firebase_db_connection\\test-71f04-firebase-adminsdk-70vbu-7a05af999c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-71f04-default-rtdb.firebaseio.com//'
})

# Set your SMTP email and password here
smtp_email = 'viththiarul67@gmail.com'  # Replace with your SMTP email
smtp_password = 'CWURrjTgOcF29V7h'  # Replace with your SMTP password
smtp_server = 'smtp-relay.brevo.com'  # Replace with your email provider's SMTP server
smtp_port = 587  # Replace with the appropriate port (587 for TLS, 465 for SSL, etc.)
from_email = 'viththiarul67@gmail.com'
subject = 'Your OTP'


@app.route('/otp', methods=['POST'])
def signup():
    # Data comes from postman
    data = request.get_json()
    print("data: ", data)

    # Check if required fields are present
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400

    email = data['email']
    print("email: ", email)

    ref = db.reference('client')
    clients = ref.get()

    try:
        if clients:
            for client_id, client_data in clients.items():
                if client_data['email'] == email:
                    # Generate OTP and update in database
                    otp = str(random.randint(1000, 9999))  # Generate a 4-digit OTP
                    ref.child(client_id).update({"otp": otp})

                    # Send OTP via email
                    msg = MIMEMultipart()
                    msg['From'] = smtp_email
                    msg['To'] = email
                    msg['Subject'] = subject
                    message_body = f'Your OTP is: {otp}'
                    msg.attach(MIMEText(message_body, 'plain'))

                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(smtp_email, smtp_password)
                        server.sendmail(smtp_email, email, msg.as_string())

                        print('OTP sent successfully.')
                        return jsonify({"message": "OTP sent successfully."})
                else:
                    print("wrong Email")
                    return jsonify({"message": "wrong Email."}), 400
        else:
            print("No clients found in the database.")
            return jsonify({"message": "No clients found in the database."}), 400
    except Exception as e:
        print(f'Email sending failed: {str(e)}')
        return jsonify({"error": "Failed to send OTP"}), 500


if __name__ == '__main__':
    app.run("localhost", 9000)
