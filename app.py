from flask import Flask
from routes.auth import auth
from routes.tasks import task

app = Flask(__name__)

# Change this to any random secret string
app.secret_key = "theone"

app.register_blueprint(auth)
app.register_blueprint(task)

if __name__ == "__main__":
    app.run(debug=True)