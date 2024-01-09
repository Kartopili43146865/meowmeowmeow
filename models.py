from extensions import db, app
from flask_login import UserMixin, LoginManager
from sqlalchemy import func

login_manager = LoginManager(app)

user_likes = db.Table('user_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)
user_dislikes = db.Table('user_dislikes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    img = db.Column(db.String)
    username = db.Column(db.String)
    pfp = db.Column(db.String)

    like = db.Column(db.Integer, default=0)
    liked_by = db.relationship('User', backref='liked_products', secondary=user_likes, lazy='dynamic', single_parent=True)

    dislike = db.Column(db.Integer, default=0)
    disliked_by = db.relationship('User', backref='disliked_products', secondary=user_dislikes, lazy='dynamic', single_parent=True)
   
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    likes = db.relationship('Product', secondary=user_likes, backref=db.backref('liking_users', lazy='dynamic'))
    dislikes = db.relationship('Product', secondary=user_dislikes, backref=db.backref('disliking_users', lazy='dynamic'))
    role = db.Column(db.String)
    pfp = db.Column(db.String)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, unique=True)
    username = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    pfp = db.Column(db.String)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def seed_data():
    with app.app_context():
        default_user = User(name='admin', password='admin123', role='admin', pfp='../static/images/adminpfp.svg')
        default_post_1 = Product(title='car', img='https://images.unsplash.com/photo-1529778873920-4da4926a72c2?q=80&w=1336&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', username='admin', pfp='../static/images/adminpfp.svg')
        default_post_2 = Product(title='car', img='https://images.unsplash.com/photo-1561389248-231c46a75a97?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGN1dGUlMjBjYXR8ZW58MHx8MHx8fDA%3D', username='admin', pfp='../static/images/adminpfp.svg')
        default_post_3 = Product(title='car', img='https://images.unsplash.com/photo-1561389881-a5d8d5549588?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTh8fGN1dGUlMjBjYXR8ZW58MHx8MHx8fDA%3D', username='admin', pfp='../static/images/adminpfp.svg')

        default_user.likes.append(default_post_1)
        default_user.likes.append(default_post_2)
        default_user.likes.append(default_post_3)



        db.session.add_all([default_user, default_post_1, default_post_2,default_post_3])
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data()