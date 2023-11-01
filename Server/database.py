import mysql.connector
from mysql.connector import errorcode
from tables import tables

config = {
    "user" : "root",
    "password" : "",
    "host" : "::1",
    "database" : "hotman"
}

def createTable(cursor, table_desc):
    try:
        cursor.execute(table_desc)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("existing")
        else:
            print(err.msg)

def createRecorcd(cnx, cursor, table_name, record):
    try:
        cursor.execute(f"insert into {table_name} values {record}");
        cnx.commit()
    except mysql.connector.errors.DataError:
        return -1
    return 0

cnx = mysql.connector.connect(user = config["user"], password = config["password"])
cursor = cnx.cursor()

try:
    cursor.execute(f"use {config["database"]}")
    cnx.database = config["database"]
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist, creating new")
        cursor.execute(f"create database {config["database"]}")
        cnx.database = config["database"]
    else:
        print(err)
        exit(1)

createRecorcd(cnx, cursor, "test", ("heee", "209"))
createTable(cursor, tables["menu"])

cursor.close()
cnx.close()
