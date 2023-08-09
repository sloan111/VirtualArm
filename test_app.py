import unittest
from app import app, db, User


class TestATM(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_atm.db'
        with app.app_context():
            db.create_all()
            cls.user = cls.create_user('1234', 5000, 1000)

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    @staticmethod
    def create_user(pin, checking_balance, savings_balance):
        existing_user = User.query.filter_by(pin=pin).first()
        if existing_user:
            print(f"User with PIN {pin} already exists.")
            return existing_user

        user = User(pin=pin, checking_balance=checking_balance, savings_balance=savings_balance)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def login_test_user(self):
        response = self.app.post('/', data={'pin': '1234'}, follow_redirects=True)
        return response

    def test_login(self):
        response = self.login_test_user(self)
        self.assertIn(b'ATM Dashboard', response.data)

    def test_invalid_login(self):
        response = self.app.post('/', data={'pin': '12ABKDSDF3456'}, follow_redirects=True)
        self.assertIn(b'Invalid PIN', response.data)

    def test_unregistered_login(self):
        response = self.app.post('/', data={'pin': '9999'}, follow_redirects=True)
        self.assertIn(b'PIN not found', response.data)

    def test_deposit(self):
        self.login_test_user(self)

        # Make a deposit to the checking account
        response = self.app.post(f'/atm/{self.user.id}', data={
            'amount': 100,
            'action': 'deposit_checking'
        }, follow_redirects=True)

        self.assertIn(b'Transaction successful', response.data)

    def test_withdraw(self):
        self.login_test_user(self)

        # Make a withdrawal from the checking account
        response = self.app.post(f'/atm/{self.user.id}', data={
            'amount': 100,
            'action': 'withdraw_checking'
        }, follow_redirects=True)

        self.assertIn(b'Transaction successful', response.data)

    def test_overdraw_withdraw(self):
        self.login_test_user(self)

        # Make a withdrawal from the checking account
        response = self.app.post(f'/atm/{self.user.id}', data={
            'amount': 55555,
            'action': 'withdraw_checking'
        }, follow_redirects=True)

        self.assertIn(b'Insufficient funds', response.data)

    def test_transfer(self):
        # Log in the test user
        self.app.post('/', data={'pin': '1234'})

        # Make a transfer from the checking to the savings account
        response = self.app.post(f'/atm/{self.user.id}', data={
            'amount': 100,
            'action': 'transfer_checking_savings'
        }, follow_redirects=True)

        self.assertIn(b'Transaction successful', response.data)

    def test_invalid_transfer(self):
        # Log in the test user
        self.app.post('/', data={'pin': '1234'})

        # Make a transfer from the checking to the savings account
        response = self.app.post(f'/atm/{self.user.id}', data={
            'amount': 999999,
            'action': 'transfer_savings_checking'
        }, follow_redirects=True)

        self.assertIn(b'Insufficient funds.', response.data)


if __name__ == '__main__':
    unittest.main()
