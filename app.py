from flask import Flask, jsonify
import threading
from prescription_automation import main  # Assuming the main function is in the same directory

app = Flask(__name__)

@app.route('/run-script', methods=['GET'])
def run_script():
    thread = threading.Thread(target=main)
    thread.start()
    return jsonify({'status': 'Script started'}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
