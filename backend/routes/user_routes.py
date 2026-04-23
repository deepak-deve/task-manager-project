from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import datetime
from db import get_conn
from auth import SECRET_KEY, error_response


user_routes=Blueprint('user_routes',__name__)

@user_routes.route('/register', methods=['POST'])
def register():
    data=request.json
    username=data.get("username")
    password=data.get("password")
   
    if not username or not password:
        return error_response("username and password required",400)
    
    if len(password) <4:
        return error_response("password at least 4 characters",400)    
       
    hashed=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
   
    c=get_conn()
    cursor=c.cursor()
    cursor.execute('''INSERT INTO users (username,password) VALUES (%s,%s)''',(username,hashed))
   
    c.commit()
    c.close()
    return jsonify({"message": "User registered", "username": username}), 201
   
@user_routes.route('/login', methods=['POST'])
def login():
    data=request.json
    username=data.get("username")
    password=data.get("password")
    
    if not username or not password:
        return error_response("username and password required",400)
    
    c=get_conn()
    cursor=c.cursor()
    
    cursor.execute('''SELECT password FROM users WHERE username=%s''',(username,))
    row=cursor.fetchone()
    c.close()
    
    if row is None:
        return error_response("user name not found",404)
            
    spw=row[0]

    if bcrypt.checkpw(password.encode(), spw.encode()): 

        token=jwt.encode({
            "username":username,
            "exp":datetime.datetime.utcnow()+datetime.timedelta(hours=1)
               },SECRET_KEY,algorithm="HS256")
                           
        return jsonify({"message": "Login successful", "token":token})

    else:
        return error_response("Wrong credentials",401)
   