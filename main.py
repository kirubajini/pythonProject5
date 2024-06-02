import subprocess
import sys
import os
from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "API Server Running"


@app.route('/login')
def login():
    # Call the login.py script or implement the login logic here
    return "Login Page"


@app.route('/signup')
def signup():
    # Call the signup.py script or implement the signup logic here
    return "Signup Page"

# Add other routes similarly...


def run_api(script_name):
    python_executable = sys.executable
    return subprocess.Popen([python_executable, script_name])


if __name__ == '__main__':
    processes = []

    base_dir = os.path.dirname(__file__)
    api_scripts = [
        os.path.join(base_dir, 'bulb.py'), os.path.join(base_dir, 'login.py'),
        os.path.join(base_dir, 'signup.py'), os.path.join(base_dir, 'fan.py'),
        os.path.join(base_dir, 'forgot_password.py'), os.path.join(
            base_dir, 'weather.py'),
        os.path.join(base_dir, 'otp.py'), os.path.join(base_dir, 'kiru.py')
    ]

    for script in api_scripts:
        process = run_api(script)
        processes.append(process)

    app.run(host='0.0.0.0', port=8000)

    for process in processes:
        process.wait()
