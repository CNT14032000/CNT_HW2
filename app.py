from flask import Flask, render_template, redirect, url_for, request ,session,flash, make_response,session
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import random
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'\x0b\xdc\x8b?~\xf9\xa4\x96\x99\xf6/<\x95\xc0v\xbb'
client = MongoClient('localhost', 27017)
db = client['auth']
bcrypt = Bcrypt(app)

# Configure upload folder

app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        sessionid = request.cookies.get('sessionid',"")
        session = db.sessions.find_one({'sessionid': sessionid})
        if session is not None:
            return redirect('/profile')
        else:
            return render_template('login.html')
   
    
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        
        user = db.users.find_one({'username':username})
        if user is not None and bcrypt.check_password_hash(user['password'],password):
            sessionid = str(random.randint(10**10,10**20))
            db.sessions.insert_one({
                'sessionid': sessionid,
                'user': username
            })
            resp = make_response(redirect('/profile'))
            resp.set_cookie('sessionid',sessionid)
            return resp
        else:
            flash('invalid username or password')
            return render_template('login.html')

@app.route('/profile',methods=['GET', 'POST'])
def profile():
    sessionid = request.cookies.get('sessionid',"")
    session = db.sessions.find_one({'sessionid': sessionid})
    if session is not None:
        user_info = db.users.find_one({'username':session['user']})
        #print(user_info)
        if 'profile_picture' not in user_info:
            user_info['profile_picture'] = 'default_picture.jpg'
        return render_template('profile.html',user=user_info)
    else:
        return redirect('/')

@app.route('/register',methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        email = request.form['email']
        user = db.users.find_one({'email':email})
        if user is not None:
            flash('This email is already registered')
            return redirect('/register')
        else:
            hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
            db.users.insert_one({
                'username': username,
                'password': hash_password,
                'email': email
            })
            flash('Registration successfully')
            return redirect('/')

@app.route('/logout')
def logout():
    sessionid = request.cookies.get('sessionid',"")
    #print(sessionid)
    db.sessions.find_one_and_delete({'sessionid': sessionid})
    session.clear()
    resp = make_response(redirect('/'))
    resp.set_cookie('sessionid', '', expires=0)  # Delete cookie
    return resp

@app.route('/change_password',methods=['GET','POST'])
def change_password():
    sessionid = request.cookies.get('sessionid',"")
    session = db.sessions.find_one({'sessionid': sessionid})

    if session is None:
        return redirect('/')
    if request.method == 'GET':
        user_info = db.users.find_one({'username':session['user']})
        if 'profile_picture' not in user_info:
            user_info['profile_picture'] = 'default_picture.jpg'
        return render_template('change_password.html',user=user_info)
    if request.method == 'POST':
        curr_password = request.form['current-password']
        new_password = request.form['new-password']
        conf_password = request.form['confirm-password']
        user = db.users.find_one({'username':session['user']})
        if user is not None and bcrypt.check_password_hash(user['password'], curr_password):
            if new_password==conf_password:
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                db.users.update_one({'username':session['user']},{"$set":{'password':hashed_password}})
                flash("Password updated successfully!")
                return redirect('/profile')
            else:
                flash("new-password and confirm-passowrd are not the same")
        else:
            flash('Invalid password')
    return redirect('/change_password')

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    sessionid = request.cookies.get('sessionid',"")
    session = db.sessions.find_one({'sessionid': sessionid})
    if session is None:
        return redirect('/')
    if request.method == 'GET':
        user_info = db.users.find_one({'username':session['user']})
        if 'profile_picture' not in user_info:
            user_info['profile_picture'] = 'default_picture.jpg'
        #print(user_info)
        return render_template('edit_profile.html',user=user_info)
    if request.method =='POST':
       
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        birthday = request.form['birthday']
        profession = request.form['profession']
        
        db.users.update_one(
            {'username':session['user']},
            {"$set":{
                'fullname':fullname,
                'email': email,
                'phone': phone,
                'birthday': birthday,
                'profession': profession
                }
            }
        )
        flash("Profile updated successfully!")
        return redirect('/profile')
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_profile_picture', methods=["POST"])
def upload_profile_picture():
    sessionid = request.cookies.get('sessionid', "")
    session = db.sessions.find_one({'sessionid': sessionid})

    if 'profile_picture' not in request.files:
        return redirect(request.url)
    
    file = request.files['profile_picture']
    if file.filename == '':
        flash('No selected file')
        return redirect('/edit_profile')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        db.users.update_one(
            {'username':session['user']},
            {
                '$set': {
                    'profile_picture': filename
                }
            }
        ) 
        flash('Image uploaded successfully')
        return redirect('/profile')
    else:
        flash('File not allowed')
        return redirect('/edit_profile')
if __name__ == '__main__':
    app.run(debug=True)
"""""
@app.route('/profile')
def profile():
    user_info = {
        "name": "Cao Ngoc Tuan",
        "bio": "Newbie Full Stack Developer",
    }
    return render_template('index.html', user=user_info)
"""