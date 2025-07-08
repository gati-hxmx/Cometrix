# backend/models/user.py

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name, email, profile_image_url=None, last_login_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.profile_image_url = profile_image_url
        self.last_login_at = last_login_at

