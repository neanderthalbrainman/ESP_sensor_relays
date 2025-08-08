import mysql.connector
import sys


def SubmitToDB(temp:int, hum:int, loc:str, time:str):
    myDB = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="user",
        password="<<>>",
        database="sensors"
    )

    #print(myDB)

    mycursor = myDB.cursor()

    sql = "INSERT INTO sensorsdata (temp, hum, loc, time) VALUES (%s, %s, %s, %s)"
    val = (int(temp), int(hum), loc, time)
    mycursor.execute(sql, val)

    myDB.commit()

    print(mycursor.rowcount, "record inserted")
