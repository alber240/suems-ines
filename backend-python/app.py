from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/ping')
def ping():
    return jsonify({"message": "SUEMS backend is alive!"})

if __name__ == '__main__':
    app.run(debug=True)
