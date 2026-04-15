from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import Rating, User
from extensions import db

ratings = Blueprint('ratings', __name__)


@ratings.route('/rate/<int:user_id>', methods=['GET', 'POST'])
@login_required
def rate_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        score = int(request.form['score'])
        review = request.form['review']

        new_rating = Rating(
            rater_id=current_user.id,
            rated_user_id=user.id,
            score=score,
            review=review
        )

        db.session.add(new_rating)
        db.session.commit()

        return redirect(url_for('skills.view_skills'))

    return render_template('rate.html', user=user)