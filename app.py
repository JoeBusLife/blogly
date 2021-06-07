"""Blogly application."""
from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "soup"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home():
    """  """
    return redirect('/users')


@app.route('/users')
def show_users():
    """  """
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)
    
    
@app.route('/users/new')
def new_user_form():
    """  """
    
    return render_template('user_new.html')
    
    
@app.route('/users/new', methods=['POST'])
def submit_new_user():
    """  """
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    image_url = image_url if image_url else None
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')
    
    
@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """  """
    user = User.query.get_or_404(user_id)
    return render_template('user_info.html', user=user)
    
    
@app.route('/users/<int:user_id>/edit')
def edit_user_info_form(user_id):
    """  """
    user = User.query.get_or_404(user_id)
    return render_template('user_info_edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def submit_edit_user_info(user_id):
    """  """
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    user.image_url = image_url if image_url else 'https://as2.ftcdn.net/v2/jpg/00/64/67/63/1000_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg'
    
    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')

    
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def submit_delete_user(user_id):
    """  """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')