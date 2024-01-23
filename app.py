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
    


'''HOMEPAGE ROUTE - GENERATE PASSWORD LOGIC'''
@app.route('/', methods=['GET', 'POST'])
def home():
   
    chars_list = list(string.ascii_letters) + list(string.digits) + list(string.punctuation) +  list(string.hexdigits) + list(string.octdigits) + list(string.printable) + list(string.ascii_lowercase) + list(string.ascii_uppercase)
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    symbols = string.punctuation
    digits = string.digits
    
    password = ''
    user_input = ''
    generated_password = ''
    uppercase_password = ''
    lowercase_password = ''
    symbols_password = ''


    if request.method == 'POST':
        user_input = request.form.get('user_input')
        uppercase_password = request.form.get('uppercase_password')
        lowercase_password = request.form.get('lowercase_password')
        digits_password = request.form.get('digits_password')
        symbols_password = request.form.get('symbols_password')

        
        #clear the generated_password  if it's not checked
        generated_password = '' if not uppercase_password else generated_password
        
        if(uppercase_password and lowercase_password and digits_password and symbols_password):
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(uppercase_letters + lowercase_letters + digits + symbols) for i in range(int(user_input)))   
                
        elif(uppercase_password and lowercase_password and digits_password):
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(uppercase_letters + lowercase_letters + digits) for i in range(int(user_input)))
        
        elif(uppercase_password and lowercase_password and symbols_password):
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(uppercase_letters + lowercase_letters + symbols) for i in range(int(user_input)))
                
        elif(uppercase_password and digits_password and symbols_password):
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(uppercase_letters + digits + symbols) for i in range(int(user_input)))
                
        elif(lowercase_password and digits_password and symbols_password):
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(lowercase_letters + digits + symbols) for i in range(int(user_input)))     
                
        elif (uppercase_password and lowercase_password):
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(uppercase_letters + lowercase_letters) for i in range(int(user_input)))
        
        elif(uppercase_password and digits_password):
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(uppercase_letters + digits) for i in range(int(user_input)))
        
        elif(uppercase_password and symbols_password):
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(uppercase_letters + symbols) for i in range(int(user_input)))
                
        elif(lowercase_password and digits_password):
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(lowercase_letters + digits) for i in range(int(user_input)))
                
        elif(lowercase_password and symbols_password):
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(lowercase_letters + symbols) for i in range(int(user_input)))
                
        elif(digits_password and symbols_password):
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(digits + symbols) for i in range(int(user_input)))
                
        
        elif lowercase_password:         
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(lowercase_letters) for i in range(int(user_input)))
                
        elif digits_password:
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(digits) for i in range(int(user_input)))
                
        elif symbols_password:
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(symbols) for i in range(int(user_input)))

        #generate a password if the uppercase_password checkbox is checked
        elif uppercase_password:
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(uppercase_letters) for i in range(int(user_input)))
                
        else:
            if user_input.isdigit() and int(user_input) > 0:
                password += ''.join(random.choice(chars_list) for i in range(int(user_input)))
        

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
            return redirect('/dashboard')
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

'''SHOW DASHBOARD'''
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    items = models.Item.select().where(models.Item.user == current_user.id)
    if request.method == 'GET':
        return render_template('dashboard.html', items=items)
    return render_template('dashboard.html')

@app.route('/item-details/<id>', methods=['GET', 'POST'])
def item_details(id):
    item = models.Item.get(models.Item.id == id)
    #show the item details  
    return render_template('item_details.html', item=item)
    

'''ADD ITEM'''
@app.route('/add-item', methods=['GET', 'POST'])
@login_required
def add_item():
    title = request.form.get('title')
    username = request.form.get('username')
    password = request.form.get('password')
    website = request.form.get('website')
    email = request.form.get('email')
    category = request.form.get('category')
    
    if request.method == 'POST':
        if not title or not username or not password or not category:
            return render_template('add_item.html', error='Please fill out all fields')
        
        models.Item.create(title=title, username=username, password=password, website=website, email=email, category=category, user=current_user.id)
        print('item created')
        return redirect('/dashboard')
    
    return render_template('add_item.html')

'''EDIT ITEM'''
@app.route('/items/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    item = models.Item.get(models.Item.id == id)
    if request.method == 'POST':
        title = request.form.get('title')
        username = request.form.get('username')
        password = request.form.get('password')
        website = request.form.get('website')
        email = request.form.get('email')
        category = request.form.get('category')
        
        if not title or not username or not password or not category:
            return render_template('edit_item.html', error='Please fill out all fields')
        
        item.title = title
        item.username = username
        item.password = password
        item.website = website
        item.email = email
        item.category = category
        item.save()
        print('item updated')
        return redirect('/dashboard')
    return render_template('edit_item.html', item=item)

'''DELETE ITEM'''
@app.route('/delete-item/<id>', methods=['GET', 'POST'])
@login_required
def delete_item(id):
    item = models.Item.get(models.Item.id == id)
    if request.method == 'POST':
        item.delete_instance()
        print('item deleted')
        return redirect('/dashboard')
    return render_template('delete_item.html', item=item)

'''Run the app'''
if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)
    


