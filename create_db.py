import sqlite3

connection = sqlite3.connect('control.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS USERS (id INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT); ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS COSTS
                (cost_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT,
                Price float,
                cost_date date,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES USERS(id));''')   # CREATE COSTS Table
if not list(cursor.execute('''SELECT * FROM USERS WHERE Username='Andrew' ''')):
    cursor.execute('''INSERT INTO USERS(Username) VALUES ('Andrew')''')
connection.commit()
connection.close()
