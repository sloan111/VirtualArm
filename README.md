# Virtual Automated Teller Machine (ATM)

This application simulates a virtual ATM, allowing users to interact with a web-based interface that emulates basic ATM functionalities such as login via a PIN, depositing funds, withdrawing funds, transferring between accounts, and logging out.

## Features

- **PIN Authentication**: Users can login using a 4 to 8 digit PIN.
- **Deposit**: Users can deposit money into their checking or savings account.
- **Withdraw**: Users can withdraw money from their checking or savings account.
- **Transfer**: Users can transfer money between their checking and savings accounts.
- **Logout**: Users can log out from their session.

## Requirements

- Python 3.7 or higher
- Flask
- SQLAlchemy
- SQLite

## Installation and Setup

1. Clone the repository

2.  Create a virtual environment and activate it:

    
    `python3 -m venv venv
    source venv/bin/activate` 
    
3.  Install the required packages:

    `pip install -r requirements.txt`

 4.   Run the application:

        `python app.py`

5. Visit `http://127.0.0.1:5000` in your web browser to interact with the application.

## ## Running Tests

You can run the automated tests by executing:

    `python test_app.py`

## ## Contributing

If you want to contribute, please fork the repository and create a pull request. Feel free to open an issue if you find a bug or have a feature request.