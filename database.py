from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    account_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    username = db.Column(
        db.String(100),
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    balance = db.Column(
        db.Float,
        default=0.0
    )


class Transaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    account_number = db.Column(
        db.String(20),
        nullable=False
    )

    transaction_type = db.Column(
        db.String(50),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    description = db.Column(
        db.String(255)
    )

    date = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )