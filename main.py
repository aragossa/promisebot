import logging
import threading
import time

import schedule
import telebot



logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(botToken, threaded=True)

@bot.message_handler(commands=['start'])
def handleStart(m):
    pass

@bot.message_handler(content_types= 'text' )
def simpleTextMessage(m):
    pass



def checkNotifications ():
    pass

def updateNewNotifciations ():
    pass


def threadCheckNotifications():
    while True:
        schedule.run_pending()
        checkNotifications ()
        time.sleep(1)



def threadUpdateNotifications():
    while True:
        schedule.run_pending()
        updateNotifications()
        time.sleep(1)


th1 = threading.Thread(target=threadCheckNotifications, args=())
th1.start()


th2 = threading.Thread(target=threadUpdateNotifications, args=())
th2.start()


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(5)
