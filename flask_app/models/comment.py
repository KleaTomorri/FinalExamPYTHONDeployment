from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Comment:
    db_name = "final_schema"

    @classmethod
    def get_comments_for_show(cls, show_id):
        query = "SELECT commentet.*, users.firstName FROM commentet JOIN users ON commentet.user_id = users.id WHERE commentet.show_id = %(show_id)s ORDER BY commentet.created_at DESC;"
        data = {'show_id': show_id}
        results = connectToMySQL(cls.db_name).query_db(query, data)
        comments = []
        if results:
            for comment in results:
                comments.append(comment)
        return comments

    @classmethod
    def create_comment(cls, data):
        query = "INSERT INTO commentet (comment, user_id, show_id) VALUES (%(comment)s, %(user_id)s, %(show_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_comment(cls, comment_id):
        query = "DELETE FROM commentet WHERE id = %(comment_id)s;"
        data = {'comment_id': comment_id}
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_comments_for_show(cls, show_id):
        query = "SELECT commentet.*, users.firstName FROM commentet JOIN users ON commentet.user_id = users.id WHERE commentet.show_id = %(show_id)s ORDER BY commentet.id DESC;"
        data = {'show_id': show_id}
        results = connectToMySQL(cls.db_name).query_db(query, data)
        comments = []
        if results:
            for comment in results:
                comments.append(comment)
        return comments

    @classmethod
    def get_comment_by_id(cls, comment_id):
        query = "SELECT * FROM commentet WHERE id = %(comment_id)s;"
        data = {'comment_id': comment_id}
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return None