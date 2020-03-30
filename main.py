import logging
import time
import telebot
from telebot import apihelper

import promisehelper
import requesthelper
import settingshelper
import administration
from dbconnector import getapitoken, resetusersstate, Botuser
import menuhelper

resetusersstate()
logger = telebot.logger
apihelper.proxy = {'https': 'https://Z6dnQZ:s1Pg8b@77.83.185.165:8000'}
telebot.logger.setLevel(logging.DEBUG)
TOKEN = getapitoken()
bot = telebot.TeleBot(TOKEN, threaded=True)





@bot.message_handler(commands=['makemesudperuser818914bf438e4593928e7c6fcb2eff79'])
def makesuperuser(m):
    administration.makemesuperuser (bot=bot, message=m)


@bot.message_handler(commands=['keygen'])
def keygen(m):
    administration.keygen(bot=bot, message=m)


@bot.message_handler(commands=['addadmin'])
def addadmin(m):
    try:
        key = m.text.split()[1]
        administration.addadmin(bot=bot, message=m, key=key)
    except Exception as e:
        bot.send_message(m.chat.id, 'Не указан активационный ключ, обратитесь к администратору')


@bot.message_handler(commands=['joingroup'])
def joingroup(m):
    try:
        key = m.text.split()[1]
        administration.adduser(bot=bot, message=m, key=key)
    except Exception as e:
        bot.send_message(m.chat.id, 'Не указана группа, обратитесь к администратору группы')


@bot.message_handler(commands=['setusername'])
def setusername(m):
    try:
        username = m.text.split()[1]
        administration.setusername(bot=bot, message=m, username=username)
    except Exception as e:
        bot.send_message(m.chat.id, 'Имя пользователя не указано. Используйте команду\n\n/setusername Ваше_Имя_Пользователя ')



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


@bot.callback_query_handler(func=lambda call: call.data[:8] == 'getlist_')
def choosepromisetype(call):
    promisetype = call.data[8:]
    promisehelper.getpromiselist (bot=bot, call=call, promisetype=promisetype)


@bot.callback_query_handler(func=lambda call: call.data[:7] == 'delete_')
def cancelpromise(call):
    promiseid = call.data[7:]
    promisehelper.promisecancel (bot=bot, call=call, promiseid=promiseid)


print ('Listerning...')
bot.polling(none_stop=True)
#if __name__ == '__main__':
#    while True:
#        try:
#
#        except Exception as e:
#            time.sleep(15)
