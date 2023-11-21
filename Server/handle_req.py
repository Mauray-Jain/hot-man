from Server.database import *
from Server.tables import config

def handle(req, cnx, cursor):
    if req["type"] == "Database":
        return handleDB(cnx, cursor, req["query"])
    else:
        return -1

def handleDB(cnx, cursor, req):
    try:
        typeOfOperation = req["type"]
        table = req["table"]
        content = req["content"]
        if typeOfOperation == "Create":
            if createRecord(cnx, cursor, table, (), content) == -1:
                return -1
        elif typeOfOperation == "Read":
            if table == "menu":
                menu = readMenu(cursor)
                return menu
            elif table == "cart":
                cart = readCart(cursor, content["user"])
                return cart
            else:
                return -1
        elif typeOfOperation == "Update":
            if table == "cart":
                return updateCart(cnx, cursor, content)
            elif table == "orders":
                return placeOrder(cursor, cnx, content["user"])
            else:
                return -1
        elif typeOfOperation == "Delete":
            return deleteRecord(cnx, cursor, table, content)
        else:
            return -1
    except:
        return -1
