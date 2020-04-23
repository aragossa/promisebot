import logging

import telebot

import likeshelper
import promisehelper
import requesthelper
import settingshelper
import administration
from dbconnector import getapitoken, resetusersstate, Botuser
import menuhelper

resetusersstate()
logging.basicConfig(
    filename='promisebot_exceptions.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = telebot.logger
#apihelper.proxy = {'https': 'https://Z6dnQZ:s1Pg8b@77.83.185.165:8000'}

telebot.logger.setLevel(logging.INFO)
TOKEN = getapitoken()
bot = telebot.TeleBot(TOKEN, threaded=True)


@bot.message_handler(commands=['makemesudperuser818914bf438e4593928e7c6fcb2eff79'])
def makesuperuser(m):
    try:
        administration.makemesuperuser(bot=bot, message=m)
    except:
        logging.debug(m)
        logging.exception('Got exception on main handler')
        bot.send_message(m.chat.id, 'Что-то пошло не так')


@bot.message_handler(commands=['keygen'])
def keygen(m):
    try:
        administration.keygen(bot=bot, message=m)
    except:
        logging.debug(m)
        logging.exception('Got exception on main handler')
        bot.send_message(m.chat.id, 'Что-то пошло не так')




@bot.message_handler(commands=['addadmin'])
def addadmin(m):
    try:
        key = m.text.split()[1]
        administration.addadmin(bot=bot, message=m, key=key)
    except Exception as e:
        logging.debug(m)
        logging.exception('Got exception on main handler')
        bot.send_message(m.chat.id, 'Не указан активационный ключ, обратитесь к администратору')


@bot.message_handler(commands=['joingroup'])
def joingroup(m):
    try:
        key = m.text.split()[1]
        administration.adduser(bot=bot, message=m, key=key)
    except:
        logging.debug(m)
        logging.exception('Got exception on main handler')
        bot.send_message(m.chat.id, 'Не указана группа, обратитесь к администратору группы')


@bot.message_handler(commands=['setusername'])
def setusername(m):
    try:
        username = m.text.split()[1]
        administration.setusername(bot=bot, message=m, username=username)
    except:
        logging.debug(m)
        logging.exception('Got exception on main handler')
        bot.send_message(m.chat.id,
                         'Имя пользователя не указано. Используйте команду\n\n/setusername Ваше_Имя_Пользователя ')


@bot.message_handler(commands=['start'])
def handlestart(m):
    try:
        menuhelper.sendmainmenu(bot=bot, uid=m.chat.id)
    except:
        logging.debug(m)
        logging.exception('Got exception on main handler')
        bot.send_message(m.chat.id, 'Что-то пошло не так')


@bot.message_handler(content_types='text')
def simpletextmessage(m):
    try:
        menuhelper.textmessagehandle(bot=bot, message=m)
    except:
        logging.debug(m)
        logging.exception('Got exception on main handler')
        bot.send_message(m.chat.id, 'Что-то пошло не так')


@bot.callback_query_handler(func=lambda call: call.data[:7] == 'select_')
def sendmessagetoinputvalue(call):
    try:
        selecteduser = call.data[7:]
        requesthelper.sendmessagetoinputvalue(bot=bot, call=call, selecteduser=selecteduser)
    except:
        logging.debug(call)
        logging.exception('Got exception on main handler')
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')


@bot.callback_query_handler(func=lambda call: call.data[:8] == 'request_')
def requesthandler(call):
    try:
        action = call.data[8:14]
        if action == 'nodate' or action == 'addate':
            requesthelper.changerequestdatestate(bot=bot, call=call)
        elif action == 'accept' or action == 'reject':
            requesthelper.incomerequesthandler(bot=bot, call=call)
    except:
        logging.debug(call)
        logging.exception('Got exception on main handler')
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')


@bot.callback_query_handler(func=lambda call: call.data[:8] == 'promise_')
def requesthandlerfin(call):
    try:
        action = call.data.split('_')[1]
        promsieid = call.data.split('_')[2]
        promisehelper.promisehandlerfin(bot, call, action, promsieid)
    except:
        logging.debug(call)
        logging.exception('Got exception on main handler')
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')


@bot.callback_query_handler(func=lambda call: call.data[:4] == 'new_')
def updatesettings(call):
    try:
        parameter = call.data[4:]
        settingshelper.updatesetttings(bot=bot, call=call, parameter=parameter)
    except:
        logging.debug(call)
        logging.exception('Got exception on main handler')
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')


@bot.callback_query_handler(func=lambda call: call.data == 'reset')
def resetstatistics(call):
    try:
        settingshelper.resetstatistics(bot=bot, call=call)
    except:
        logging.debug(call)
        logging.exception('Got exception on main handler')
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')


@bot.callback_query_handler(func=lambda call: call.data[:8] == 'getlist_')
def choosepromisetype(call):
    try:
        promisetype = call.data[8:]
        promisehelper.getpromiselist(bot=bot, call=call, promisetype=promisetype)
    except:
        logging.debug(call)
        logging.exception('Got exception on main handler')
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')

@bot.callback_query_handler(func=lambda call: call.data[:7] == 'delete_')
def cancelpromise(call):
    try:
        promiseid = call.data[7:]
        promisehelper.promisecancel(bot=bot, call=call, promiseid=promiseid)
    except:
        logging.debug(call)
        logging.exception('Got exception on main handler')
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')


@bot.callback_query_handler(func=lambda call: call.data[:6] == 'likes_')
def cancelpromise(call):
    try:
        action = call.data[6:]
        likeshelper.likeshandler(bot=bot, call=call, action=action)
    except:
        logging.debug(call)
        logging.exception('Got exception on main handler')
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')


print('Listerning...')
bot.polling(none_stop=True)