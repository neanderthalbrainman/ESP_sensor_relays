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
    try:
        tempCast = int(temp)
        humCast = int(hum)
    except ValueError:
        print("Couldn't cast to int")
        return

    sql = "INSERT INTO sensorsdata (temp, hum, loc, time) VALUES (%s, %s, %s, %s)"
    val = (int(temp), int(hum), loc, time)
    
        
    try:
        mycursor.execute(sql, val)
        myDB.commit()
    except BaseException as e:
        print("Error writing to DB: ", e)
        print("DATA:", temp, hum, loc, time)
        print (type(temp))
        print(type(hum))
        print(type(loc))
        print(type(time))
        print("not a valid datapoint, omitting")
        return
    finally:
        mycursor.close()
    print(mycursor.rowcount, "record inserted")
