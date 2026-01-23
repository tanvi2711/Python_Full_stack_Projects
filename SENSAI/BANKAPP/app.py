from flask import *
import sqlite3
from datetime import datetime
app=Flask(__name__)
conn=sqlite3.connect("bank.db")
cur = conn.cursor()
cur.execute("create table if not exists accmaster(accno integer primary key autoincrement,name text,email text,mobile text,gender text,birthdate text,acctype text,balance real)");
cur.execute("create table if not exists Transactions(accno int,trans text,amount int,date_time text)");
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/checklogin",methods=['POST'])
def checklogin():
    userid=request.form['userid']
    password=request.form['password']
    if userid=='Tanvi' and password=='1234':
        return redirect("home")
    else:
        return "login Failed"
    
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/openaccount")
def openaccount():
    return render_template("openaccount.html")

@app.route("/openaccountsubmit",methods=['POST'])
def openaccountsubmit():
   Name=request.form['name']
   Email= request.form['email']
   Mobile= request.form['mobile']
   Gender=request.form['gender']
   Birthdate= request.form['bdate']
   Acctype= request.form['acctype']
   Balance= request.form['balance']

   conn=sqlite3.connect('bank.db')
   cur=conn.cursor()
   cur.execute("INSERT INTO accmaster(Name,Email,Mobile,Gender,Birthdate,Acctype,Balance) values(?,?,?,?,?,?,?)",[Name,Email,Mobile,Gender,Birthdate,Acctype,Balance])
   conn.commit()
   return render_template("newaccountsuccess.html")
@app.route("/allaccounts")
def allaccounts():
    conn=sqlite3.connect("bank.db")
    cur=conn.cursor()
    cur.execute("select * from accmaster")
    rows=cur.fetchall()
    return render_template("allaccounts.html",rows=rows)

@app.route("/searchaccounts",methods=['get','post'])
def searchaccounts():
    if request.method=='GET':
        return render_template("searchaccounts.html")
    if request.method=='POST':
        accno=request.form.get('search')
        conn=sqlite3.connect('bank.db')
        cur=conn.cursor()
        cur.execute("select * from accmaster where accno=?",[accno])
        row=cur.fetchone()
        return render_template("searchaccounts.html",row=row)
    
@app.route("/deposit",methods=['get','post'])
def deposit():
    if request.method=='GET':
        return render_template("deposit.html")

    if request.method=='POST':
        accno=request.form['accno']
        amount=request.form['amount']
        conn=sqlite3.connect('bank.db')
        cur=conn.cursor()
        cur.execute("select * from accmaster where accno=?",[accno])
        row=cur.fetchone()
        if row:
            cur.execute("update accmaster set balance=balance+? where accno=?",[amount,accno])
            current=datetime.now()
            current_date=current.strftime("%Y-%m-%d %H-%M-%S")
            cur.execute("insert into transactions values(?,?,?,?)",[accno,'deposit',amount,current_date])
            conn.commit()
            return render_template("deposit.html",msg="Amount Deposited Successfully")
        else:
            return render_template("deposit.html",msg="Account not found")


@app.route("/withdraw",methods=['get','post'])
def withdraw():
    if request.method=='GET':
        return render_template("withdraw.html")
    else:
        accno=request.form['accno']
        amount=int(request.form['amount'])
        conn=sqlite3.connect('bank.db')
        cur=conn.cursor()
        cur.execute("select * from accmaster where accno=?",[accno])
        row=cur.fetchone()
        if row:
            balance=row[7]
            if balance >= amount:
                cur.execute("update accmaster set balance=balance-? where accno=?",[amount,accno])
                current=datetime.now()
                current_date=current.strftime("%Y-%m-%d %H-%M-%S")
                cur.execute("insert into transactions values(?,?,?,?)",[accno,'withdraw',amount,current_date])
                conn.commit()
                return render_template("withdraw.html",msg="Amount Withdraw Successfully")
            else:
                return render_template("withdraw.html",msg="Insufficient Balance")
        else:
            return render_template("withdraw.html",msg="Account Not Found")        
@app.route("/statements",methods=['GET','POST'])
def statements():
    if request.method=="GET":
        return render_template("statement.html")
    if request.method=="POST":
        accno=request.form['accno']
        conn=sqlite3.connect("bank.db")
        cur=conn.cursor()
        cur.execute("SELECT * FROM transactions where accno=?",[accno])
        rows=cur.fetchall()
        print(rows)
        return render_template("statement.html",rows=rows)
@app.route('/logout')
def logout():
    return render_template('logout.html')



app.run(debug="on")