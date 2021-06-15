"""Blogly application."""
from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, User, Post, Tag, PostTag
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
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
    posts = Post.query.order_by(desc('created_at')).limit(5).all()
    return render_template('home.html', posts=posts)
    # return redirect('/users')


@app.route('/users')
def show_users():
    """  """
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)
    
    
@app.route('/users/new')
def new_user_form():                          
    """  """
    
    return render_template('users_new.html')
    
    
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
    return render_template('user.html', user=user)
    
    
@app.route('/users/<int:user_id>/edit')
def edit_user_info_form(user_id):
    """  """
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user)


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



@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """  """
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('user_new_post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def submit_new_post(user_id):
    """  """
    tag_ids = [int(tag_id) for tag_id in request.form.getlist("post-tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    title = request.form["title"]
    content = request.form["content"]
    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)
    
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')


@app.route('/posts/<post_id>')
def show_post(post_id):
    """  """
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/posts/<post_id>/edit')
def edit_post_form(post_id):
    """  """
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    
    for tag in tags:
        tag.check = "checked" if tag in post.tags else ""
    
    return render_template('post_edit.html', post=post, tags=tags)


@app.route('/posts/<post_id>/edit', methods=['POST'])
def submit_edit_post(post_id):
    """  """
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    
    tag_ids = [int(tag_id) for tag_id in request.form.getlist("post-tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    # db.session.add(post)
    
    # form_post_tags = request.form.getlist("post-tags")
    # new_post_tags = [PostTag(post_id=post_id, tag_id=int(tag_id)) for tag_id in form_post_tags]
    # PostTag.query.filter_by(post_id=post_id).delete()
    # db.session.add_all(new_post_tags)    
    
    db.session.add(post)
    db.session.commit()
    
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<post_id>/delete', methods=['POST'])
def submit_delete_post(post_id):
    """  """
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()
    
    return redirect(f'/users/{post.user_id}')



@app.route('/tags')
def show_tags():
    """  """
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)
    
    
@app.route('/tags/new')
def new_tag_form():                          
    """  """
    
    return render_template('tags_new.html')
    
    
@app.route('/tags/new', methods=['POST'])
def submit_new_tag():
    """  """
    new_tag = Tag(name=request.form["name"])
    request.form.getlist('hello[]')
    
    db.session.add(new_tag)
    db.session.commit()
    
    return redirect('/tags')
    
    
@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """  """
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag.html', tag=tag)
    
    
@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """  """
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_edit.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def submit_edit_tag(tag_id):
    """  """
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]
    
    db.session.add(tag)
    db.session.commit()
    
    return redirect('/tags')

    
@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def submit_delete_tag(tag_id):
    """  """
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    
    return redirect('/tags')