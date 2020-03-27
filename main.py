import logging
import threading
import time

import schedule
import telebot
import dbhelper

helper = dbhelper
TOKEN = helper.getapitoken()
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(TOKEN, threaded=True)


@bot.message_handler(commands=['start'])
def handlestart(m):
    pass


@bot.message_handler(content_types='text')
def simpletextmessage(m):
    pass


def checknotifications():
    pass


def updatenewnotifciations():
    pass


def threadchecknotifications():
    while True:
        schedule.run_pending()
        checknotifications()
        time.sleep(1)


def threadupdatenotifications():
    while True:
        schedule.run_pending()
        updatenewnotifciations()
        time.sleep(1)

if __name__ == '__main__':
    th1 = threading.Thread(target=threadchecknotifications(), args=())
    th1.start()

    th2 = threading.Thread(target=threadupdatenotifications(), args=())
    th2.start()

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(5)
