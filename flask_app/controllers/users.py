from flask_app import app
from flask import render_template, redirect, flash, session, request
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/shows')
    return redirect('/login')

@app.route('/register')
def registerPage():
    if 'user_id' in session:
        return redirect('/shows')
    return render_template('login_registration.html')

@app.route('/register', methods=['POST'])
def register():
    if 'user_id' in session:
        return redirect('/')
    
    form_data = request.form
    if not User.validate_userRegister(form_data):
        return redirect(request.referrer)
    
    user = User.get_user_by_email({'email': form_data['email']})
    if user:
        flash('An account with this email already exists', 'emailRegister')
        return redirect(request.referrer)
    
    data = {
        'firstName': form_data['firstName'],
        'lastName': form_data['lastName'],
        'email': form_data['email'],
        'password': form_data['password']
    }
    
    # Hash the password before saving it
    data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    # Create the user
    user_id = User.create(data)
    
    if user_id:
        session['user_id'] = user_id
        return redirect('/shows')
    else:
        flash('Failed to create an account. Please try again.', 'registrationError')
        return redirect(request.referrer)

@app.route('/login')
def loginPage():
    if 'user_id' in session:
        return redirect('/shows')
    return render_template('login_registration.html')

@app.route('/login', methods=['POST'])
def login():
    if 'user_id' in session:
        return redirect('/')
    
    form_data = request.form
    if not User.validate_user(form_data):
        return redirect(request.referrer)
    
    user = User.get_user_by_email({'email': form_data['email']})
    if not user:
        flash('Invalid email or password', 'loginError')
        return redirect(request.referrer)
    
    if not bcrypt.check_password_hash(user['password'], form_data['password']):
        flash('Invalid email or password', 'loginError')
        return redirect(request.referrer)
    
    session['user_id'] = user['id']
    return redirect('/shows')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


