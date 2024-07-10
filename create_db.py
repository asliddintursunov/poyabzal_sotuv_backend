from app import create_app
from extensions import db

flask_app = create_app()
with flask_app.app_context():
    db.create_all()
    print("Database created :)")