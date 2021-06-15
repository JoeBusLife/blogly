"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    first_name = db.Column(db.String(20),
                            nullable=False)
    
    last_name = db.Column(db.String(20),
                            nullable=False)
    
    image_url = db.Column(db.Text,
                            nullable=False,
                            default='https://as2.ftcdn.net/v2/jpg/00/64/67/63/1000_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg')
    
    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")
    
    @property
    def full_name(self):
        """Return user full name"""

        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"
    
    
class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    title = db.Column(db.String(50),
                        nullable=False)
    
    content = db.Column(db.Text,
                        nullable=False)
    
    created_at = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.now)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    
    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content created_at={p.created_at} user_id={p.user_id}>"
    
    
class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    name = db.Column(db.String(50),
                        nullable=False)
    
    posts = db.relationship('Post', secondary='posts_tags', backref='tags')
    
    def __repr__(self):
        t = self
        return f"<Tag id={t.id} name={t.name}>"
    
    
class PostTag(db.Model):
    __tablename__ = 'posts_tags'
    
    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
    
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        primary_key=True)
    
    def __repr__(self):
        pt = self
        return f"<Post id={pt.post_id} Tag id={pt.tag_id}>"