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

def deleteRecord(cnx, cursor, table, record):
    cursor.execute(f"delete from {table} where id = {record['id']}")
    cnx.commit()

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
    cursor.execute("select category, name, rate, id from menu where quantity_available > 0")
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

def clearCart(cnx, cursor):
    cursor.execute("select id from cart")
    earlier = cursor.fetchone()
    if earlier is not None:
        cursor.execute("delete from cart")
        cnx.commit()

def updateCart(cnx, cursor, record):
    try:
        cursor.execute(f"select category, name, rate, quantity from cart where user = {record['user']}")
    except KeyError:
        print("No number")
        return -1
    output = cursor.fetchall()
    names = [i[0] for i in menu]
    categories = [i[1] for i in menu]
    rates = [i[2] for i in menu]
    id = names.index(record["name"])

    if record["name"] not in names:
        return -1

    if "id" not in record:
        record["id"] = id + 1
    if "category" not in record:
        record["category"] = categories[id]
    if "quantity" not in record:
        record["quantity"] = 1
    if "rate" not in record:
        record["rate"] = rates[id]

    if output == []:
        if createRecord(cnx, cursor, "cart", (), record) == -1:
            print("Error in creating cart")
            return -1
        return 0

    namesInCart = [i[1] for i in output]
    print("cart:", namesInCart)
    if record["name"] in namesInCart:
        cursor.execute(f"update cart set quantity = quantity + {record['quantity']} where id = {record['id']}")
        cnx.commit()
    else:
        if createRecord(cnx, cursor, "cart", (), record) == -1:
            print("Error adding record")
            return -1
    return 0

def readCart(cursor, user):
    cursor.execute(f"select category, name, rate, quantity, id from cart where user = {user} and quantity > 0")
    output = cursor.fetchall()
    if output == []:
        return -1
    obj = {}
    for i in output:
        i = list(i)
        if i[0] not in obj:
            obj[i[0]] = []
        obj[i[0]].append(i[1:])
    obj["Total"] = getTotal(cursor, user)
    return obj

def getTotal(cursor, user):
    cursor.execute(f"select rate, quantity from cart where user = {user}")
    output = cursor.fetchall()
    if output == []:
        return 0
    else:
        sum = 0
        for i in output:
            sum += i[0] * i[1]
        return sum
