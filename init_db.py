from app import create_app
from ext import db
from models import Team


def database():
    app = create_app()
    with app.app_context():
        db.create_all()

        if not Team.query.first():
            db.session.commit()


if __name__ == '__main__':
    database()