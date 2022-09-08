from flask import render_template, request, session, redirect, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.posts import Post
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route( "/" ) 
def redirectFirstPage():
    return redirect ('/login')

@app.route('/login')
def displayLoginform():
    return render_template( "login.html")

@app.route('/login/home', methods = ['POST'])
def redirectToHome():
    email = request.form['email']
    users_password = request.form['users_password']
    data = (email, users_password)
    result  = User.user_login(data)
    print("RESULT LOGIN: ", result)    
    if len( result ) > 0:
        print("RESULT LOGIN: ", result)
        encryptedPassword = result[0]['users_password']
        print("Encripted Password: ", encryptedPassword)
        if bcrypt.check_password_hash( encryptedPassword, users_password ):
            session.clear()
            users_id = result[0]['users_id']
            first_name = result[0]['first_name']
            last_name = result[0]['last_name']
            email = result[0]['email']
            session['users_id'] = users_id
            session['first_name'] = first_name
            session['last_name'] = last_name
            session['email'] = email
            print("ACTUALMENTE EN SESION", session)
            return redirect ('/home')
        else:
            flash( "Password: Credenciales equivocadas.", 'login' )
    else:
        flash( "No existe usuario/password con esta información", 'login' )
    return redirect('/login')

@app.route('/home')
def displayDashboard():
    currentUser = session
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        'users_id': session['users_id']
    }
    fillTable = User.get_all_users(data)
    postus = Post.get_all_posts()
    return render_template( "homepage.html", inSessionData = currentUser, table_users = fillTable, allPostus = postus)

@app.route('/register')
def displayRegistrationform():
    return render_template( "register.html")

@app.route('/register/newuser', methods = ['POST'])
def loadToDBUserInfo():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    users_password = request.form['users_password']
    confirm_users_password = request.form['confirm_users_password']
    if first_name == "" or last_name == "" or email == "" or users_password == "" or confirm_users_password == "":
        flash("Existen campos vacíos, llénelos por favor", 'register')
        return redirect('/register')
    else:
        encryptedpassword = bcrypt.generate_password_hash(users_password)
        data = (first_name,last_name,email,users_password,encryptedpassword,confirm_users_password)
        print("DE FORM 1 REGISTRO: ", data )
        print("FIN DE PARTE REGISTRO ", data)
        if User.validate_registration(data):
            User.user_Registration(data)
        else:
            return redirect('/register')
        return redirect('/login')

@app.route('/<name>/<int:id>', methods = ['GET'])
def displayUserProfile(name, id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id
    }
    print("SOLO DATO USER: ", data)
    userData = User.get_userInformationBy_id(data)
    print("SOLO DATO USER: ", userData)
    currentUser = session
    postusById = Post.get_post_from_one_user(id)
    print("TODOS LOS POSTS POR ID: ", postusById)
    return render_template('profile.html', inSessionData = currentUser, user_In_Table = userData, fromPostDBById = postusById)

@app.route('/delete/account/<id>')
def displayDeleteAccount(id):
    if 'users_id' not in session:
        return redirect("/logout")
    data = {
        "id" : id
    }
    User.delete_user_account(id)
    return redirect('/logout')

@app.route('/logout')
def userlogout():
    session.clear()
    return redirect('/')

