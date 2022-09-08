from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app 
from datetime import date, datetime


class Like:
    def __init__(self, likes_id, user_id, post_id, likes, created_at, updated_at):
        self.likes_id = likes_id
        self.user_id = user_id
        self.post_id = post_id
        self.likes = likes
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def add_likes( cls, data ):
        query = "INSERT INTO likes (user_id, post_id, likes, created_at, updated_at) VALUES ( %(user_id)s, %(post_id)s, %(likes)s, SYSDATE(), SYSDATE());"
        data2 = {
            "user_id" : data[1],
            "post_id" : data[2],
            "likes" : data[0]
        }
        result = connectToMySQL('project_app').query_db( query, data2 )
        
        query = "UPDATE posts SET post_likes = post_likes +1 WHERE posts_id = %(post_id)s;"
        data3 = {
            "user_id" : data[1],
            "post_id" : data[2],
            "post_likes" : data[0]
        }
        result = connectToMySQL('project_app').query_db( query, data3 )
        print("RESULTS ENVIADO LIKE DB: ", result)
        return result

    @classmethod
    def users_who_liked(cls, id):
        query = "SELECT DISTINCT likes.user_id, likes.post_id, users.first_name, users.last_name, users.users_id from likes left join posts on posts.posts_id = likes.post_id left join users on users.users_id = likes.user_id where post_id = %(id)s AND posts_id = %(id)s AND users.users_id = likes.user_id;"
        data = {
            "id" : id
        }
        result = connectToMySQL('project_app').query_db( query, data )
        print("RESULTS LISTA LIKES: ", result)
        return result 