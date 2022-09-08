from flask import render_template, request, session, redirect
from flask_app import app
from flask_app.models.posts import Post
from flask_app.models.like import Like 


@app.route('/home/post/like', methods = ['POST'])
def sendLikeDB():
    if 'users_id' not in session:
        return redirect('/logout')
    post_likes = request.form['likes_counts']
    user_id = request.form['users_id']
    post_id = request.form['posts_id']
    data = ( post_likes, user_id, post_id )
    print("DE FORM FOR LIKE: ", data )
    print("FIN DE PARTE SENDLIKE ", data)
    result = Like.add_likes(data)
    print("LIKES RESULTS: ", result)
    return redirect('/home')

@app.route('/post/likes/<id>', methods = ['GET'])
def likePostViews(id):
    if 'users_id' not in session:
        return redirect('/logout')
    currentUser = session
    usersPost = Post.get_single_post(id)
    userWhoLiked = Like.users_who_liked(id)
    print("USERS A QUIENES LES HA GUSTADO EL POST", userWhoLiked)
    return render_template( "likesview.html", inSessionData = currentUser, singleUserPost = usersPost, userWhoLiked = userWhoLiked)