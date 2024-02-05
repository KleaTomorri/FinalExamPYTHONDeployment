from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
class Show:
    db_name = "final_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.comments = data['comments']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO shows (title, network,  release_date, comments, user_id) VALUES (%(title)s, %(network)s,%(release_date)s, %(comments)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL(cls.db_name).query_db(query)
        shows = []
        if results:
            for show in results:
                shows.append(show)
        return shows
    
    @classmethod
    def get_show_by_id(cls, data):
        query = "SELECT shows.*, users.firstName FROM shows LEFT JOIN users ON shows.user_id = users.id WHERE shows.id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            
            return result[0]
        return False
    

    
    @classmethod
    def get_comment_by_id(cls, data):
        query = "SELECT * FROM commentet where commentet.id = %(id)s;"
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM shows where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_all_recipe_comments(cls, data):
        query ="DELETE FROM commentet where commentet.shows_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
   
    @classmethod
    def update(cls, data):
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, comments = %(comments)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    
    
 # functionality for comments
   

   
   
   
   
   
   #validimet
    @staticmethod
    def validate_shows(show):
        is_valid = True
        if len(show['title'])< 3:
            flash('Title should be more  or equal to 2 characters', 'name')
            is_valid = False
        if len(show['comments'])< 3:
            flash('Comments should be more  or equal to 3 characters', 'description')
            is_valid = False
        return is_valid
    
    
  