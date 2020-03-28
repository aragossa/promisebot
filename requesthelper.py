from dbconnector import Botuser
import datetime

from keyboards import getrecipientrequestkeyboard, getgroupusersinlinekeyboard, getnodateinlinekeyboard, \
    getdateinlinekeyboard


def senduserlist(bot, message):
    keyboard = getgroupusersinlinekeyboard(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text='Выберите пользователя', reply_markup=keyboard)


def sendmessagetoinputvalue(bot, call, newstate, selecteduser=None):
    user = Botuser(call.message.chat.id)
    user.updateuserstate(newstate=newstate)
    if selecteduser:
        user.updateselecteduser(selecteduser)
    keyboard=getnodateinlinekeyboard()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите запрос', reply_markup=keyboard)


def changerequestdatestate(bot, call):
    user = Botuser(call.message.chat.id)
    keyboardtype = call.data[8:]
    if keyboardtype == 'nodate':
        user.updateuserstate('REQUEST_INPUT_DATE')
        keyboard = getdateinlinekeyboard()
    elif keyboardtype == 'addate':
        user.updateuserstate('REQUEST_INPUT')
        keyboard = getnodateinlinekeyboard()
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

def sendrequesttouser(bot, selecteduser, requestid):
    user = Botuser(selecteduser)
    requestdata = user.getrequestinfo(requestid=requestid)
    reqesttext = requestdata[0]
    try:
        reqestdate = datetime.datetime.strptime(requestdata[1], '%Y-%m-%d %H:%M:%S').strftime("%d.%m.%Y")
    except ValueError:
        reqestdate = requestdata[1]
    requestsender = Botuser(requestdata[2]).getusername()
    sendmessagetext = ('Запрос от {0}\n{1}\nДата обещания: {2}'.format (requestsender, reqesttext, reqestdate))
    keyboard = getrecipientrequestkeyboard(requestid=requestid)
    bot.send_message (chat_id=user.uid, text=sendmessagetext, reply_markup=keyboard)


def incomerequesthandler(bot, call):
    user=Botuser(call.message.chat.id)
    action = call.data[8:14]
    requestid = call.data[15:]
    if action == 'accept':
        requestaccept(user=user, requestid=requestid, call=call, bot=bot)
    elif action == 'reject':
        requestreject(user=user, requestid=requestid, call=call, bot=bot)


def requestaccept(user, requestid, call, bot):
    sendtext = ('Запрос принят\nВведите обещание:')
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=sendtext)
    user.updateuserstate('PROMISE_INPUT')
    user.updateselectedpromise(requestid)


def promiseinput(bot, user, value):
    selectedpromise = user.getuserselectedpromise()
    sendnotifidata = user.requestaccept(requestid=selectedpromise, promisetext=value)
    requestrecipient = sendnotifidata[0]
    requestsender = sendnotifidata[1]
    promisetext = sendnotifidata[2]
    sendtext = ('Новое обещание:\n{}'.format(promisetext))
    bot.send_message(chat_id=user.uid, text=sendtext)
    if requestsender != requestrecipient:
        bot.send_message(chat_id=requestsender, text=sendtext)
    user.resetuserstate()


def requestreject(user, requestid, call, bot):
    sendnotifidata = user.requestreject(requestid=requestid)
    requestrecipient = sendnotifidata[0]
    requestsender = sendnotifidata[1]
    requesttext = sendnotifidata[2]
    sendtext = ('Отклонен запрос:\n{}'.format(requesttext))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=sendtext)
    if requestsender != requestrecipient:
        bot.send_message (chat_id=requestsender, text=sendtext)


