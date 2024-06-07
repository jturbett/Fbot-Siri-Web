from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

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
