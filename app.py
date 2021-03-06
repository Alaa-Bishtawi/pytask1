import datetime
import logging
from urllib import request

from flask import Flask
from flask import request

from models import Link

logging.basicConfig(filename='server.log',
                    encoding='utf-8', level=logging.DEBUG)
app = Flask(__name__)


@app.errorhandler(Exception)
def page_not_found(e):
    return str(e)


def my_decorator(func):
    # print("inside decorater")

    def wrapperInner():
        logging.info(str(datetime.datetime.now()), +' Function ' + func.__name__ +
                     ' Called ')
        result = func()
        # print("Something is happening after the function is called.")
        return result

    return wrapperInner


@app.route('/show_urls', methods=['GET'], endpoint='showUrls')
@my_decorator
def showUrls():
    link = Link()
    logging.info(' Get Request  /show_urls at  ' +
                 str(datetime.datetime.now()) + ' And returned All Urls ')
    return link.showUrls()


@app.route('/show_urls_order', methods=['GET'], endpoint='showUrlsOrderd')
@my_decorator
def showUrlsOrderd():
    orderType = request.args.get("orderType")
    link = Link()
    logging.info(' Get Request  /show_urls_order at  ' +
                 str(datetime.datetime.now()) + ' And returned All Urls orderd')

    return link.showUrlsOrderd(orderType)


@app.route('/show_urls_Json', methods=['GET'], endpoint='showUrlsJson')
@my_decorator
def showUrlsJson():
    link = Link()
    logging.info(' Get Request  /show_urls_Json at  ' +
                 str(datetime.datetime.now()) + ' And returned All Urls As Jsoon')
    return link.showUrlsJson()


@app.route('/full_url', methods=['GET'], endpoint='check_full_url')
@my_decorator
def check_full_url():
    short_url = request.args.get("url")
    short_url = short_url.split("/")[-1:][0]
    link = Link()
    original_url = link.CheckExsistUrl(short_url)
    logging.info(' Get Request  /full_url at  ' + str(datetime.datetime.now()
                                                      ) + ' And returned full url url is : ' + original_url)

    return original_url


@app.route('/short_url', methods=['POST'], endpoint='short_url')
@my_decorator
def short_url():
    original_url = request.form.get('original_url')
    link = Link()
    short_url = link.ShortenUrl(original_url)
    short_url = link.server_url + short_url
    logging.info(' POST Request  /short_url at  ' + str(datetime.datetime.now()
                                                        ) + ' And returned short url is : ' + short_url)

    return short_url


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello World!'


@app.route('/get', methods=['GET'])
def get_hello_world():
    return 'Get Hello World!'


if __name__ == '__main__':
    app.run()
