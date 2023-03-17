import sqlite3

def CreateBD():
    connect_db = sqlite3.connect('ToDoList.db')
    current_connect = connect_db.cursor()
    #current_connect.execute("DROP TABLE Business")
    current_connect.execute("CREATE TABLE IF NOT EXISTS Business ([id_business] INTEGER PRIMARY KEY, [date] TEXT, [time] TEXT, id_text INT, [text_business] TEXT, [id_user] INT)")
    connect_db.commit()
    
def FillDB(id, date, time, id_text, text_business, id_user):
    connect_db = sqlite3.connect('ToDoList.db')
    current_connect = connect_db.cursor()
    data = [(id, date, time, id_text, text_business, id_user)]
    current_connect.executemany("INSERT INTO Business(id_business, date, time, id_text, text_business, id_user) VALUES(?,?,?,?,?,?)", data)
    connect_db.commit()
    
def GetIDBusiness():
    connect_db = sqlite3.connect('ToDoList.db')
    current_connect = connect_db.cursor()
    current_connect.execute("SELECT id_business FROM Business ORDER BY id_business DESC LIMIT 1")
    count_number = current_connect.fetchall()
    if len(count_number):
        id = count_number[0][0] + 1
    else:
        id = 1
    return id

def SelectDB():
    connect_db = sqlite3.connect('ToDoList.db')
    current_connect = connect_db.cursor()
    current_connect.execute("SELECT * FROM Business")
    result = current_connect.fetchall()
    connect_db.commit()
    return result
    
def GetIDText(id_user):
    connect_db = sqlite3.connect('ToDoList.db')
    current_connect = connect_db.cursor()
    current_connect.execute("SELECT id_text FROM Business WHERE id_user = ? ORDER BY id_text DESC LIMIT 1",(id_user,))
    count_number = current_connect.fetchall()
    if len(count_number):
        count_number = count_number[0][0] + 1
    else:
        count_number = 1
    connect_db.commit()
    return count_number

def DeleteTheTask(id_user, id_text):
    connect_db = sqlite3.connect('ToDoList.db')
    current_connect = connect_db.cursor()
    current_connect.execute("DELETE FROM Business WHERE (id_user = ? AND id_text = ?)", (id_user, id_text,))
    current_connect.execute("SELECT id_text, id_business FROM Business WHERE id_user = ?", (id_user,))
    rows = current_connect.fetchall()
    for row in rows:
        id_business = row[1]
        if (row[0]>id_text):
            new_value = row[0] - 1
            current_connect.execute("UPDATE Business SET id_text = ? WHERE id_business = ?", (new_value, id_business,))
    connect_db.commit()
    

def DeleteDB(id_user):
    connect_db = sqlite3.connect('ToDoList.db')
    current_connect = connect_db.cursor()
    current_connect.execute("DELETE FROM Business WHERE id_user = ?", (id_user,))
    result = current_connect.fetchall()
    connect_db.commit()
    print(result)
    
def GetIDBusinessForSelect(id_user, id_text):
    connect_db = sqlite3.connect('ToDoList.db')
    current_connect = connect_db.cursor()
    current_connect.execute("SELECT id_business FROM Business WHERE id_user = ? AND id_text = ?", (id_user,id_text,))
    result = current_connect.fetchall()
    connect_db.commit()
    return result
    
def SelectTasks(id_user):
    connect_db = sqlite3.connect('ToDoList.db')
    current_connect = connect_db.cursor()
    current_connect.execute("SELECT date, time, id_text, text_business FROM Business WHERE id_user = ?", (id_user,))
    result = current_connect.fetchall()
    connect_db.commit()
    return result

def UpdateTaskText(id_user, id_text, text_business):
    connect_db = sqlite3.connect('ToDoList.db')
    current_connect = connect_db.cursor()
    current_connect.execute("UPDATE Business SET text_business = ? WHERE (id_user = ? AND id_text = ?)", (text_business, id_user, id_text,))
    #result = current_connect.fetchall()
    connect_db.commit()
    
def UpdateTaskDate(id_user, id_text, date):
    connect_db = sqlite3.connect('ToDoList.db')
    current_connect = connect_db.cursor()
    current_connect.execute("UPDATE Business SET date = ? WHERE (id_user = ? AND id_text = ?)", (date, id_user, id_text,))
    #result = current_connect.fetchall()
    connect_db.commit()
    
def UpdateTaskTime(id_user, id_text, time):
    connect_db = sqlite3.connect('ToDoList.db')
    current_connect = connect_db.cursor()
    current_connect.execute("UPDATE Business SET time = ? WHERE (id_user = ? AND id_text = ?)", (time, id_user, id_text,))
    #result = current_connect.fetchall()
    connect_db.commit()
