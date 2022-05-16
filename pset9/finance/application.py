#ver confirmação
import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from pytz import timezone #get easy timezone(need to install in terminal, but not cs50)

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    cash = db.execute("SELECT cash FROM users WHERE id =?", session["user_id"])

    finance = db.execute("SELECT symbol, name, shares, price, total, idStock FROM company INNER JOIN stock ON stock.idCompany = company.idCompany WHERE action='buy' AND idUser =?", session["user_id"])
    #checking if the shares purchased have the same price and joining them if necessary, avoiding redundancies in display
    delet = []
    for i in range(len(finance)):
        for j in range(len(finance)):
            if finance[i]['price'] == finance[j]['price'] and finance[i]['symbol'] == finance[j]['symbol']: #finding the duplicates
                if finance[i]['idStock'] != finance[j]['idStock'] and i < j: #ensure will not count the same duplicates
                    finance[i]['shares'] += finance[j]['shares']
                    finance[i]['total'] += finance[j]['total']
                    if j not in delet:
                        delet.append(j)

    print(delet)
    #deleting the duplicates
    j = 0
    for i in delet:
        if j == 0:
            del finance[i]
        else:
            del finance[i-1]
        j += 1

    #updating with sells
    rowsell = db.execute("SELECT symbol, shares, total FROM stock INNER JOIN company ON company.idCompany = stock.idCompany WHERE action='sell' AND idUser = ?", session["user_id"])
    print(rowsell)
    i = -1
    for f in finance:
        i += 1
        for s in rowsell:
            if f['symbol'] == s['symbol']:
                if s['shares'] <= -f['shares']:
                    del finance[i]
                else:
                    f['shares'] += s['shares']

                f['total'] -= s['total']

    #get total of stocks, if there is none, display the cash only
    total = 0
    for f in finance:
        total += f['total']

    if total == 0:
        total = usd(cash[0]['cash'])
    else:
        total = usd(total+cash[0]['cash'])

    #transforming the values into dollars
    for row in finance:
        row['price'] = usd(row['price'])
        row['total'] = usd(row['total'])
    cash = usd(cash[0]['cash'])

    return render_template("index.html", finance = finance, total = total, cash = cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        #get the informations
        userCash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        company = lookup(request.form.get("symbol"))
        share = request.form.get("shares")
        if not company:
            return apology("Symbol error")
        elif share.isdigit() == False or not share:
            return apology("Invalid value")

        total = int(share)*company['price'] #the total price of the shares
        if total > userCash[0]['cash']: #checking if the user have enough money to buy all the share wanted
            return apology("you don't have enough money for that")

        #verifying if the symbol is already in db
        db_symbol = db.execute("SELECT symbol FROM company")
        found = False
        for row in db_symbol:
            if company['symbol'] == row['symbol']:
                found = True

        #if don't, insert
        if found == False:
            db.execute("INSERT INTO company (symbol, name) VALUES (?, ?)", company['symbol'], company['name'])

        #updating cash
        userCash = userCash[0]['cash'] - total

        share = int(share)
        date = datetime.now() #in server timezone
        date = date.strftime('%m/%d/%Y %H:%M') #text formatting to keep organized
        #insertting information into the database
        comp = db.execute("SELECT idCompany FROM company WHERE symbol = ?", company['symbol'])
        db.execute("INSERT INTO stock (idUser, idCompany, shares, price, total, date, action) VALUES (?, ?, ?, ?, ?, ?, ?)", session["user_id"], comp[0]['idCompany'], share, company['price'], total, date, "buy")
        db.execute("UPDATE users SET cash = ? WHERE id = ?", userCash, session['user_id'])

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    finance = db.execute("SELECT symbol, shares, price, date FROM stock INNER JOIN company ON stock.idCompany = company.idCompany")

    return render_template("history.html", finance = finance)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT id, hash FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username was submitted and isn't in use
        if not request.form.get("username"):
            return apology("must provide a valid username", 403)

        #ensure it is registered
        if len(rows) != 1 :
            return apology("must register")

        # Ensure password was submitted and match
        if not request.form.get("password") or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Incorrect password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        result = lookup(request.form.get("symbol"))

        if not result:
            return apology("Symbol error")

        return render_template("quoted.html", result = result, price = usd(result['price']))

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    #User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        db_username = db.execute("SELECT username FROM users")
        hashPass = generate_password_hash(password = request.form.get("password"), method='pbkdf2:sha256')
        user = request.form.get("username")

        #Ensure username was submitted
        if not user:
            return apology("must provide username", 400)

        #Ensure username don't already exists
        for row in db_username:
            if user == row['username']:
                return apology("username already exists")

        #Ensure password was submitted and match
        if not hashPass or not request.form.get("confirmation") or request.form.get("password") != request.form.get("confirmation"):
            return apology("the password needs to match", 400)

        #Ensure password is secure
        if len(request.form.get("password")) < 8 or len(re.findall(r"[0-9]", request.form.get("password"))) < 1 or len(re.findall(r"[A-Z]", request.form.get("password"))) < 1:
            return apology("Invalid password")

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", user, hashPass)

        rows = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    symbol = db.execute("SELECT symbol FROM company ORDER BY symbol")

    if request.method == "POST":
        sell_symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        #checking if the user has shares
        idCompany = db.execute("SELECT idCompany FROM company WHERE symbol = ?", sell_symbol)
        ushare = db.execute("SELECT SUM(shares) FROM stock WHERE idCompany = ? AND idUser = ? AND action = 'buy'", idCompany[0]["idCompany"], session["user_id"])#getting the shares that user owns
        if shares < '1' or not shares:
            return apology("Invalid value")
        elif ushare[0]['SUM(shares)'] == None or str(ushare[0]['SUM(shares)']) < shares: #checking if the user owns sufficient shares to sell
            return apology("You don't have enough shares for that")

        #insertting into the db
        shares = int(shares)
        price = lookup(request.form.get("symbol"))
        total = shares*price['price']
        shares *= -1 #tranforming the shares in "debit"
        date = datetime.now() #in server timezone
        date = date.strftime('%m/%d/%Y %H:%M') #text formatting to keep organized
        db.execute("INSERT INTO stock (idUser, idCompany, shares, price, total, date, action) VALUES (?, ?, ?, ?, ?, ?, ?)", session["user_id"], idCompany[0]["idCompany"], shares, price['price'], total, date, 'sell')

        #updating the user's cash
        cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
        cash = cash[0]['cash'] + total
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session['user_id'])
        return redirect("/")
    else:
        return render_template("sell.html", symbol = symbol)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)