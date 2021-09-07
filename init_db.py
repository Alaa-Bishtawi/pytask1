import mysql.connector

import constants

myCon = mysql.connector.connect(
    host=constants.DB_HOST,
    user=constants.DB_USER,
    # password= constants.DB_PASSWORD,
    database=constants.DB_NAME)
mycur = myCon.cursor()
with open('schema.sql') as f:
    mycur.execute(f.read())

myCon.commit()
myCon.close()
