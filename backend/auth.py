import jwt
import os #for .env
from flask import Flask,request,jsonify
from functools import wraps    #Keeps original function info


SECRET_KEY=os.getenv("SECRET_KEY")

def error_response(message,status_code):
    return jsonify({"error":message}),status_code

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):       #args-handles id #kwargs-handles named values(?status_code=completed)
        auth_header=request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return error_response("Unauthorized",401)
            
        try:
            token=auth_header.split(" ") [1]
            user=jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
        except Exception:
            return error_response("Invalid or expired token",401)
        return f(user, *args, **kwargs)
    return decorated   