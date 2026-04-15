from flask import Blueprint, render_template, redirect
from flask_login import current_user, login_required
from models import User, SkillPost, Message, Rating

main = Blueprint('main', __name__)


# 🏠 Landing / Home
@main.route('/')
def home():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    return render_template('landing.html')


# 📊 Dashboard
@main.route('/dashboard')
@login_required
def dashboard():
    # 🔢 Stats
    total_users = User.query.count()
    total_skills = SkillPost.query.count()
    total_messages = Message.query.count()
    total_ratings = Rating.query.count()

    avg_rating = 0
    if total_ratings > 0:
        avg_rating = round(
            sum(r.score for r in Rating.query.all()) / total_ratings, 2
        )

    # 🛠️ Skills
    skills = SkillPost.query.order_by(SkillPost.created_at.desc()).all()

    return render_template(
        'dashboard.html',
        total_users=total_users,
        total_skills=total_skills,
        total_messages=total_messages,
        avg_rating=avg_rating,
        skills=skills
    )
@main.route('/profile')
@login_required
def profile():
    user = current_user
    return render_template('profile.html', user=user)