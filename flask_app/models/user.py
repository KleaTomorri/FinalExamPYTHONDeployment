from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db_name = "final_schema"
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM users where email = %(email)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def get_user_by_id(cls, data):
        query = 'SELECT * FROM users where id = %(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
        
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (firstName, lastName, email, password) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_userRegister(data):
        is_valid = True
        if len(data['firstName']) < 2:
            flash("First name must be at least 2 characters long", 'nameRegister')
            is_valid = False
        if len(data['lastName']) < 2:
            flash("Last name must be at least 2 characters long", 'lastNameRegister')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address", 'emailRegister')
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters long", 'passwordRegister')
            is_valid = False
        
        return is_valid

    @staticmethod
    def validate_user(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address", 'emailLogin')
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters long", 'passwordLogin')
            is_valid = False
        return is_valid

    
