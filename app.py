#Third-party Libraries
from flask import Flask, render_template, request, redirect, g, url_for, flash
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from playhouse.shortcuts import model_to_dict

#Internal imports 
from config import secret_key
import models

#Python libraries 
import random, string
import sqlite3
import json

app = Flask(__name__)

'''User Session management setup'''
#secretKey to encode the session
app.secret_key = secret_key
#sets up the session
login_manager = LoginManager()
#Initialize login manager
login_manager.init_app(app)

#loads the user from the user ID that Flask-Login stores in the user's session
@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None
    
    
'''Database connection'''
@app.before_request
def before_request():
    '''Connect to the database before each request'''
    g.db = models.database
    g.db.connect()
    
@app.after_request
def after_request(response):
    '''Close the database connection after each request'''
    g.db.close()
    return response
    


'''HOMEPAGE ROUTE'''
@app.route('/', methods=['GET', 'POST'])
def home():
    user_input= None
    chars_list = list(string.ascii_letters) + list(string.digits) + list(string.punctuation) +  list(string.hexdigits) + list(string.octdigits) + list(string.printable) + list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits)
    
    password = ' '
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        
        #checks if user_input is a positive num and greater than 0
        if user_input.isdigit() and int(user_input) > 0:
            for i in range(int(user_input)):
                password += random.choice(chars_list)
            
    #render_template() function is used to render an HTML page
    return render_template('index.html', user_input=password)



'''LOGIN ROUTE'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('login.html', error='Please fill out all fields')
        
        user = models.User.get(models.User.username == username) 
        
        if user and check_password_hash(user.password, password):
            user_dict = model_to_dict(user)
            del user_dict['password']
            login_user(user)
            print('user logged in')
            return redirect('/')
        else:
            print('username or password is incorrect')
            return render_template('login.html', error='Username or password is incorrect')
    return render_template('login.html')
    
    

'''LOGOUT ROUTE'''
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        print('user logged out')
        return redirect('/')
    return render_template('logout.html')


'''Login Manager Config'''
#redirect users to the login page when they aren't logged in and try to access a login_required view
login_manager.login_view = 'login'
login_manager.login_message = 'You need to login to view this page'



'''CREATE ACCOUNT ROUTE'''''
@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not username or not password or not email:
            return render_template('create_account.html', error='Please fill out all fields')
        
        try:
            models.User.get(models.User.username == username)
            print('user exists')
            return render_template('create_account.html', error='A user with that username or email already exists')
        except models.DoesNotExist:
            try:
                models.User.get(models.User.email == email)
                print('user exists')
                return render_template('create_account.html', error='A user with that username or email already exists')
            except models.DoesNotExist:
                hashed_password = generate_password_hash(password)
                models.User.create(username=username, email=email, password=hashed_password)
                flash('Account created successfully', 'success')
                print('account created')
                return redirect(url_for('/'))
        
    return render_template('create_account.html')


'''Run the app'''
if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)
    


