from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()
with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Role: {user.role}")
