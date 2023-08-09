from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.String(8), unique=True, nullable=False)
    checking_balance = db.Column(db.Float, nullable=False)
    savings_balance = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


def validate_pin(pin):
    return 4 <= len(pin) <= 8 and pin.isdigit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pin = request.form['pin']

        if not validate_pin(pin):
            flash('Invalid PIN. Please enter a 4 to 8 digit PIN.')
            return redirect(url_for('index'))

        user = User.query.filter_by(pin=pin).first()

        if not user:
            flash('PIN not found. Please try again.')
            return redirect(url_for('index'))

        return redirect(url_for('atm', user_id=user.id))

    return render_template('index.html')


@app.route('/atm/<int:user_id>', methods=['GET', 'POST'])
def atm(user_id):
    try:
        user = User.query.get_or_404(user_id)
    except SQLAlchemyError as e:
        print(e)
        flash('Database error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        action = request.form['action']

        if action == 'logout':
            return redirect(url_for('index'))

        amount = request.form['amount']

        if not amount.isdigit() or float(amount) < 0:
            flash('Invalid input. Please enter a positive numeric value.')
            return redirect(url_for('atm', user_id=user.id))

        amount = float(amount)

        if action == 'deposit_checking':
            user.checking_balance += amount
        elif action == 'deposit_savings':
            user.savings_balance += amount
        elif action == 'withdraw_checking':
            if user.checking_balance < amount:
                flash('Insufficient funds.')
                return redirect(url_for('atm', user_id=user.id))
            user.checking_balance -= amount
        elif action == 'withdraw_savings':
            if user.savings_balance < amount:
                flash('Insufficient funds.')
                return redirect(url_for('atm', user_id=user.id))
            user.savings_balance -= amount
        elif action == 'transfer_checking_savings':
            if user.checking_balance < amount:
                flash('Insufficient funds.')
                return redirect(url_for('atm', user_id=user.id))
            user.checking_balance -= amount
            user.savings_balance += amount
        elif action == 'transfer_savings_checking':
            if user.savings_balance < amount:
                flash('Insufficient funds.')
                return redirect(url_for('atm', user_id=user.id))
            user.savings_balance -= amount
            user.checking_balance += amount

        db.session.commit()
        flash('Transaction successful.')

    return render_template('atm.html', user=user)


def create_user(pin, checking_balance, savings_balance):
    existing_user = User.query.filter_by(pin=pin).first()
    if existing_user:
        print(f"User with PIN {pin} already exists.")
        return

    user = User(pin=pin, checking_balance=checking_balance, savings_balance=savings_balance)
    db.session.add(user)
    db.session.commit()


# Create sample users
with app.app_context():
    if os.environ.get('FLASK_ENV') != 'production':  # Placeholder guardrail, ENV var not set in demo
        create_user('1234', 500, 1000)
        create_user('5678', 700, 2000)

if __name__ == '__main__':
    app.run(debug=True)
