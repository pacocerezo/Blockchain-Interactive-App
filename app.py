from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from blockchain import Transaction, Block, Blockchain

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///blockchain.db")

# Start Blockchain
cs50chain = Blockchain()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    response.headers["SameSite"] = "None"
    response.headers["Secure"] = True
    return response


@app.route("/")
def index():

    # Render template
    return render_template("index.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    # User reached route via POST
    if request.method == "POST":

        # Get active user address
        user = db.execute("SELECT username FROM wallets WHERE id = ?", session.get("user_id"))

        # Get amount from form
        amount = int(request.form.get('amount'))

        # Register tx in the blockchain
        cs50chain.createTx(Transaction('treasury', user[0]['username'], amount))

        flash("Coins buyed!")

        # Render template
        return redirect("/mine")


    # User reached route via GET
    else:
        # Render template
        return render_template("buy.html")


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():

    # User reached route via POST
    if request.method == "POST":

        # Redirect to restart blockchain link
        return redirect("/restart")

    # User reached route via GET
    else:

        # Existing wallets
        wallets = db.execute("SELECT * FROM wallets")

        # Update their balances in the db from the blockchain
        for wallet in wallets:
            address = wallet['address']
            bal = cs50chain.getBalance(address)
            db.execute("UPDATE wallets SET balance = ? WHERE address = ?", bal, address)

        # Updated wallets to show balance in web app
        wallets = db.execute("SELECT * FROM wallets")

        # Render template
        return render_template("dashboard.html", blocks=cs50chain.chain, wallets=wallets)


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM wallets WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash('INVALID USERNAME AND/OR PASSWORD')
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to homepage
        return redirect("/dashboard")

    # User reached route via GET
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/transactions", methods=["GET", "POST"])
@login_required
def transactions():

    # User reached route via POST
    if request.method == "POST":

        # Get sender address (active user)
        user = db.execute("SELECT username FROM wallets WHERE id = ?", session.get("user_id"))
        user_address = user[0]['username']

        # Get tx receiver from form
        receiver = request.form.get('receiver')

        # Get ammount from form
        amount = int(request.form.get('amount'))

        # Check for funds availability
        if cs50chain.getBalance(user_address) < amount:
            flash("NOT ENOUGH FUNDS")
            return render_template("transactions.html")

        # Check for existing wallet
        c = 0
        addresses = db.execute("SELECT address FROM wallets")
        for address in addresses:
            if receiver in address.values():
                c += 1
        if c == 0:
            flash("WALLET DOESN'T EXIST")
            return render_template("transactions.html")

        # Register tx in the blockchain
        cs50chain.createTx(Transaction(user_address, receiver, amount))

        flash("Transaction created!")

        return redirect('/mine')

    # User reached route via GET
    else:
        return render_template("transactions.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST
    if request.method == "POST":

        # Check for errors
        if request.form.get("password") != request.form.get("confirmation"):
            flash("PASSWORDS DON'T MATCH")
            return render_template("registration.html")

        # Get password hash
        hashed = generate_password_hash(request.form.get("password"))

        # Add user to database
        try:
            db.execute("INSERT INTO wallets (username, hash, address) VALUES (:username, :hash, :address)",
                    username=request.form.get("username"),
                    hash=hashed,
                    address=request.form.get("address"))
            return redirect('/')
        except:
            flash("USERNAME ALREADY REGISTERED")
            return render_template("registration.html")


    # User reached route via GET
    else:
        return render_template("registration.html")


@app.route("/mine", methods=["GET", "POST"])
@login_required
def mine():
    # User reached route via POST
    if request.method == "POST":

        # Mine block with pending transactions
        cs50chain.minePendingTx('miner')

        flash("Block mined!")

        # Redirect to dashboard
        return redirect("/dashboard")

    # User reached route via GET
    else:

        # Render pending transactions
        return render_template("pending-tx.html", pending=cs50chain.pendingTx)


@app.route("/restart", methods=["GET", "POST"])
@login_required
def restart():
    # User reached route via POST
    if request.method == "POST":

        # Restart blockchain to genesis block
        cs50chain.chain = [
            Block([], "0" * 64)
        ]

        flash("Blockchain restarted!")

        # Redirect to dashboard
        return redirect("/dashboard")

    # User reached route via GET
    else:
        return render_template("restart.html")