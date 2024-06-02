import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate(
    "C:\\Users\\vitht\\PycharmProjects\\pythonProject4\\firebase_db_connection\\test-71f04-firebase-adminsdk-70vbu-7a05af999c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-71f04-default-rtdb.firebaseio.com//'
})

# Global variable to store the key of the first entry
entry_key = None


@app.route('/bulb', methods=['POST'])
def fan_information():
    global entry_key

    try:
        data = request.get_json()
        print("data: ", data)

        required_fields = ['switch', 'mode']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing {field}"}), 400

        switch = data['switch']
        mode = data['mode']

        # Validating switch value
        if switch not in ['On', 'Off']:
            return jsonify({"error": "Invalid switch value. Valid values are 'On' or 'Off'"}), 400

        # Validating mode value
        if mode not in ['Low Power', 'Mid Power', 'High Power']:
            return jsonify({"error": "Invalid mode value. Valid values are 'Low Power' or 'High Power'"}), 400

        timestamp = datetime.now()

        ref = db.reference('bulb_data')

        if entry_key is None:
            # Insert the first entry and store its key
            new_client_ref = ref.push()
            entry_key = new_client_ref.key
            new_client_ref.set({
                'Switch': switch,
                'Mode': mode,
                'On Time': timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })
            print(f"First bulb information added successfully, 'timestamp': {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            return jsonify({"message": "First bulb information added successfully",
                            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")})
        else:
            # Update the existing entry
            ref.child(entry_key).update({
                'Switch': switch,
                'Mode': mode,
                'On Time': timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })
            print(f"Bulb information updated successfully, 'timestamp': {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            return jsonify({"message": "Bulb information updated successfully",
                            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run("localhost", 10000)
