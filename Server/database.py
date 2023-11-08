import mysql.connector
from mysql.connector import errorcode
from Server.tables import menu

def createDB(cnx, cursor, database):
    try:
        cursor.execute(f"use {database}")
        cnx.database = database
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist, creating new")
            cursor.execute(f"create database {database}")
            cnx.database = database
        else:
            print(err)
            exit(1)

def createTable(cursor, table_desc):
    try:
        cursor.execute(table_desc)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("existing")
        else:
            print(err.msg)

def createRecord(cnx, cursor, table_name, fields, values):
    if fields == ():
        fields = tuple(values.keys())
        values = tuple(values.values())
    if len(fields) != len(values):
        return -1
    fields = str(fields).replace("'", "")
    try:
        cursor.execute(f"insert into {table_name} {fields} values {values}")
        cnx.commit()
    except mysql.connector.errors.DataError:
        return -1
    return 0

def createMenu(cnx, cursor):
    cursor.execute("select id from menu where id=1")
    earlier_menu = cursor.fetchone()
    if earlier_menu is not None:
        return
    for i in menu:
        if createRecord(cnx, cursor, "menu", ("name", "category", "rate", "quantity_available"), i) == -1:
            print("Error creating menu")
            exit(1)

def readMenu(cursor):
    cursor.execute("select category, name, rate from menu where quantity_available > 0")
    output = cursor.fetchall()
    if output == []:
        return -1
    obj = {}
    for i in output:
        i = list(i)
        if i[0] not in obj:
            obj[i[0]] = []
        obj[i[0]].append(i[1:])
    return obj

def updateCart(cnx, cursor, record):
    cursor.execute("select category, name, rate, quantity from cart")
    output = cursor.fetchall()
    print(output)
    if "quantity" not in record:
        record["quantity"] = 1
    if output == []:
        print("Record:", record)
        if createRecord(cnx, cursor, "cart", (), record) == -1:
            print("what tha")
        print("here")
        return
    names = []
    for i in output:
        names.append(i[1])
    if record["name"] in names:
        cursor.execute(f"update cart set quantity = quantity + 1 where name = '{record['name']}'")
        cnx.commit()
    else:
        createRecord(cnx, cursor, "cart", (), record)

def getTotal(cursor):
    cursor.execute("select rate, quantity from cart")
    output = cursor.fetchall()
    if output == []:
        return 0
    else:
        sum = 0
        for i in output:
            sum += i[0] * i[1]
        return sum
