from flask_login import UserMixin
from ext import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    predictions = db.relationship('Prediction', backref='user', lazy=True)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    group_letter = db.Column(db.String(1), nullable=False)
    matches_played = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    match_details = db.Column(db.String(200), nullable=False)
    predicted_home_score = db.Column(db.Integer, nullable=False)
    predicted_away_score = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.CheckConstraint('predicted_home_score >= 0', name='check_home_score_positive'),
        db.CheckConstraint('predicted_away_score >= 0', name='check_away_score_positive'),
    )