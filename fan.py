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

switch_state = 'On'
previous_mode = None
previous_switch = None


@app.route('/fan', methods=['POST'])
def fan_information():
    global switch_state, previous_mode, previous_switch

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

        ref = db.reference('fan_data')
        fan = ref.get()

        if fan:
            if previous_switch == switch and previous_mode == mode:
                print(f"Fan with switch {switch}, {mode} already exists")
                return jsonify({"error": f"Fan with switch {switch}, {mode} already exists"}), 400

            if previous_switch == "Off" and switch == "Off":
                print("Cannot proceed. Fan is currently switched Off.")
                return jsonify({"error": "Cannot proceed. Fan is currently switched Off."}), 400

        previous_mode = mode
        previous_switch = switch

        new_client_ref = ref.push()
        new_client_ref.set({
            'Switch': switch,
            'Mode': mode,
            'On Time': timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })

        print(f"Fan information added successfully, 'timestamp': {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        return jsonify({"message": "Fan information added successfully", "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run("localhost", 11000)
