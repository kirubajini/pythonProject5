import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for your app

# Firebase setup
cred = credentials.Certificate(
    "C:\\Users\\vitht\\PycharmProjects\\pythonProject4\\firebase_db_connection\\test-71f04-firebase-adminsdk-70vbu-7a05af999c.json"
)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-71f04-default-rtdb.firebaseio.com//'
})

# SMTP configuration
smtp_email = 'viththiarul67@gmail.com'
smtp_password = 'CWURrjTgOcF29V7h'
smtp_server = 'smtp-relay.brevo.com'
smtp_port = 587

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    if "email" not in data or "otp" not in data:
        return jsonify({"error": "Missing email or OTP"}), 400

    email = data['email']
    otp = data['otp']

    ref = db.reference('client')
    clients = ref.get()
    for client_id, client_data in clients.items():
        if client_data['email'] == email:
            if 'otp' in client_data and client_data['otp'] == otp:
                try:
                    # Simulate sending SMS for OTP verification success
                    phone_number = client_data.get('phone', 'default@sms.gateway')  # Replace with actual phone number field
                    sms_message = MIMEMultipart()
                    sms_message['From'] = smtp_email
                    sms_message['To'] = phone_number
                    sms_message['Subject'] = 'OTP Verification'
                    sms_body = 'OTP verification successful.'
                    sms_message.attach(MIMEText(sms_body, 'plain'))

                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(smtp_email, smtp_password)
                        server.sendmail(smtp_email, phone_number, sms_message.as_string())

                    return jsonify({"message": "OTP verified successfully. SMS sent."})
                except Exception as e:
                    return jsonify({"error": f"OTP verified but failed to send SMS: {str(e)}"}), 500
            else:
                return jsonify({"error": "Invalid OTP"}), 400
    return jsonify({"error": "Email not found"}), 404

if __name__ == '__main__':
    app.run("localhost", 2000)
