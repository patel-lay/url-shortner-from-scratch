from flask import Flask, request, jsonify
from flask_cors import CORS

from hash_function import hashFunction 
from backend_server import backendServer

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from any domain

@app.route("/api", methods=["POST"])
def set_short_url():
    try:
        data = request.get_json()
        if(data is None):    
            return jsonify({"message": "URl parsing unsuccessfully"}), 200
        long_url = data["long_url"] #get the long url
        hash = hashFunction()
        backend = backendServer()
        hash.set_long_url(long_url) #hash it to get short url
        hash.create_hash(long_url)
        short_url = hash.get_short_url()
        backend.send_url(short_url, long_url) #save short_url, long_url in redis database

        return jsonify({"message": "URl parsed successfully", "longURL": long_url, "shortURL":short_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api", methods=["GET"])
def get_url():
    try:
        data = request.get_json()
        if(data is None):    
            return jsonify({"message": "URl parsed unsuccessfully"}), 200
        short_url = data["short_url"]
        backend = backendServer()
        long_url = backend.get_url(short_url)
        print(long_url)

        return jsonify({"message": "URl parsed successfully", "longURL": long_url, "shortURL":short_url}), 302
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
