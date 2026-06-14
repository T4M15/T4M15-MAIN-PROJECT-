from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ext import db
from models import User, Team, Prediction
from forms import RegisterForm, LoginForm, PredictionForm

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful.', 'danger')
    return render_template('login.html', form=form)


@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@main.route('/teams')
def teams():
    all_teams = Team.query.order_by(Team.group_letter, Team.points.desc()).all()
    return render_template('teams.html', teams=all_teams)


@main.route('/matches', methods=['GET', 'POST'])
def matches():
    form = PredictionForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You must be logged in to make a prediction!', 'danger')
            return redirect(url_for('main.login'))

        prediction = Prediction(
            user_id=current_user.id,
            match_details=form.match_details.data,
            predicted_home_score=form.home_score.data,
            predicted_away_score=form.away_score.data
        )
        db.session.add(prediction)
        db.session.commit()
        flash('Prediction submitted successfully!', 'success')
        return redirect(url_for('main.matches'))

    user_predictions = []
    if current_user.is_authenticated:
        user_predictions = Prediction.query.filter_by(user_id=current_user.id).all()

    return render_template('matches.html', form=form, predictions=user_predictions)


@main.route('/prediction/delete/<int:id>', methods=['POST'])
@login_required
def delete_prediction(id):
    prediction = Prediction.query.get_or_404(id)
    if prediction.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('main.matches'))
    db.session.delete(prediction)
    db.session.commit()
    flash('Prediction removed.', 'success')
    return redirect(url_for('main.matches'))


@main.route('/prediction/update/<int:id>', methods=['POST'])
@login_required
def update_prediction(id):
    prediction = Prediction.query.get_or_404(id)
    if prediction.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('main.matches'))

    home_score = request.form.get('home_score')
    away_score = request.form.get('away_score')

    if home_score is not None and away_score is not None:
        try:
            prediction.predicted_home_score = int(home_score)
            prediction.predicted_away_score = int(away_score)
            db.session.commit()
            flash('Prediction updated!', 'success')
        except ValueError:
            flash('Invalid input data.', 'danger')

    return redirect(url_for('main.matches'))



@main.route('/wcmatches')
def wcmatches():
    return render_template('wcmatches.html')