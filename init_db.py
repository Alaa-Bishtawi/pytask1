import mysql.connector
import constants
myCon = mysql.connector.connect(
    host=constants.DbHost,
    user=constants.DbUser,
    # password="dpass",
    database=constants.DbName)
mycur = myCon.cursor()
with open('schema.sql') as f:
    mycur.execute(f.read())

myCon.commit()
myCon.close()
