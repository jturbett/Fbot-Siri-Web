from flask import Flask, request
import subprocess
import os

app = Flask(__name__)
# This creates the directory on the server that triggers the flask app to run the script when a 
# POST is made to the url, and I set up a siri shortcut to make this work http://22.22.22.22/webhook  
# The  repeated with a bunch more directorys and python scripts
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'motion.py')
        subprocess.run(["python3", script_path])
        return 'Script executed', 200
    else:
        return 'Invalid request', 400

@app.route('/wateritall', methods=['POST'])
def wateritall():
    if request.method == 'POST':
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'water', 'wateritall.py')
        subprocess.run(["python3", script_path])
        return 'Water it all script executed', 200
    else:
        return 'Invalid request', 400

@app.route('/irrigation', methods=['POST'])
def irrigation():
    if request.method == 'POST':
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'irrigation.py')
        subprocess.run(["python3", script_path])
        return 'Irrigation script executed', 200
    else:
        return 'Invalid request', 400

if __name__ == '__main__':
    app.run(debug=True)
