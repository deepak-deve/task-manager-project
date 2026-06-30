from flask import Flask, jsonify
from flask_cors import CORS
from routes.user_routes import user_routes
from routes.task_routes import task_routes
from dotenv import load_dotenv
import os

load_dotenv()
app=Flask(__name__)
CORS(app)

         
app.register_blueprint(user_routes)  #Built-in Flask function 
app.register_blueprint(task_routes)


     
    


@app.route('/')
def home():
    return jsonify({"message":"WELCOME TO TASK MANAGER!"})
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


