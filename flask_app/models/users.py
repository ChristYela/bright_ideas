from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app 
from datetime import date, datetime
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PWD_REGEX = re.compile("^(?=.*?[A-Z])(?=(.*[a-z]){1,})(?=(.*[\d]){1,})(?=(.*[\W]){1,})(?!.*\s).{8,}$")

class User:
    def __init__(self, users_id, first_name, last_name, email, users_password, created_at):
        self.users_id = users_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.users_password = users_password
        self.created_at = created_at

    @classmethod
    def user_Registration(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, users_password, created_at, updated_at) VALUES ( %(first_name)s , %(last_name)s , %(email)s, %(encryptedpassword)s, SYSDATE(), SYSDATE());"
        data2 = {
            "first_name" : data[0],
            "last_name" : data[1],
            "email" : data[2],
            "users_password" : data[3],
            "encryptedpassword" : data[4],
            "confirm_users_password" : data[5]
        }
        result = connectToMySQL('project_app').query_db( query, data2 )
        return result

    @classmethod
    def user_login(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data2 = {
            "email" : data[0],
            "users_password" : data[1],
        }
        result = connectToMySQL('project_app').query_db( query, data2 )
        return result

    @classmethod
    def get_userInformationBy_id( cls, data ):
        query = "SELECT * FROM users WHERE users_id = %(id)s;"
        results = connectToMySQL('project_app').query_db( query, data )
        user = []
        for n in results:
            user.append( User( n['users_id'], n['first_name'], n['last_name'], n['email'], n['users_password'], n['created_at'] ) )
        return user

    @classmethod 
    def get_all_users( cls, data ):
        query = "SELECT * FROM users WHERE users_id != %(users_id)s ORDER BY first_name;"
        results = connectToMySQL('project_app').query_db(query,data)
        users = []
        for n in results:
            users.append( User( n['users_id'], n['first_name'], n['last_name'], n['email'], n['users_password'], n['created_at'] ) )
        return users

    @classmethod
    def delete_user_account(cls, id):
        data = {
            "id" : id
        }
        query = "DELETE FROM posts WHERE user_id = %(id)s;"
        result = connectToMySQL('project_app').query_db( query, data )
        query = "DELETE FROM likes WHERE user_id = %(id)s;"
        result1 = connectToMySQL('project_app').query_db( query, data )
        query = "DELETE FROM users WHERE users_id = %(id)s;"
        result2 = connectToMySQL('project_app').query_db( query, data )
        return result, result1, result2

    @classmethod
    def get_user_to_validate( cls, username ):
        query = "SELECT * FROM users WHERE username=%(username)s;"
        data = {
            "username" : username
        }
        result = connectToMySQL( "project_app" ).query_db( query, data )
        return result

    @staticmethod
    def validate_login(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']): 
            flash("Dirección de correo electrónico no valida!", 'login')
            is_valid = False            
        if not PWD_REGEX.match(data['users_password']):
            flash("Password debe cumplir con los requisitos", 'login')
            is_valid = False    
        if len(data['users_password']) < 8:
            flash("Password debe ser al menos de 8 caracteres", 'login')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_registration(data):
        isValid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data2 = {
            "first_name" : data[0],
            "last_name" : data[1],
            "email" : data[2],
            "users_password" : data[3],
            "encryptedpassword" : data[4],
            "confirm_users_password" : data[5]
        }
        results = connectToMySQL('project_app').query_db( query, data2 )
        if len(results) >= 1:
            flash("El Email ya está registrado", 'register')
            isValid = False
        if len( data[0] ) < 3:
            flash( "El Nombre debe ser al menos de 3 caracteres", 'register' )
            isValid = False 
        if len( data[1] ) < 3:
            flash( "El Apellido debe ser al menos de 3 caracteres", 'register' )
            isValid = False
        if not EMAIL_REGEX.match(data[2]):
            flash("La dirección de email debe ser un formato válido", 'register')
            isValid = False            
        if not PWD_REGEX.match(data[3]):
            flash("El Password debe tener un formato válido", 'register')
            isValid = False
        if len(data[3]) < 8:
            flash("El Password debe ser al menos 8 caracteres ", 'register')
            isValid = False
        if data[3] != data[5]:
            flash("Los Passwords deben coincidir", 'register')
            isValid = False
        return isValid
