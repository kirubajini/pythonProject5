import subprocess
import sys
import os


def run_api(script_name):
    python_executable = sys.executable
    return subprocess.Popen([python_executable, script_name])


if __name__ == '__main__':
    processes = []

    base_dir = os.path.dirname(__file__)
    api_scripts = [os.path.join(base_dir, 'bulb.py'), os.path.join(base_dir, 'login.py'), os.path.join(base_dir, 'signup.py'),
                   os.path.join(base_dir, 'fan.py'), os.path.join(base_dir, 'forgot_password.py'), os.path.join(base_dir, 'weather.py'),
                   os.path.join(base_dir, 'otp.py'), os.path.join(base_dir, 'kiru.py')]

    for script in api_scripts:
        process = run_api(script)
        processes.append(process)

    for process in processes:
        process.wait()
