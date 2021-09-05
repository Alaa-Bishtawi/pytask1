import hashlib
import json
import random
import re
import string
from datetime import date
import mysql.connector
import constants

class Link():
    server_url = constants.server_url

    def __init__(self):
        try:
            self.myCon = mysql.connector.connect(
                host=constants.DbHost,
                user=constants.DbUser,
                # password="dpass",
                database=constants.DbName )

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

    def checkDuplicateShorten(self, short_url):
        """
                    Check database if shorten url exists before
                    """
        state = False
        try:
            mycursor = self.myCon.cursor()

            mycursor.execute(f"SELECT * FROM urls  WHERE short_url ='{short_url}'")

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
        """
                    check given url if valid
                    """
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
        """
                    add record to database
                    """
        state = False
        try:
            mycursor = self.myCon.cursor()

            today = date.today()
            tdate = today.strftime("%Y/%d/%m")

            print(tdate)
            sql_insert_query = f"insert into urls (original_url, short_url, RegDate) values ('{original_url}','{short_url}','{tdate}')";

            mycursor.execute(sql_insert_query)
            self.myCon.commit();

            state = True
        except mysql.connector.Error as error:
            state = False

        finally:
            mycursor.close()
            if state == True:
                return short_url
            else:
                return "Erorr While Inserting Url"

    def CheckExsistUrl(self, short_url):
        mycursor = self.myCon.cursor()

        mycursor.execute(f"SELECT original_url, short_url FROM urls  WHERE short_url ='{short_url}'")

        myRecordset = mycursor.fetchall()
        if mycursor.rowcount == 0:
            mycursor.close()
            return "no such exissting website"
        else:
            original_url = myRecordset[0][0]
            mycursor.close()
            return original_url

    def ShortenUrl(self, original_url):

        vaild = self.isValidURL(original_url)
        if vaild != True:
            return "The Url Not Valid"
        letters = string.ascii_letters
        short_url = str(int(hashlib.sha1(original_url.encode("utf-8")).hexdigest(), 16) % (10 ** 6))

        random_value = ''.join(random.choice(letters) for i in range(6))
        temp = short_url + random_value
        duplicated = self.checkDuplicateShorten(temp) # if duplicated -- return false
        while duplicated == False:
            random_value = ''.join(random.choice(letters) for i in range(6))
            temp = short_url + random_value
            duplicated = self.checkDuplicateShorten(temp)

        return self.AddShortenedUrl(original_url, temp)

    def showUrlsOrderd(self,orderType):
        """
            get all api urls orderd
            """
        #Var
        mycursor = self.myCon.cursor()
        mycursor.execute(f"SELECT original_url, short_url, RegDate FROM urls ORDER BY RegDate {{orderType}} ")  # ASC or DESC
        myRecordset = mycursor.fetchall()
        mycursor.close()
        return str(myRecordset)


    def showUrls(self):
        """
            get all api urls as string without any ordering
            """
        try:
            mycursor = self.myCon.cursor()
            mycursor.execute("SELECT original_url, short_url, RegDate FROM urls ")
            myRecordset = mycursor.fetchall()
            mycursor.close()
            return str(myRecordset)

        except mysql.connector.Error as err:

            print("Something went wrong: {}".format(err))

    def showUrlsJson(self):
        """
            get all api urls as json file
            """
        mycursor = self.myCon.cursor()

        mycursor.execute("SELECT original_url, short_url, RegDate FROM urls ")

        myRecordset = mycursor.fetchall()
        json_data = []
        row_headers = [x[0] for x in mycursor.description]  # this will extract row headers
        for r in myRecordset:
            json_data.append(dict(zip(row_headers, r)))

        mycursor.close()
        return json.dumps(json_data)

    def my_decorator(self,func):

        def wrapper():
            print(" My function name ")
           # print("Something is happening before the function is called.")
            result = func()
            print("Something is happening after the function is called.")
            return result

        return wrapper




    #
    # def GetRowsNumber(self):
    #     mycursor = self.myCon.cursor()
    #
    #     mycursor.execute("SELECT Count(*) FROM urls ")
    #
    #     myRecordset = mycursor.fetchall()
    #     mycursor.close()
    #     return myRecordset[0][0]

    # Function to validate URL
    # using regular expression
    # def ShortenUrl(self, original_url):
    #     # app.config['SECRET_KEY'] = 'this should be a secret random string'
    #     #
    #     # hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])
    #     # hashids = Hashids(min_length=4, salt= 'this should be a secret random string')
    #     vaild = self.isValidURL(original_url)
    #     if vaild != True:
    #         return "The Url Not Valid"
    #     original_url_id = self.GetRowsNumber() + 1
    #     url_length = len(original_url)
    #     url_sum = 0
    #
    #     for i in range(url_length):
    #         url_sum += ord(original_url[i])
    #     print(url_sum)
    #
    #     # print(url_id)
    #
    #     hashid = hashids.encode(original_url_id)
    #     # print(hashid)
    #     # short_url = "http://127.0.0.1:5000/" + hashid
    #     short_url = hashid
    #     return self.AddShortenedUrl(original_url, short_url)
    #     # print(short_url)
