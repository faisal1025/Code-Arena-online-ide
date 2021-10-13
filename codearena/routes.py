import random, string, subprocess, sys, secrets,  os
from PIL import Image
from flask import render_template, request, flash, session, redirect, url_for
from passlib.hash import sha256_crypt
from functools import wraps
from werkzeug.utils import secure_filename
from codearena.model import User, db, Problems
from codearena import app

def convertToBinary(picFile):
    with open(picFile, 'rb') as file:
        binary_data = file.read()
    return binary_data
    
def convertToFile(binary_data):
    filename = secrets.token_hex(4)
    filename = filename+'.png'
    picFile = f'C:\\Users\\faisa\\Desktop\\Code Arena online ide\\codearena\\static\\defaultProfile\\{filename}'
    file = open(picFile, 'wb')
    file.write(binary_data)
    file.close()
    return filename

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        flash('Unauthorized, please login first', 'warning')
        return redirect(url_for('login', next=request.url))
    return decorated_function

def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            flash('Please logout first already logged in', 'warning')
            return redirect(url_for('myAccount', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

#ide
@app.route('/')
def ide():
    return render_template('ide/ide.html')
    

# signup
@app.route('/signup', methods=['GET', 'POST'])
@logout_required
def signup():
    if request.method == 'POST':
        username = request.form['user_name']
        fullname = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        confpassword = request.form['confpassword']
        gender = request.form['gender']
        country = request.form['country']
        occupation = request.form['occupation']
        college = request.form['work']
        languageList = request.form.getlist('language')
        languages = ''
        for lang in languageList:
            languages += lang+', '
        languages = languages[:-2]
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User.query.filter_by(email=email).first()
            if not user:            
                if password == confpassword:
                    password = sha256_crypt.encrypt(str(password))
                    user1 = User(username=username, name=fullname, email=email, password=password,
                                gender=gender, country=country, occupation=occupation, college=college,
                                language=languages)
                    db.session.add(user1)
                    db.session.commit()
            
                    flash("Account successfully created ", "success")
                    return redirect('/login')
                else:
                    flash("Password does't match", "danger")
                    return redirect('/signup')
            else:
                flash("Email already registered", "info")
                return redirect(url_for('signup'))

        else:
            flash("Username already exist. Please choose different one.", "info")
            return redirect(url_for('signup'))
    return render_template('/auth/signup.html')


#login
@app.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['password'] 

        user1 = User.query.filter_by(username=username).first()

        if user1:
            pw_hash = user1.password
            if sha256_crypt.verify(password, pw_hash):
                session.permanent = True
                session['logged_in'] = True
                session['username'] = user1.username
                session['name'] = user1.name
                session['email'] = user1.email
                session['password'] = user1.password
                session['gender'] = user1.gender 
                session['education'] = user1.college 
                session['occupation'] = user1.occupation
                session['language'] = user1.language
                session['country'] = user1.country
                if user1.pic:
                    session['pic'] = convertToFile(user1.pic)

                flash(f'Welcome {user1.name}, you have successfully logged in', 'success')
                return redirect(url_for('myAccount'))
            else:
                flash('Password doesn\'t matched please enter correct password', 'warning')
                return redirect(url_for('login'))
        else:
            flash('User doesn\'t exist please signup first', 'danger')
            return redirect(url_for("login"))

    return render_template('/auth/login.html')


#logout
@app.route('/logout')
@login_required
def logout():
    if 'pic' in session:
        filename = session['pic']
        picFile = f'codearena/static/defaultProfile/{filename}'
        os.remove(picFile)
    session.clear()
    flash('You are successfully logged out', 'success')
    return redirect(url_for('login'))

#Dashboard
@app.route('/myAccount', methods=['GET', 'POST'])
@login_required
def myAccount():
    if request.method=='POST':
        photo = request.files['pic']
        if photo:
            # creating filename
            filename = secrets.token_hex(4);
            filename = filename+'.png'

            size = (125, 125)
            image = Image.open(photo)
            image.thumbnail(size=size)

            # saving photo file
            image.save(os.path.join("C:\\Users\\faisa\\Desktop\\Code Arena online ide\\codearena\\static\\defaultProfile", secure_filename(filename)))
            picfile = f'C:\\Users\\faisa\\Desktop\\Code Arena online ide\\codearena\\static\\defaultProfile\\{filename}'
            
            if 'pic' in session:
                os.remove(f"codearena/static/defaultProfile/{session['pic']}")
            session['pic'] = filename
            binary_code = convertToBinary(picfile)
            user1 = User.query.filter_by(email=session['email']).first()
            user1.pic = binary_code
            db.session.commit()
            flash('Profile picture updated successfully', 'info')
            return redirect(url_for('myAccount'))
    return render_template('user/dashboard.html')

# Updation Form
@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        fullname = request.form['full_name']
        email = request.form['email']
        gender = request.form['gender']
        country = request.form['country']
        occupation = request.form['occupation']
        college = request.form['work']
        languageList = request.form.getlist('language')
        languages = ''
        for lang in languageList:
            languages += lang+', '
        languages = languages[:-2]

        user = User.query.filter_by(email=email).first()
        if email != session['email'] and user:
            flash('Email already exist please choose another email', 'danger')
            return redirect(url_for('update'))

        user1 = User.query.filter_by(username=session['username']).first()
        session['name'] = user1.name = fullname
        session['email'] = user1.email = email
        session['gender'] = user1.gender = gender
        session['education'] = user1.college = college
        session['occupation'] = user1.occupation = occupation
        session['language'] = user1.language = languages
        session['country'] = user1.country = country
        db.session.commit()
        flash('Account successfully updated', 'success')
        return redirect(url_for('myAccount'))

    return render_template("user/update.html")

# For Deleting Account
@app.route('/deleteAccount')
@login_required
def deleteAccount():
        user1 = User.query.filter_by(username=session['username']).first()
        db.session.delete(user1)
        db.session.commit()
        if 'pic' in session:
                os.remove(f"codearena/static/defaultProfile/{session['pic']}")
        session.clear()
        flash("Account deleted successfully", 'success')
        return redirect(url_for('ide'))


#for compiler
@app.route('/compiler', methods=['GET', 'POST'])
def compiler():
    if request.method == 'POST':
        language = request.form['language']
        code = request.form['code']
        input = request.form['input']
        filename = ''.join(random.choice(string.ascii_letters+'_'+string.digits) for _ in range(10))

        inputFile = f'codearena/static/ide/temp/{filename}.txt'
        inputFile_obj = open(inputFile, 'w')
        inputFile_obj.write(input)
        inputFile_obj.close()
    
        file = f'codearena/static/ide/temp/{filename}.{language}'
        file_obj = open(file, 'w')
        file_obj.write(code)
        file_obj.close()

        if language == 'c':
            exe = subprocess.Popen(["gcc", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = exe.communicate()
            if exe.returncode == 0:
                sys.stdin = open(inputFile, 'r')
                CompletedProcess = subprocess.run('./a.out', capture_output=True, text=True, stdin=sys.stdin)
                sys.stdin.close()
                output = CompletedProcess.stdout
                os.remove(file)
                os.remove(inputFile)
                return output
            os.remove(file)
            os.remove(inputFile)
            return stderr


        if language == 'cpp':
            exe = subprocess.Popen(["g++", file ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = exe.communicate()
            if exe.returncode == 0:
                sys.stdin = open(inputFile, 'r')
                CompletedProcess = subprocess.run('./a.out', capture_output=True, text=True, stdin=sys.stdin)
                sys.stdin.close()
                output = CompletedProcess.stdout
                os.remove(file)
                os.remove(inputFile)
                return output
            os.remove(file)
            os.remove(inputFile)
            return stderr
            

        if language == 'py':
            sys.stdin = open(inputFile, 'r')
            CompletedProcess = subprocess.run(['python3', file], capture_output=True, text=True, stdin=sys.stdin)
            sys.stdin.close()
            if CompletedProcess.returncode == 0:
                output = CompletedProcess.stdout
                os.remove(file)
                os.remove(inputFile)
                return output
            else:
                output = CompletedProcess.stderr
                os.remove(file)
                os.remove(inputFile)
                return output

@app.route('/about')
def about():
    return  render_template("about.html")


@app.route('/aboutme')
def aboutme():
    return render_template("about_me.html")

@app.route('/practice')
def practice():
    problems = Problems.query.all()
    return render_template('practice/practice.html', problems=problems)

@app.route('/practice/<string:code>/')
def question(code):
    problem = Problems.query.filter_by(code=code).first()
    return render_template('practice/question.html', problem=problem)

@app.route('/submitques')
@login_required
def submit():
    return redirect(url_for('ide'))
