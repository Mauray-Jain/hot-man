from Server.database import *
from Server.tables import config

def handle(req, cnx, cursor):
    x = req["type"]
    if x == "Otp":
        return handleOtp(req["number"])
    elif x == "Database":
        return handleDB(cnx, cursor, req["query"])
    else:
        return -1

def handleDB(cnx, cursor, req):
    typeOfOperation = req["type"]
    table = req["table"]
    content = req["content"]
    if typeOfOperation == "Create":
        if createRecord(cnx, cursor, table, (), content) == -1:
            return -1
    elif typeOfOperation == "Read":
        if table == config["menu"]:
            menu = readMenu(cursor)
            return menu
        elif table == config["cart"]:
            cart = readCart(cursor, content["user"])
            return cart
    elif typeOfOperation == "Update":
        if table == config["cart"]:
            return updateCart(cnx, cursor, content)
    elif typeOfOperation == "Delete":
        return deleteRecord(cnx, cursor, table, content)
    else:
        return -1

def handleOtp(number):
    if len(str(number)) != 10:
        return -1
