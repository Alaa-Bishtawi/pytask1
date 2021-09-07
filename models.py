import hashlib
import json
import logging
import random
import re
import string
from datetime import date

import mysql.connector

import constants

logging.basicConfig(filename='server.log',
                    encoding='utf-8', level=logging.DEBUG)


class Link():
    server_url = constants.SERVER_URL

    def __init__(self):
        try:

            self.myCon = mysql.connector.connect(
                host=constants.DB_HOST,
                user=constants.DB_USER,
                # password="dpass",
                database=constants.DB_NAME)

        except mysql.connector.Error as err:
            logging.error("Something went wrong: {}".format(err))

    def checkDuplicateShorten(self, short_url):
        """   Check database if shorten url exists before  """
        state = False
        try:
            mycursor = self.myCon.cursor()

            mycursor.execute(
                f"SELECT * FROM urls  WHERE short_url ='{short_url}'")

            mycursor.fetchall()
            if mycursor.rowcount == 0:

                state = True
            else:

                state = False

        except:
            state = None
        finally:
            mycursor.close()
            return state

    def isValidURL(self, str):
        """  check given url if valid """
        regex = ("((http|https)://)(www.)?" +
                 "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                 "{2,256}\\.[a-z]" +
                 "{2,6}\\b([-a-zA-Z0-9@:%" +
                 "._\\+~#?&//=]*)")
        p = re.compile(regex)
        if (re.search(p, str)):
            return True
        else:
            return False

    def AddShortenedUrl(self, original_url, short_url):
        """ add record to database  """

        state = False
        try:
            mycursor = self.myCon.cursor()

            today = date.today()
            tdate = today.strftime("%Y/%d/%m")

            print(tdate)
            sql_insert_query = f"insert into urls (original_url, short_url, RegDate) values ('{original_url}','{short_url}','{tdate}')"

            mycursor.execute(sql_insert_query)
            self.myCon.commit()

            state = True
            logging.info('Here is inserted quey ' + sql_insert_query)
        except mysql.connector.Error as error:
            state = False

        finally:
            mycursor.close()
            if state == True:
                return short_url
            else:
                logging.error("Erorr While Inserting Url")
                return "Erorr While Inserting Url"

    def CheckExsistUrl(self, short_url):
        mycursor = self.myCon.cursor()

        mycursor.execute(
            f"SELECT original_url, short_url FROM urls  WHERE short_url ='{short_url}'")

        myRecordset = mycursor.fetchall()
        if mycursor.rowcount == 0:
            mycursor.close()
            logging.error("no such exissting website")
            return "no such exissting website"
        else:
            original_url = myRecordset[0][0]
            mycursor.close()
            return original_url

    def ShortenUrl(self, original_url):

        vaild = self.isValidURL(original_url)
        if vaild != True:
            logging.error("404 The Url Not Valid")
            return "404 The Url Not Valid"
        letters = string.ascii_letters
        short_url = str(
            int(hashlib.sha1(original_url.encode("utf-8")).hexdigest(), 16) % (10 ** 6))

        random_value = ''.join(random.choice(letters) for i in range(6))
        temp = short_url + random_value
        duplicated = self.checkDuplicateShorten(
            temp)  # if duplicated -- return false
        while duplicated == False:
            random_value = ''.join(random.choice(letters) for i in range(6))
            temp = short_url + random_value
            duplicated = self.checkDuplicateShorten(temp)

        return self.AddShortenedUrl(original_url, temp)

    def showUrlsOrderd(self, orderType):
        """get all api urls orderd """
        mycursor = self.myCon.cursor()
        mycursor.execute(
            f"SELECT original_url, short_url, RegDate FROM urls ORDER BY RegDate {{orderType}} ")  # ASC or DESC
        myRecordset = mycursor.fetchall()
        mycursor.close()
        return str(myRecordset)

    def showUrls(self):
        """ get all api urls as string without any ordering """

        try:
            mycursor = self.myCon.cursor()
            mycursor.execute(
                "SELECT original_url, short_url, RegDate FROM urls ")
            myRecordset = mycursor.fetchall()
            mycursor.close()
            return str(myRecordset)

        except mysql.connector.Error as err:
            logging.error("Something went wrong: {}".format(err))
            print("Something went wrong: {}".format(err))

    def showUrlsJson(self):
        """ get all api urls as json file """

        mycursor = self.myCon.cursor()

        mycursor.execute("SELECT original_url, short_url, RegDate FROM urls ")
        myRecordset = mycursor.fetchall()
        json_data = []
        row_headers = [x[0] for x in mycursor.description]
        for r in myRecordset:
            json_data.append(dict(zip(row_headers, r)))

        mycursor.close()
        return json.dumps(json_data)
