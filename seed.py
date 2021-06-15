"""Seed file to make sample data for pets db."""

from models import db, User, Post, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
Post.query.delete()
User.query.delete()


user1 = User(first_name="John", last_name="Doe")
user2 = User(first_name="Kane", last_name="Frost", image_url="https://redefined.s3.us-east-2.amazonaws.com/wp-content/uploads/2021/04/12063628/CodyFrost_CreditNaomiKane.jpg")
user3 = User(first_name="Y", last_name="Knot", image_url="https://studio.cults3d.com/R8GCnaENC21XYRj8-iqVydxadNs=/516x516/https://files.cults3d.com/uploaders/13798904/illustration-file/1ea55fbd-b647-4e16-a72b-912dbad31faa/34f35a7348ce15f7e782a899e83dfe4c_display_large.jpg")
        
db.session.add_all([user1, user2, user3])
db.session.commit()
        
post1 = Post(title="Hello", content="I am boring", user_id=1)
post2 = Post(title="Why?", content="Life is so rounded, its pointless", user_id=2)
post3 = Post(title="You can do it!", content='Cause "Y Knot"', user_id=3)
post4 = Post(title="Yolo", content="Sieze the day hombre", user_id=3)
        
db.session.add_all([post1, post2, post3, post4])
db.session.commit()

tag1 = Tag(name='yolo')
tag2 = Tag(name='bro')
tag3 = Tag(name='boring')
tag4 = Tag(name='sad')

db.session.add_all([tag1, tag2, tag3, tag4])
db.session.commit()

post_tag1 = PostTag(post_id=1, tag_id=3)
post_tag2 = PostTag(post_id=2, tag_id=4)
post_tag3 = PostTag(post_id=3, tag_id=2)
post_tag4 = PostTag(post_id=3, tag_id=1)
post_tag5 = PostTag(post_id=4, tag_id=1)

db.session.add_all([post_tag1, post_tag2, post_tag3, post_tag4, post_tag5])
db.session.commit()