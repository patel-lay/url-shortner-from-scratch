from flask import Flask, request, jsonify
from flask_cors import CORS

from hash_function import hashFunction 
from backend_server import backendServer as backend

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from any domain

@app.route("/api", methods=["POST"])
def receive_data():
    try:
        data = request.get_json()
        if(data is None):    
            return jsonify({"message": "URl parsed successfully", "longURL": long_url, "shortURL":short_url}), 200
        long_url = data["long_url"]
        hash = hashFunction()
        print("Received data:", long_url)
        hash.set_long_url(long_url)
        hash.create_hash(long_url)
        short_url = hash.get_short_url()
        # print("Received data:", long_url)
        # print("Shortened url:", short_url)
       # backend.send_url(short_url, long_url)

        return jsonify({"message": "URl parsed successfully", "longURL": long_url, "shortURL":short_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
