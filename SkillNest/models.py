from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime


# 🔐 Required for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 👤 User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    # Relationship
    skills = db.relationship('SkillPost', backref='user', lazy=True)
    @property
    def average_rating(self):
        ratings = Rating.query.filter_by(rated_user_id=self.id).all()
        if ratings:
            return round(sum(r.score for r in ratings) / len(ratings), 1)
        return "No ratings"

    def __repr__(self):
        return f"<User {self.email}>"



# 🛠️ Skill Posting Model
class SkillPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Skill {self.title}>"
    
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    rater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rated_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    score = db.Column(db.Integer, nullable=False)  # 1 to 5
    review = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)