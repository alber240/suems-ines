from flask import Flask
from routes.auth import auth
from routes.events import events

app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(events)

@app.route('/api/ping')
def ping():
    return {"message": "SUEMS backend is alive!"}

if __name__ == '__main__':
    app.run(debug=True)
