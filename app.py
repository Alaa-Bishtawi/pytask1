import datetime
from urllib import request
import logging
from flask import request
from models import Link
from flask import Flask

logging.basicConfig(filename='server.log', encoding='utf-8', level=logging.DEBUG)
app = Flask(__name__)


@app.route('/show_urls', methods=['GET'])
def showUrls():
    link = Link()
    logging.info(' Get Request  /show_urls at  ' + str(datetime.datetime.now()) + ' And returned All Urls ' )
    return link.showUrls()


@app.route('/show_urls_ASC', methods=['GET'])
def showUrlsAsc():
    link = Link()
    logging.info(' Get Request  /show_urls_ASC at  ' + str(datetime.datetime.now()) + ' And returned All Urls Asending' )

    return link.showUrlsAsc()


@app.route('/show_urls_Json', methods=['GET'])
def showUrlsJson():
    link = Link()
    logging.info(' Get Request  /show_urls_Json at  ' + str(datetime.datetime.now()) + ' And returned All Urls As Jsoon' )
    return link.showUrlsJson()


@app.route('/full_url', methods=['GET'])
def check_full_url():
    short_url = request.args.get("url")
    short_url = short_url.split("/")[-1:][0]
    link = Link()
    original_url = link.CheckExsistUrl(short_url)
    logging.info(' Get Request  /full_url at  ' + str(datetime.datetime.now()) + ' And returned full url url is : ' + original_url )

    return original_url


########################


@app.route('/short_url', methods=['POST'])
def short_url():
    original_url = request.form.get('original_url')

    # characters = string.digits + string.ascii_letters
    # # short_url = ''.join(choices(characters, k=8))
    # short_url = ''.join(choices(characters, k=8))
    # print(characters)
    link = Link()
    short_url = link.ShortenUrl(original_url)
    short_url = link.server_url + short_url
    logging.info(' POST Request  /short_url at  ' + str(datetime.datetime.now()) + ' And returned short url is : ' + short_url )

    return short_url


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # link = Link()
    # url = 'www.facebook.com'
    # link.ShortenUrl(url)
    # print('finished adding')
    # link.showUrls()
    # print(link.CheckExsistUrl('qZVq'))

    return 'Hello World!'


@app.route('/get', methods=['GET'])
def get_hello_world():
    return 'Get Hello World!'


if __name__ == '__main__':

    app.run()
