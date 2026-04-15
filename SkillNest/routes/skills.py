from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import SkillPost
from extensions import db

skills = Blueprint('skills', __name__)


# ➕ Post a Skill
@skills.route('/post-skill', methods=['GET', 'POST'])
@login_required
def post_skill():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        rate = request.form['rate']
        location = request.form['location']

        new_skill = SkillPost(
            title=title,
            description=description,
            category=category,
            rate=rate,
            location=location,
            user_id=current_user.id
        )

        db.session.add(new_skill)
        db.session.commit()

        return redirect(url_for('main.home'))

    return render_template('post_skill.html')


# 📄 View all skills
@skills.route('/skills')
def view_skills():
    category = request.args.get('category')
    location = request.args.get('location')
    search = request.args.get('search')

    query = SkillPost.query

    if category:
        query = query.filter(SkillPost.category.ilike(f"%{category}%"))

    if location:
        query = query.filter(SkillPost.location.ilike(f"%{location}%"))

    if search:
        query = query.filter(SkillPost.title.ilike(f"%{search}%"))

    skills = query.order_by(SkillPost.created_at.desc()).all()

    return render_template('browse_skills.html', skills=skills)