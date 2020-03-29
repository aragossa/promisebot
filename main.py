import logging
import time
import telebot
from telebot import apihelper

import promisehelper
import requesthelper
import settingshelper
from dbconnector import getapitoken, resetusersstate
import menuhelper

resetusersstate()
logger = telebot.logger
apihelper.proxy = {'https': 'https://Z6dnQZ:s1Pg8b@77.83.185.165:8000'}
telebot.logger.setLevel(logging.DEBUG)
TOKEN = getapitoken()
bot = telebot.TeleBot(TOKEN, threaded=True)


@bot.message_handler(commands=['start'])
def handlestart(m):
    menuhelper.sendmainmenu (bot=bot, uid=m.chat.id)


@bot.message_handler(content_types='text')
def simpletextmessage(m):
    menuhelper.textmessagehandle(bot=bot, message=m)


@bot.callback_query_handler(func=lambda call: call.data[:7] == 'select_')
def sendmessagetoinputvalue(call):
    selecteduser = call.data[7:]
    requesthelper.sendmessagetoinputvalue (bot=bot, call=call, newstate='REQUEST_INPUT', selecteduser=selecteduser)


@bot.callback_query_handler(func=lambda call: call.data[:8] == 'request_')
def requesthandler(call):
    action = call.data[8:14]
    if action == 'nodate' or action == 'addate':
        requesthelper.changerequestdatestate (bot=bot, call=call)
    elif action == 'accept' or action == 'reject':
        requesthelper.incomerequesthandler(bot=bot, call=call)


@bot.callback_query_handler(func=lambda call: call.data[:8] == 'promise_')
def requesthandlerfin(call):
    action = call.data.split('_')[1]
    promsieid = call.data.split('_')[2]
    promisehelper.promisehandlerfin(bot, call, action, promsieid)


@bot.callback_query_handler(func=lambda call: call.data[:4] == 'new_')
def updatesettings(call):
    parameter = call.data[4:]
    settingshelper.updatesetttings(bot=bot, call=call, parameter=parameter)



@bot.callback_query_handler(func=lambda call: call.data == 'reset')
def resetstatistics(call):
    settingshelper.resetstatistics (bot=bot, call=call)


print ('Listerning...')
bot.polling(none_stop=True)
#if __name__ == '__main__':
#    while True:
#        try:
#
#        except Exception as e:
#            time.sleep(15)
