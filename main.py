from http.client import BAD_REQUEST, FORBIDDEN, INTERNAL_SERVER_ERROR, METHOD_NOT_ALLOWED, UNAUTHORIZED
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import create_table_news, create_table_users, get_db
import news_model
import users_models
from flask_httpauth import HTTPBasicAuth
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()
bcrypt = Bcrypt(app)

@auth.verify_password
def authenticate(username, password):
    try:
        if username and password:
            db = get_db()
            cursor = db.cursor()
            query = "SELECT password FROM tbl_users WHERE username = ?"
            cursor.execute(query, [username])
            hash = cursor.fetchone()
            if len(hash) == 1:
                pwd = bytes(str(hash[0]), 'utf-8')
                check = bcrypt.check_password_hash(pwd, password)
                return check
            else:
                print('salah login')
                return False
        else:
            print('belum di isi')
            return False
    except:
        print('koreksi kode')
        return False

@app.route('/api/v1/news', methods=['GET'])
@auth.login_required
def get_news():
    if 'admin' in auth.current_user():
        result = news_model.get_news()
        data = {
                
                'status': 200,
                'data': result
            
            }
        
        resp = jsonify(data)
        resp.status_code = 200
        
        return resp
    else:
        result = news_model.get_news_user()
        data = {
                
                'status': 200,
                'data': result
                
            }
            
        resp = jsonify(data)
        resp.status_code = 200
            
        return resp

@app.route('/api/v1/news/<news_id>', methods=['GET'])
@auth.login_required
def get_news_by_id(news_id):
    try:
        if 'admin' in auth.current_user():
            result = news_model.get_news_by_id(news_id)
            data = {
                    
                    'status': 200,
                    'data': result
                
                }
            
            resp = jsonify(data)
            resp.status_code = 200
            
            return resp
        else:
            result = news_model.get_news_by_id_user(news_id)
            data = {
                        
                    'status': 200,
                    'data': result
                    
                }
                
            resp = jsonify(data)
            resp.status_code = 200
                
            return resp

    except TypeError:
        data = {
                
                'status': 404,
                'message': "Data Not Found"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 404
        
        return resp
    except:
        data = {
                
                'status': 400,
                'message': "Bad Request"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 400
        
        return resp

@app.route('/api/v1/news/<news_id>', methods=['PUT'])
@auth.login_required
def update_news(news_id):
    try:
        news_detail = request.json
        news_id = news_detail['news_id']
        title = news_detail['title']
        content = news_detail['content']
        flag = news_detail['flag']
        
        if 'admin' in auth.current_user():
            result = news_model.update_news(news_id, title, content, flag)
            if result == True:
                data = {
                        
                    'status': 200,
                    'message': 'Success!'
                        
                    }
                    
                resp = jsonify(data)
                resp.status_code = 200
                    
                return resp
            else:
                data = {
                            
                    'status': 404,
                    'message': "Data Not found"
                        
                    }
                    
                resp = jsonify(data)
                resp.status_code = 404
                    
                return resp
        else:
            data = {
                
                'status': 401,
                'message': "Unauthorized Access"
            
            }
        
            resp = jsonify(data)
            resp.status_code = 401
            
            return resp
    except:
        data = {
                
                'status': 400,
                'message': "Bad Request"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 400
        
        return resp

@app.route('/api/v1/news/<news_id>', methods=['PATCH'])
@auth.login_required
def patch_news(news_id):
    try:
        news_detail = request.json
        news_id = news_detail['news_id']
        flag = news_detail['flag']
        if 'admin' in auth.current_user():
            result = news_model.patch_news(news_id, flag)
            if result == True:
                data = {
                    
                        'status': 200,
                        'message': 'Success!'
                    
                    }
                
                resp = jsonify(data)
                resp.status_code = 200
                
                return resp
        
            else:
                data = {
                            
                    'status': 403,
                    'message': "flag is wrong"
                        
                    }
                    
                resp = jsonify(data)
                resp.status_code = 403
                    
                return resp
        else:
            data = {
                
                'status': 401,
                'message': "Unauthorized Access"
            
            }
        
            resp = jsonify(data)
            resp.status_code = 401
            
            return resp
    except:
        data = {
                
                'status': 400,
                'message': "Bad Request"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 400
        
        return resp

@app.route('/api/v1/news', methods=['POST'])
@auth.login_required
def insert_news():
    try:
        if 'admin' in auth.current_user():
            news_detail = request.json
            title = news_detail['title']
            content = news_detail['content']
            flag = news_detail['flag']
            result = news_model.insert_news(title, content, flag)
            if result == True:
                data = {
                    
                        'status': 201,
                        'message': 'Success!'
                    
                    }
                
                resp = jsonify(data)
                resp.status_code = 201
                
                return resp
            else:
                data = {
                        
                        'status': 403,
                        'message': "title is taken or flag is wrong"
                    
                    }
                
                resp = jsonify(data)
                resp.status_code = 403
                
                return resp
            
        else:
            data = {
                
                'status': 401,
                'message': "Unauthorized Access"
            
            }
        
            resp = jsonify(data)
            resp.status_code = 401
            
            return resp
    except:
        data = {
                
                'status': 400,
                'message': "Bad Request"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 400
        
        return resp

@app.route('/api/v1/news/<news_id>', methods=['DELETE'])
@auth.login_required
def delete_news(news_id):
    try:
        if 'admin' in auth.current_user():
            result = news_model.delete_news(news_id)
            data = {
                        
                    'status': 200,
                    'message': "Success for Delete"
                    
                }
                
            resp = jsonify(data)
            resp.status_code = 200
                
            return resp
        else:
            data = {
                    
                'status': 403,
                'message': "Forbidden Access"
                
            }
            
            resp = jsonify(data)
            resp.status_code = 403
                
            return resp
    except:
        data = {
                
                'status': 404,
                'message': "Data Not Found"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 404
        
        return resp

@app.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    if 'admin' in auth.current_user():
        result = users_models.get_users()
        data = {
                
                'status': 200,
                'data': result
            
            }
        
        resp = jsonify(data)
        resp.status_code = 200
        
        return resp
    else:
        data = {
                
                'status': 401,
                'message': "Unauthorized Access"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 401
        
        return resp

@app.route('/users/<id>', methods=['GET'])
@auth.login_required
def get_users_by_id(id):
    try:
        if 'admin' in auth.current_user():
            result = users_models.get_users_by_id(id)
            data = {
                    
                    'status': 200,
                    'data': result
                
                }
            
            resp = jsonify(data)
            resp.status_code = 200
            
            return resp
        else:
            data = {
                
                'status': 401,
                'message': "Unauthorized Access"
            
            }
        
            resp = jsonify(data)
            resp.status_code = 401
            
            return resp
    except TypeError:
        data = {
                
                'status': 404,
                'message': "Data Not Found"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 404
        
        return resp
    except:
        data = {
                
                'status': 400,
                'message': "Bad Request"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 400
        
        return resp

@app.route('/users', methods=['POST'])
@auth.login_required
def insert_users():
    try:
        users_details = request.json
        username = users_details['username']
        password = users_details['password']
        result = users_models.insert_users(username, password)
        data = {
                    
            'status': 201,
            'message': 'Success!'
                    
            }
                
        resp = jsonify(data)
        resp.status_code = 201
                
        return resp
        
    except TypeError:
        data = {
                
                'status': 400,
                'message': "Bad Request"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 400
        
        return resp
    except ValueError:
        data = {
                
                'status': 403,
                'message': "username is taken"
            
            }
        resp = jsonify(data)
        resp.status_code = 403
        
        return resp

@app.route('/users/<id>', methods=['PUT'])
@auth.login_required
def update_users(id):
    try:
        if 'admin' in auth.current_user():
            users_details = request.json
            id = users_details['id']
            username = users_details['username']
            password = users_details['password']
            result = users_models.update_users(id, username, password)
            data = {
                    
                    'status': 200,
                    'message': 'Success!'
                    
                }
                
            resp = jsonify(data)
            resp.status_code = 200
                
            return resp
        else:
            data = {
                
                'status': 401,
                'message': "Unauthorized Access"
            
            }
        
            resp = jsonify(data)
            resp.status_code = 401
            
            return resp
        
    except TypeError:
        data = {
                
                'status': 400,
                'message': "Bad Request"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 400
        
        return resp
    except ValueError:
        data = {
                
                'status': 403,
                'message': "username is taken"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 403
        
        return resp

@app.route('/users/<id>', methods=['DELETE'])
@auth.login_required
def delete_users(id):
    try:
        if 'admin' in auth.current_user():
            result = users_models.delete_users(id)
            data = {
                    
                    'status': 200,
                    'message': "Success for Delete"
                
                }
            
            resp = jsonify(data)
            resp.status_code = 200
            
            return resp
        else:
            data = {
                
                'status': 401,
                'message': "Unauthorized Access"
            
            }
        
            resp = jsonify(data)
            resp.status_code = 401
            
            return resp
    except:
        data = {
                
                'status': 404,
                'message': "Data Not Found"
            
            }
        
        resp = jsonify(data)
        resp.status_code = 404
        
        return resp

@app.errorhandler(403)
def forbidden(error=FORBIDDEN):
    message = {
        
            'status': 403,
            'message': 'Forbidden Access'
        }
    
    resp = jsonify(message)
    resp.status_code = 403
    
    return resp

@app.errorhandler(405)
def methodnotallowed(error=METHOD_NOT_ALLOWED):
    message = {
        
            'status': 405,
            'message': 'method not allowed'
        }
    
    resp = jsonify(message)
    resp.status_code = 405
    
    return resp

@app.errorhandler(500)
def internalserver(error=INTERNAL_SERVER_ERROR):
    message = {
        
            'status': 500,
            'message': 'internal server error'
        }
    
    resp = jsonify(message)
    resp.status_code = 500
    
    return resp

@app.errorhandler(400)
def badrequest(error=BAD_REQUEST):
    message = {
        
            'status': 400,
            'message': 'Bad Request'
        }
    
    resp = jsonify(message)
    resp.status_code = 400
    
    return resp

@app.errorhandler(401)
def unauthorized(error=UNAUTHORIZED):
    message = {
        
            'status': 401,
            'message': 'Unauthorized Login'
        }
    
    resp = jsonify(message)
    resp.status_code = 401
    
    return resp

if __name__ == "__main__":
    create_table_news()
    create_table_users()
    app.run(debug=True)