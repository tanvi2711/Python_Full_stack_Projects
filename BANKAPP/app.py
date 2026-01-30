from flask import *
import sqlite3
from datetime import datetime

app = Flask(__name__)

# DB init
conn = sqlite3.connect("bank.db")
cur = conn.cursor()

cur.execute("""
create table if not exists accmaster(
    accno integer primary key autoincrement,
    name text,
    email text,
    mobile text,
    gender text,
    birthdate text,
    acctype text,
    balance real
)
""")

cur.execute("""
create table if not exists Transactions(
    accno int,
    trans text,
    amount real,
    date_time text
)
""")

conn.commit()
conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/checklogin", methods=['POST'])
def checklogin():
    userid = request.form['userid']
    password = request.form['password']
    if userid == 'bank_admin' and password == '12345':
        return redirect("home")
    else:
        return "login Failed"


@app.route("/home")
def home():
    conn = sqlite3.connect("bank.db")
    cur = conn.cursor()

    cur.execute("select count(*) from accmaster")
    totalacc = cur.fetchone()[0]

    # 🔥 FIX: handle NULL sum
    cur.execute("select sum(balance) from accmaster")
    totaldeposit = cur.fetchone()[0] or 0

    current = datetime.now()
    current_date = current.strftime("%Y-%m-%d")
    cur.execute(
        "select count(*) from transactions where date_time like ?",
        [current_date + '%']
    )
    dailytran = cur.fetchone()[0]

    conn.close()
    return render_template(
        "home.html",
        totalacc=totalacc,
        totaldeposit=totaldeposit,
        dailytran=dailytran
    )


@app.route("/openaccount")
def openaccount():
    return render_template("openaccount.html")


@app.route("/openaccountsubmit", methods=['POST'])
def openaccountsubmit():
    Name = request.form['name']
    Email = request.form['email']
    Mobile = request.form['mobile']
    Gender = request.form['gender']
    Birthdate = request.form['bdate']
    Acctype = request.form['acctype']

    # 🔥 FIX: convert to float
    Balance = float(request.form['balance'])

    conn = sqlite3.connect('bank.db')
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO accmaster(Name,Email,Mobile,Gender,Birthdate,Acctype,Balance) values(?,?,?,?,?,?,?)",
        [Name, Email, Mobile, Gender, Birthdate, Acctype, Balance]
    )
    conn.commit()
    conn.close()

    return render_template("newaccountsuccess.html")


@app.route("/allaccounts")
def allaccounts():
    conn = sqlite3.connect("bank.db")
    cur = conn.cursor()
    cur.execute("select * from accmaster")
    rows = cur.fetchall()
    conn.close()
    return render_template("allaccounts.html", rows=rows)


@app.route("/searchaccounts", methods=['GET', 'POST'])
def searchaccounts():
    if request.method == 'GET':
        return render_template("searchaccounts.html")

    accno = request.form.get('search')
    conn = sqlite3.connect('bank.db')
    cur = conn.cursor()
    cur.execute("select * from accmaster where accno=?", [accno])
    row = cur.fetchone()
    conn.close()
    return render_template("searchaccounts.html", row=row)


@app.route("/deposit", methods=['GET', 'POST'])
def deposit():
    if request.method == 'GET':
        return render_template("deposit.html")

    accno = request.form['accno']

    # 🔥 FIX: convert to float
    amount = float(request.form['amount'])

    conn = sqlite3.connect('bank.db')
    cur = conn.cursor()

    cur.execute("select * from accmaster where accno=?", [accno])
    row = cur.fetchone()

    if row:
        cur.execute(
            "update accmaster set balance = balance + ? where accno=?",
            [amount, accno]
        )

        current = datetime.now()
        current_date = current.strftime("%Y-%m-%d %H-%M-%S")

        cur.execute(
            "insert into transactions values(?,?,?,?)",
            [accno, 'deposit', amount, current_date]
        )

        conn.commit()
        conn.close()
        return render_template("deposit.html", msg="Amount Deposited Successfully")

    conn.close()
    return render_template("deposit.html", msg="Account not found")


@app.route("/withdraw", methods=['GET', 'POST'])
def withdraw():
    if request.method == 'GET':
        return render_template("withdraw.html")

    accno = request.form['accno']
    amount = float(request.form['amount'])

    conn = sqlite3.connect('bank.db')
    cur = conn.cursor()

    cur.execute("select * from accmaster where accno=?", [accno])
    row = cur.fetchone()

    if row:
        balance = row[7]
        if balance >= amount:
            cur.execute(
                "update accmaster set balance = balance - ? where accno=?",
                [amount, accno]
            )

            current = datetime.now()
            current_date = current.strftime("%Y-%m-%d %H-%M-%S")

            cur.execute(
                "insert into transactions values(?,?,?,?)",
                [accno, 'withdraw', amount, current_date]
            )

            conn.commit()
            conn.close()
            return render_template("withdraw.html", msg="Amount Withdraw Successfully")
        else:
            conn.close()
            return render_template("withdraw.html", msg="Insufficient Balance")

    conn.close()
    return render_template("withdraw.html", msg="Account Not Found")


@app.route("/statements", methods=['GET', 'POST'])
def statements():
    if request.method == "GET":
        return render_template("statement.html")

    accno = request.form['accno']
    conn = sqlite3.connect("bank.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions where accno=?", [accno])
    rows = cur.fetchall()
    conn.close()
    return render_template("statement.html", rows=rows)


@app.route('/logout')
def logout():
    return render_template('logout.html')


app.run(debug=True)
