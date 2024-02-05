from flask_app import app

# import our controllers
from flask_app.controllers import users, shows

if __name__=="__main__":   
    app.run(debug=True)   