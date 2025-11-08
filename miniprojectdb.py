import sqlite3
from datetime import date
import random

conn = sqlite3.connect('projectsql.db')
c = conn.cursor()

# c.execute('''
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     first_name TEXT,
#     last_name TEXT,
#     role TEXT,
#     email TEXT,
#     phone INTEGER,
#     password TEXT
#           );
# ''')



# c.execute('''
# INSERT INTO users ( first_name, last_name,role, email, phone, password)
# VALUES ( ?, ?, ?, ?, ?,?)
# ''', ( 'Rajeev', 'P S','Admin', 'rajeev@example.com', 9876543210, 'mypassword123'))
# c.execute("""insert into users( first_name, last_name,role, email, phone, password)
# values(?,?,?,?,?,?) """,('sam','jhon','user','sam@gmail.com','2423423','sam@123'))
# c.execute(""" insert into users(first_name, last_name,role, email, phone, password)values(?,?,?,?,?,?)""",('saviar','cs','user','saviar@gmail.com','2423423','xaviar@123'))
# conn.commit()

# c.execute('''
# CREATE TABLE IF NOT EXISTS transactions (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id INTEGER,
#     account_id INTEGER,
#     amount REAL,
#     date DATE,
#     type TEXT,
#     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
#     FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
# );
# ''')

# c.execute('''
#  CREATE TABLE IF NOT EXISTS accounts (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id INTEGER,
#      balance REAL DEFAULT 0.0,
#      account_no TEXT UNIQUE,
#      type TEXT,
#      status TEXT,
#      created_at DATE,    
#      FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE);

#  ''')


def login(user):
    
    if not user:
       print("login failed ")
       return
    if user :
        print("Successfully Logged")
    while True:
        print("Enter options:\n 1. Withdraw Funds\n 2. Deposit\n 3. View Transactions\n 4. Main Menu")
        option = input("Enter choice: ")

        match option:
            case "1":
                withdraw(user)
            case "2":
                deposit(user)
            case "3":
                viewTransactions(user)
            case "4":
                 
                 print("Back to main menu...")
                 index()
                 
            case _:
                print(" Invalid option, please try again.")    

    
        

def withdraw(user):
    user_id = user[0]
    
    c.execute("""
        SELECT a.balance,user_id,a.id as account_id
        FROM accounts a
        INNER JOIN users u ON a.user_id = u.id
        WHERE u.id = ?
    """, (user_id,))
    record = c.fetchone()
    balance, user_id, account_id ,name = record
    print(f"Welcome {name} Your balance is: ₹{balance}")
    
    while True:
        amount = input("Enter amount to withdraw: ")
        if amount.isdigit():
            amount = float(amount)
            break
        else:
            print("Invalid amount..!  Please enter valid amount ")
     
    created = date.today().isoformat()
    if user and balance >= amount:
        created = date.today().isoformat()
        new_balance = balance - amount
        c.execute("UPDATE accounts SET balance = ? WHERE user_id = ?", (new_balance, user_id))
        c.execute("INSERT INTO transactions (account_id,user_id, type, amount,date) VALUES (?, ?,?,?, ?)", (account_id, user_id,"Withdraw",amount,created))
        conn.commit()
        print(f"₹{amount} withdrawn successfully. New balance: ₹{new_balance}")
       
    if user == "":
        print("user not exist")
    if balance < amount:
         print("Low Balance ")
         
    
    
    

def deposit(user):
    user_id = user[0]
    
    c.execute("""
        SELECT a.balance,user_id,a.id as account_id,u.first_name
        FROM accounts a
        INNER JOIN users u ON a.user_id = u.id
        WHERE u.id = ?
    """, (user_id,))
    record = c.fetchone()
    balance, user_id, account_id ,name = record
    print(f"Welcome {name} Your balance is: ₹{balance}")
    
    while True:
        amount = input("Enter amount to deposit: ")
        if amount.isdigit():
            amount = float(amount)
            break
        else:
            print("Invalid amount..!  Please enter valid amount ")
    if user and balance > 0:
        created = date.today().isoformat()
        new_balance = balance + amount
        c.execute("UPDATE accounts SET balance = ? WHERE user_id = ?", (new_balance, user_id))
        c.execute("INSERT INTO transactions (account_id,user_id, type, amount,date) VALUES (?, ?,?,?, ?)", (account_id, user_id,"Deposit",amount,created))
        conn.commit()
        print(f"₹{amount} Deposit successfully. New balance: ₹{new_balance}")
       
    if amount < 0:
         print("Amount must be greater than zero.")
         return
    
    

def viewTransactions(user):
    user_id = user[0]

   
    while True:
        print("\n View Transactions")
        print("1. All Transactions")
        print("2. Deposits Only")
        print("3. Withdrawals Only")
        print("4. Back to Menu")
        choice = input("Enter choice: ")

        
        if choice == "1":
            query = "SELECT type, amount, date FROM transactions WHERE user_id = ? ORDER BY date DESC"
            params = (user_id,)
        elif choice == "2":
            query = "SELECT type, amount, date FROM transactions WHERE user_id = ? AND type = 'Deposit' ORDER BY date DESC"
            params = (user_id,)
        elif choice == "3":
            query = "SELECT type, amount, date FROM transactions WHERE user_id = ? AND type = 'Withdraw' ORDER BY date DESC"
            params = (user_id,)
        elif choice == "4":
            break
        else:
            print(" Invalid choice.")
            return

        c.execute(query, params)
        records = c.fetchall()

        if not records:
            print(" No transactions found for this selection.")
            return

        print("\n=== Transaction History ===")
        print(f"{'Type':<12} {'Amount':<10} {'Date':<12}")
        print("-" * 40)

        for record in records:
            type,amount,date = record
            print(f"{type:<12} ₹{amount:<10} {date:<12}")
        
        print("-" * 40)
        

   
def checkEmail(new_email,c):
    c.execute("SELECT * FROM users WHERE email = ?", (new_email,))
    user = c.fetchone()  
    if user:
        print(" Email exists in database!")
        new_email = input("Enter  other email :")
        checkEmail(new_email)
    else:
        return new_email

def registerUser():
    conn = sqlite3.connect('projectsql.db')
    c = conn.cursor()
    name = input("Enter name :")
    lname = input("Enter last name : ")
    email = input("Enter email :")
    check_email =  c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()  # fetch one matching record
    email = checkEmail(email,c)
    
    
    while True:
        phone = input("Enter phone number :")
        if phone.isdigit() and len(phone) >= 4:
            break
        else:
            print("Invalid phone number. Please enter digits only (at least 10 digits).")
    
    while True:
        password = input("Enter password :")
        if len(password) >= 8:
            break
        else:
            print("Password must be 8 characters long).")
    cPassword = input("Enter confirm password :")
    if password != cPassword:    
        while True:
            
            if password != cPassword:
                print("confirm password not matching password!")
                cPassword = input("Enter confirm password :")
            else:
                break
    c.execute("""insert into users( first_name, last_name,role, email, phone, password)
    values(?,?,?,?,?,?) """,(name,lname,"User",email,phone,password))
    conn.commit()
   
    

    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    
    created_at = date.today().isoformat()
    user_id =  user[0]
    account_no = random.randint(10**10, (10**11) - 1)
    balance = 1000
    c.execute("""insert into accounts( user_id, balance,account_no, type, status, created_at)
    values(?,?,?,?,?,?) """,(user_id,balance,account_no,'Savings',"Active",created_at))
    conn.commit()
    print("User registered successfully..")   
        

def index():

    while True:
        print("\n=== Bank System ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        option = input("Enter choice:")

        match option:
            case "1":
                registerUser()
            case "2":
                email = input("Enter email :")
                password = input("Enter  password :")
                c.execute("SELECT * FROM users WHERE email = ? and password = ?", (email,password))
                user = c.fetchone()

                login(user)
            case "3":
                print(" Exiting system...")
                break
            case _:
                print(" Invalid option, please try again.")    
index()
       
    
   





    



