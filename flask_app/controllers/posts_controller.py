from flask import render_template, request, session, redirect
from flask_app import app
from flask_app.models.posts import Post



@app.route( "/home/post", methods = ['POST'] ) 
def sendPostu():
    if 'users_id' not in session:
        return redirect('/logout')
    posts_content = request.form['posts_content']
    user_id = request.form['users_id']
    data = (posts_content, user_id)
    print("DE FORM 3 POST USUARIO: ", data )
    print("FIN PARTE DE REGISTRO" , data)
    if Post.validate_post(data):
        Post.send_post(data)
    else:
        print("valores incorrectos")
        return redirect('/home')
    print("FIN DE POST")
    return redirect('/home')

@app.route("/post/edit/<id>", methods = ['GET'])
def displayEditWindow(id):
    if 'users_id' not in session:
        return redirect('/logout')
    currentUser = session
    usersPost = Post.get_single_post(id)
    return render_template( "editpost.html", inSessionData = currentUser, singleUserPost = usersPost)
    
@app.route( "/update/post/<id>", methods = ['POST'] ) 
def updatePostu(id):
    if 'users_id' not in session:
        return redirect('/logout')
    posts_content = request.form['update_posts_content']
    user_id = request.form['user_id']
    post_id = request.form['post_id']
    data = (posts_content, user_id, post_id)
    if Post.validate_post(data):
        Post.update_post(data)
    else:
        print("valores incorrectos")
        return redirect('/post/edit/<id>')
    print("FIN DE POST")
    return redirect('/home')

@app.route("/home/delete/<id>")
def deleteThisPost(id):
    if 'users_id' not in session:
        return redirect("/logout")
    Post.delete_post(id)
    return redirect('/home')