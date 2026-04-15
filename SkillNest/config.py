import os

class Config:
    # 🔐 Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # 🗄️ Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 📁 File uploads (for future use)
    UPLOAD_FOLDER = os.path.join('static', 'uploads')

    # ⚙️ Optional tweaks (safe defaults)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB upload limit