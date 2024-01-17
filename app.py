#contains Flask routes
from flask import Flask, render_template, request, redirect
import random, string

app = Flask(__name__)

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_name = None
    main_password = None
    
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        main_password = request.form.get('main_password')
        #side note: hash password 
        if user_name and main_password:
            return redirect('/')
        
    return render_template('login.html', user_name=user_name, main_password=main_password)

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    username = ''
    password = ''
    email = ''
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        if username and password and email:
            return redirect('/index.html', )
    return render_template('create_account.html', username=username, password=password, email=email)




if __name__ == '__main__':
    app.run(debug=True)
    


