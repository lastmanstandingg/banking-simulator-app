from flask import Flask, render_template, request, redirect, session, flash
from database import db, User, Transaction
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_hex(32)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banking.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        account_number = "SIM" + secrets.token_hex(4).upper()

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            account_number=account_number,
            password=hashed_password,
            balance=0.0
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!")

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        account_number = request.form["account_number"]

        password = request.form["password"]

        user = User.query.filter_by(
            account_number=account_number
        ).first()

        if user and check_password_hash(user.password, password):

            session.clear()

            session["user_id"] = user.id

            return redirect("/dashboard")

        flash("Invalid login credentials")

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    user = db.session.get(User, session["user_id"])

    return render_template(
        "dashboard.html",
        user=user
    )


# DEPOSIT
@app.route("/deposit", methods=["GET", "POST"])
def deposit():

    if "user_id" not in session:
        return redirect("/login")

    user = db.session.get(User, session["user_id"])

    if request.method == "POST":

        amount = float(request.form["amount"])

        if amount > 0 and amount <= 1000000:

            user.balance += amount

            transaction = Transaction(
                account_number=user.account_number,
                transaction_type="Deposit",
                amount=amount,
                description="Virtual cash deposit"
            )

            db.session.add(transaction)
            db.session.commit()

            flash("Deposit successful!")

        else:
            flash("Invalid deposit amount")

        return redirect("/dashboard")

    return render_template("deposit.html")


# WITHDRAW
@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():

    if "user_id" not in session:
        return redirect("/login")

    user = db.session.get(User, session["user_id"])

    if request.method == "POST":

        amount = float(request.form["amount"])

        if amount > 0 and amount <= user.balance:

            user.balance -= amount

            transaction = Transaction(
                account_number=user.account_number,
                transaction_type="Withdrawal",
                amount=amount,
                description="Virtual cash withdrawal"
            )

            db.session.add(transaction)
            db.session.commit()

            flash("Withdrawal successful!")

        else:
            flash("Insufficient balance or invalid amount")

        return redirect("/dashboard")

    return render_template("withdraw.html")


# TRANSACTION HISTORY
@app.route("/transactions")
def transactions():

    if "user_id" not in session:
        return redirect("/login")

    user = db.session.get(User, session["user_id"])

    records = Transaction.query.filter_by(
        account_number=user.account_number
    ).order_by(Transaction.date.desc()).all()

    return render_template(
        "transactions.html",
        records=records
    )


# LOGOUT
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

from decimal import Decimal, InvalidOperation

@app.route("/transfer", methods=["GET", "POST"])
def transfer():

    if "user_id" not in session:
        return redirect("/login")

    user = db.session.get(User, session["user_id"])

    if request.method == "POST":

        recipient_account = request.form["recipient_account"].strip()

        try:
            amount = Decimal(request.form["amount"])

            if not amount.is_finite() or amount <= 0:
                raise InvalidOperation

            if amount.as_tuple().exponent < -2:
                raise InvalidOperation

        except InvalidOperation:
            flash("Enter a valid transfer amount.")
            return redirect("/transfer")

        recipient = User.query.filter_by(
            account_number=recipient_account
        ).first()

        if not recipient:
            flash("Recipient account does not exist.")

        elif recipient.id == user.id:
            flash("You cannot transfer money to yourself.")

        elif amount > Decimal(str(user.balance)):
            flash("Insufficient balance.")

        else:
            user.balance = float(Decimal(str(user.balance)) - amount)

            recipient.balance = float(
                Decimal(str(recipient.balance)) + amount
            )

            db.session.add(Transaction(
                account_number=user.account_number,
                transaction_type="Transfer Sent",
                amount=float(amount),
                description=f"Transfer to {recipient.account_number}"
            ))

            db.session.add(Transaction(
                account_number=recipient.account_number,
                transaction_type="Transfer Received",
                amount=float(amount),
                description=f"Transfer from {user.account_number}"
            ))

            db.session.commit()

            flash("Virtual transfer completed successfully!")

            return redirect("/dashboard")

    return render_template("transfer.html", user=user)

@app.route("/admin")
def admin():

    if "user_id" not in session:
        return redirect("/login")

    admin_user = db.session.get(User, session["user_id"])

    # Add a proper admin role check here before deployment.
    if not admin_user or not getattr(admin_user, "is_admin", False):
        return "Access denied", 403

    users = User.query.all()

    transactions = Transaction.query.order_by(
        Transaction.date.desc()
    ).limit(50).all()

    return render_template(
        "admin.html",
        users=users,
        transactions=transactions
    )


if __name__ == "__main__":
    app.run(debug=True)