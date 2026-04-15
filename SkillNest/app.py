from flask import Flask
from config import Config
from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 🔌 Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # 📦 Import models (VERY IMPORTANT)
    from models import User, SkillPost

    # 🧭 Register routes (we’ll create these next)
    from routes.auth import auth
    from routes.skills import skills
    from routes.main import main

    app.register_blueprint(auth)
    app.register_blueprint(skills)
    app.register_blueprint(main)

    # 🗄️ Create database
    with app.app_context():
        db.create_all()

    return app


app = create_app()

from routes.messages import messages
app.register_blueprint(messages)

from routes.ratings import ratings
app.register_blueprint(ratings)


if __name__ == "__main__":
    app.run(debug=True)