from flask import Blueprint, request, jsonify
from db import get_conn
from auth import token_required, error_response

task_routes = Blueprint('task_routes', __name__)

@task_routes .route('/tasks', methods=['POST'])
@token_required
def add(user):
        
    data=request.json
    title=data.get("title")
    status=data.get("status")
    
    if not title or not status:
        return error_response("Title and status required",400)
    username=user["username"]
    
    try:
        c=get_conn()
        cursor=c.cursor()
        cursor.execute('''INSERT INTO tasks (title,status,username) VALUES(%s,%s,%s)''',(title,status,username))
        c.commit()
    except Exception:
        return error_response("Internal server error",500)
    finally:    
        c.close()
    return jsonify({"message": "Task added to DB"}), 201
    
@task_routes .route('/tasks', methods=['GET'])
@token_required
def show(user):
    username=user["username"]
    page=request.args.get("page",1,type=int)
    limit=request.args.get("limit",10,type=int)
    offset=(page-1)*limit
    status=request.args.get("status")
    search=request.args.get("search")
    
    try:
        c=get_conn()
        cursor=c.cursor(dictionary=True)
        if status and search:
            cursor.execute('''SELECT * FROM tasks WHERE username=%s AND status=%s AND title LIKE %s LIMIT %s OFFSET %s '''
                                                ,(username,status,f"%{search}%",limit,offset))
        elif status:
            cursor.execute('''SELECT * FROM tasks WHERE username=%s AND status=%s LIMIT %s OFFSET %s''', (username,status,limit,offset))
        elif search:
            cursor.execute('''SELECT * FROM tasks WHERE username=%s AND title LIKE %s LIMIT %s OFFSET %s '''
                                                ,(username,f"%{search}%",limit,offset))
        
        else:
            cursor.execute('''SELECT * FROM tasks WHERE username=%s LIMIT %s OFFSET %s''', (username,limit,offset))        
            
        row=cursor.fetchall()
    except Exception:
        return error_response("Internal server error",500)
    finally:    
        c.close()
        
    return jsonify(row)
       
@task_routes .route ('/tasks/<int:id>', methods=['GET'])
@token_required
def get_task(user,id):
    username=user["username"]
    
    try:
        c=get_conn()
        cursor=c.cursor(dictionary=True)
        cursor.execute('''SELECT * FROM tasks WHERE id=%s AND username=%s''',(id,username))
        row=cursor.fetchone()
        
    except Exception:
        return error_response("Internal server error",500)
    finally:   
        c.close()
    
    if row:
        return jsonify(row)
   
    return error_response("Task not found in DB",404)
    
@task_routes .route('/tasks/<int:id>', methods=['DELETE'])
@token_required
def delete(user,id):
    username=user["username"]
    
    try:
        c=get_conn()
        cursor=c.cursor()
        cursor.execute('''DELETE FROM tasks WHERE id=%s AND username=%s''',(id,username))    
        c.commit()
    
        if cursor.rowcount ==0:
            return error_response("Task not found",404)
            
        else:
            return jsonify({"message":"Task deleted"}),200
     
    except Exception:
        return error_response("Internal server error",500)
            
    finally:    
         c.close()
    
    
@task_routes .route('/tasks/<int:id>', methods=['PUT'])
@token_required
def update(user,id):

    data = request.json
    title = data.get("title")
    status = data.get("status")
    username=user["username"]
    
    if not title or not status:
        return error_response("Title and status required", 400)
        
    try:    
        c = get_conn()
        cursor = c.cursor()
        cursor.execute("UPDATE tasks SET title=%s, status=%s WHERE id=%s AND username=%s",(title, status,id,username))
        c.commit()

        if cursor.rowcount == 0:
            return error_response("Task not found",404)
    except Exception:
        return error_response("Internal server error",500)  
        
    finally:
        c.close()
    return jsonify({"message": "Task updated"})    
  