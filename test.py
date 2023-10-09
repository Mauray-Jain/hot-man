from sqlite3 import DatabaseError
import mysql.connector

cnx = mysql.connector.connect(user = "root", password = "MJ#LovesMysql", host = "127.0.0.1", database = "hotman")
cnx.close()
