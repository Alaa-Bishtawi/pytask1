import mysql.connector
myCon = mysql.connector.connect(
    host="localhost",
    user="root",
    # password="dpass",
    database="test")
mycur = myCon.cursor()
with open('schema.sql') as f:
    mycur.execute(f.read())

myCon.commit()
myCon.close()
