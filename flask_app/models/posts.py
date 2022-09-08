from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app 
from datetime import date, datetime
from flask import flash


class Post:
    def __init__(self, posts_id, posts_content, created_at, user_id):
        self.posts_id = posts_id
        self.posts_content = posts_content
        self.created_at = created_at
        self.user_id = user_id

    @classmethod
    def send_post(cls, data):
        query = "INSERT INTO posts (posts_content, user_id, post_likes, created_at, updated_at) VALUES ( %(posts_content)s, %(user_id)s, 0, SYSDATE(), SYSDATE());"
        data2 = {
            "posts_content" : data[0],
            "user_id" : data[1],
        }
        result = connectToMySQL('project_app').query_db( query, data2 )
        return result

    @classmethod
    def update_post(cls, data):
        query = "UPDATE posts SET posts_content = %(posts_content)s WHERE posts_id = %(post_id)s;"
        data = {
            "posts_content" : data[0],
            "user_id" : data[1],
            "post_id" : data[2]
        }
        result = connectToMySQL('project_app').query_db( query, data )
        return result

    @classmethod 
    def get_all_posts(cls):
        query = "SELECT posts.posts_content, users.first_name, users.last_name, posts.user_id, posts.posts_id, users.users_id, posts.post_likes, posts.created_at FROM users LEFT JOIN posts ON users.users_id = posts.user_id WHERE posts_id > 0 ORDER BY post_likes DESC;"
        result = connectToMySQL('project_app').query_db( query )
        return result

    @classmethod
    def get_post_from_one_user(cls, id):
        data = {
            "id" : id
        }
        query = "SELECT * FROM users LEFT JOIN posts on users.users_id = posts.user_id WHERE users_id = %(id)s;"
        result = connectToMySQL('project_app').query_db( query, data )
        return result

    @classmethod
    def get_single_post(cls, id):
        data = {
            "id" : id
        }
        query = "SELECT * FROM users LEFT JOIN posts on users.users_id = posts.user_id LEFT JOIN likes ON users.users_id = likes.user_id WHERE posts_id = %(id)s;"
        result = connectToMySQL('project_app').query_db( query, data )
        return result

    @classmethod
    def delete_post(cls, id ):
        data = {
            "id" : id
        }
        query = "DELETE FROM likes WHERE post_id = %(id)s;"
        result1 = connectToMySQL('project_app').query_db( query, data )
        query = "DELETE FROM posts WHERE posts_id = %(id)s;"
        result = connectToMySQL('project_app').query_db( query, data )
        return result , result1

    @staticmethod
    def validate_post(data):
        isValid = True
        query = "SELECT * FROM post WHERE user_id = %(user_id)s;"
        data2 = {
            "posts_content" : data[0],
            "user_id" : data[1],
        }

        results = connectToMySQL('project_app').query_db( query, data2 )
        print("VALIDAR POST: ", results)
        if len( data[0] ) < 1:
            flash( "Su post tiene que ser al menos de 1 caracter", 'post' )
            isValid = False 
        return isValid
