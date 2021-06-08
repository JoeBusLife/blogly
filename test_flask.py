from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        db.drop_all()
        db.create_all()

        user = User(first_name="John", last_name="Doe")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>John Doe</h1>', html)
            self.assertEqual(self.user.image_url, 'https://as2.ftcdn.net/v2/jpg/00/64/67/63/1000_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg')
            self.assertIn(f'<img id="user-img" src="{self.user.image_url}" alt="user image">', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Joe", "last_name": "Hinkle", "image_url": "https://i.giphy.com/media/9rlYe7LGZNwSqRiPzJ/200w.gif"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            user = User.query.get(2)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<a href="/users/{user.id}">Joe Hinkle</a>', html)
            self.assertEqual(user.image_url, "https://i.giphy.com/media/9rlYe7LGZNwSqRiPzJ/200w.gif")
            
    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'<a href="/users/{self.user_id}">John Doe</a>', html)


class PostViewsTestCase(TestCase):
    """Tests for views for Posts."""

    def setUp(self):
        """Add sample users and posts."""

        db.drop_all()
        db.create_all()

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

        (self.user1_id, self.user2_id, self.user3_id) = (user1.id, user2.id, user3.id)
        (self.user1, self.user2, self.user3) = (user1, user2, user3)
        (self.post1_id, self.post2_id, self.post3_id, self.post4_id) = (post1.id, post2.id, post3.id, post4.id)
        (self.post1, self.post2, self.post3, self.post4) = (post1, post2, post3, post4)

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_recent_posts(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)
            self.assertIn('By Y Knot', html)
            self.assertIn('You can do it!', html)
            
    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post1_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Hello</h2>', html)
            self.assertIn('<i>By John Doe</i>', html)
            self.assertEqual(self.post1.content, 'I am boring')
            self.assertIn(f'<button formaction="/users/{self.post1.user_id}">Back</button>', html)
            self.assertIn(f'<button formaction="/posts/{self.post1_id}/delete" formmethod="POST">Delete</button>', html)
            
    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "3rd post", "content": "I am so helpful", "user_id": self.user3_id}
            resp1 = client.post(f"/users/{self.user3_id}/posts/new", data=d, follow_redirects=True)
            html1 = resp1.get_data(as_text=True)

            self.assertEqual(resp1.status_code, 200)
            self.assertIn(f'<a href="/posts/5">3rd post</a>', html1)
            
            # Does new post show up on home page as most recent post
            resp2 = client.get("/")
            html2 = resp2.get_data(as_text=True)
            
            self.assertEqual(resp2.status_code, 200)
            self.assertIn(f'<h1>Blogly Recent Posts</h1>\n\n\n<h2><a class="story-h2" href="/posts/5">3rd post</a></h2>', html2)
            
            # Does new post details page work
            resp3 = client.get("/posts/5")
            html3 = resp3.get_data(as_text=True)
            
            self.assertEqual(resp3.status_code, 200)
            self.assertIn('<p>I am so helpful</p>', html3)
            
    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post3_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'<a href="/posts/{self.post3_id}">{self.post3.title}</a>', html)
            
            