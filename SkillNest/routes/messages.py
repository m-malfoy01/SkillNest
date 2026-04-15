from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import Message, User
from extensions import db

messages = Blueprint('messages', __name__)


# 💬 Chat with specific user
@messages.route('/chat/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat(user_id):
    other_user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        content = request.form['message']

        new_msg = Message(
            sender_id=current_user.id,
            receiver_id=other_user.id,
            content=content
        )

        db.session.add(new_msg)
        db.session.commit()

        return redirect(url_for('messages.chat', user_id=user_id))

    # fetch messages both ways
    chats = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    return render_template('chat.html', chats=chats, user=other_user)