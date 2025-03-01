from flask import Flask, request, jsonify
from flask_cors import CORS

from hash_function import hashFunction 
from backend_server import backendServer

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from any domain
# def create_app():
#     app = Flask(__name__)
#     app.add_url_rule("/api", set_short_url, methods=["POST"])  # Register the function
#     app.add_url_rule("/api", get_url, methods=["GET"])  # Register the function


#     return app

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
        message =  "Short URL saved successfully"
        return jsonify({"message": message, "long_url": long_url, "short_url":short_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api", methods=["GET"])
def get_url():
    try:
        data = request.get_json()
        if(data is None):    
            return jsonify({"message": "URl parsed unsuccessfully"}), 200
        short_url = data["short_url"]
        if not short_url.startswith("https://tinyurl.com/"):
            return jsonify({"message": "short url type incorrect"}), 200

        backend = backendServer()
        long_url = backend.get_url(short_url)
        backend.response = "" #reset response

        return jsonify({"message": "URl parsed successfully", "long_url": long_url, "short_url":short_url}), 302
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    # app = create_app()
    # app.app_context().push()
    app.run(host='0.0.0.0', port=4000, debug=True)
