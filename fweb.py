#Flask code to be hosted by Apache
from flask import Flask, request
import json
import subprocess

app = Flask(__name__)

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Run the local Python script
        result = subprocess.run(["/usr/bin/python3", "/home/fbot/motion1.py"], capture_output=True, text=True)

        # Check if the script ran successfully
        if result.returncode == 0:
            print("Script executed successfully")
            response = {'success': True, 'output': result.stdout}
        else:
            print("Script execution failed")
            response = {'success': False, 'error': result.stderr}

        return json.dumps(response), 200, {'ContentType': 'application/json'}
    except Exception as e:
        print(f"Error running script: {e}")
        return json.dumps({'success': False, 'error': str(e)}), 500, {'ContentType': 'application/json'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
