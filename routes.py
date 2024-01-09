from werkzeug.utils import secure_filename
from form import addPost, editPost, signUp, loginForm, addComment
import os
from models import Product, User, Comment
from extensions import app, render_template, db, redirect, request
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime
from flask import request
import random

@app.route('/profile')
@login_required
def profile():
    posts = Product.query.all()[::-1]
    return render_template(
        'profile.html',
        form=addComment(),
        comments=Comment.query.all(),
        your_posts=list(filter(lambda x: current_user.name == x.username, posts)),
        current_time=datetime.now(),
        liked_posts=list(filter(lambda x: current_user in x.liked_by, posts)),
        )

@app.route('/comment/<int:product_id>', methods=["GET","POST"])
@login_required
def comment(product_id):
    form = addComment()
    if form.validate_on_submit():
        if current_user.is_authenticated:
                new_comment = Comment(
                    comment=form.comment.data,
                    username=current_user.name,
                    user_id=current_user.id,
                    product_id=product_id,
                    pfp=current_user.pfp,
                    )
                db.session.add(new_comment)
                db.session.commit()
    return redirect('/')

# home page
@app.route('/')
def home():
    posts = Product.query.all()[::-1]
    return render_template(
        'index.html',
        form=addComment(),
        comments=Comment.query.all(),
        posts=posts,
        current_time=datetime.now(),
        )


# add_post page
@app.route('/add_post', methods=["GET","POST"])
@login_required
def inner():
    form = addPost()
    if form.validate_on_submit():
        if form.img.data:
            filename = str(random.randint(1, 
            10000000000000000000000000000000000000000000000000000000000000000000000000000000000000))
            new_product = Product(
                title=form.title.data,
                img=f'./static/images/{filename}', 
                username=current_user.name,
                pfp=current_user.pfp,
                )
            form.img.data.save(os.path.join(app.root_path, './static/images', filename))
            db.session.add(new_product)
            db.session.commit()
            return redirect('/')

    return render_template('addpost.html', form=form)

# edit page
@app.route('/edit/<int:product_id>', methods=["GET","POST"])
@login_required
def edit(product_id):
    product = Product.query.get(product_id)
    form = editPost(title=product.title)
    if form.validate_on_submit():
        product.title = form.title.data
        if form.img.data:
            filename = secure_filename(form.img.data.filename)
            form.img.data.save(os.path.join(app.root_path, './static/images', filename))
            product.img = f'./static/images/{filename}'
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', form=form)

# delete
@app.route('/delete/<int:product_id>', methods=["GET","POST"])
@login_required
def delete(product_id):
    product = Product.query.get(product_id)
    os.remove(os.path.join(app.root_path, product.img)) 
    db.session.delete(product)
    db.session.commit()
    return redirect('/')

@app.route('/like', methods=['GET','POST'])
def like():
    if current_user.is_authenticated:
        post_id = request.form.get('post_id')
        product = Product.query.get(post_id)

        already_liked = current_user in product.liked_by
        already_disliked = current_user in product.disliked_by

        if already_liked:
            product.like -= 1
            product.liked_by.remove(current_user)
        else:
            product.like += 1
            product.liked_by.append(current_user)
        if already_disliked:
            product.dislike -= 1
            product.disliked_by.remove(current_user)

        db.session.commit()

        return redirect('/')
    else:
        return redirect('/signup')

@app.route('/dislike', methods=['GET','POST'])
def dislike():
    if current_user.is_authenticated:
        post_id = request.form.get('post_id')
        product = Product.query.get(post_id)

        already_disliked = current_user in product.disliked_by
        already_liked = current_user in product.liked_by

        if already_disliked:
            product.dislike -= 1
            product.disliked_by.remove(current_user)
        else:
            product.dislike += 1
            product.disliked_by.append(current_user)

        if already_liked:
            product.like -= 1
            product.liked_by.remove(current_user)

        db.session.commit()

        return redirect('/')
    else:
        return redirect('/signup')


@app.route('/signup', methods=['GET','POST'])
def signup():
    form = signUp()
    if form.validate_on_submit():
        existing_user = User.query.filter(User.name == form.name.data).first()
        if existing_user:
            return 'this name already exist'
        else:
            filename = str(random.randint(1, 
            1000000000000000000000000000000000000000000000000000000000000000000000000000000000))
            new_user = User(name=form.name.data,password=form.password.data,pfp=f'./static/images/{filename}',role='user')
            form.pfp.data.save(os.path.join(app.root_path, './static/images', filename))

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect('/')
    return render_template('signup.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter(form.name.data == User.name).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect('/')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')