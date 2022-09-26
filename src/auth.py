from flask import Blueprint,request, jsonify
import validators
from database import User,db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import jwt_required,create_access_token,create_refresh_token,get_jwt_identity
from flasgger import swag_from

auth=Blueprint("auth",__name__,url_prefix="/api/v1/auth")

@swag_from('./docs/auth/register.yaml')
@auth.post('/register')
def register():
    username=request.json['username']
    email=request.json['email']
    password=request.json['password']

    if len(password)<6:
        return jsonify({'error':'password is too short'})
    if len(username)<3:
        return jsonify({'error':'username is too short'})
    if not username.isalnum() or " " in username:
        return jsonify({'error':'username should be alphanumeric & not include spaces'})
    if not validators.email(email):
        return jsonify({'error':'email is not valid'})
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error':'username already taken'})
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error':'email already taken'})


    pwd_hash=generate_password_hash(password)
    user=User(username=username,password=pwd_hash,email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify(
        {
            'message':'user is created',
            'user':{'username':username,'email':email}
        }
    )
@swag_from('./docs/auth/login.yaml')    
@auth.post('/login')
def login():
    email=request.json.get('email')
    password=request.json.get('password')
    user=User.query.filter_by(email=email).first()
    
    if user:
        check_password=check_password_hash(user.password,password)
        if check_password:
            refresh=create_refresh_token(identity=user.id)
            access=create_access_token(identity=user.id)
            return jsonify({
                'user':{
                    'refresh':refresh,
                    'access':access,
                    'username':user.username,
                    'email':user.email
                }
            }

            )

    return jsonify({'error':'your creadential is not valid'})


@auth.get('/<int:id>')
@jwt_required()
def get_user(id):
    user=User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'error':'item not found'})
    return jsonify({
        
        'username':user.username,
        'email':user.email
    })    


@auth.put('/update/<int:id>')
@jwt_required()
def update_user(id):
    
    
    user=User.query.get(id)
    username=request.json['username']
    email=request.json['email']
    password=request.json['password']
    pwd_hash=generate_password_hash(password)
    user.username=username
    user.email=email
    user.password=pwd_hash

    db.session.commit()
    return jsonify(
        {
            'message':'user is created',
            'user':{'username':username,'email':email}
        }
    ) 

@auth.delete('/delete/<int:id>')
def delete_user(id):
    user=User.query.filter_by(id=id).first()
    if not user:
        return jsonify({"error":"item not found"})
    db.session.delete(user)
    db.session.commit()
    return jsonify({})    
