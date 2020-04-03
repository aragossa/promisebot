import datetime

import keyboardhelper
from dbconnector import Botuser


def promisehandler(bot, message, action):
    keyboard = keyboardhelper.getemptyinlinekeyboard()
    user = Botuser(message.chat.id)
    promises = user.getactivepromisesme()
    if promises:
        sendmessage = 'Выберите общеание:'
        i = 1
        for promise in promises:
            promise_id = promise[0]
            promiserequest =promise[1]
            promisetext = promise[2]
            try:
                promisedate = datetime.datetime.strptime(promise[3], '%Y-%m-%d %H:%M:%S').strftime("%d.%m.%Y")
            except ValueError:
                promisedate = promise[3]
            promisesender = Botuser(promise[4])
            promisesendername = promisesender.getusername()
            keyboard.add (keyboardhelper.getpromsieinlinebutton(text=i, promiseid=promise_id, action=action))
            sendmessage = sendmessage + """\n{}. {}\nОт: {}\nДата обещания: {}""".format(i, promisetext, promisesendername, promisedate)
            i += 1
        bot.send_message (chat_id=message.chat.id, text=sendmessage, reply_markup=keyboard)
    else:
        bot.send_message(chat_id=message.chat.id, text='Активных обещаний нет')


def promisehandlerfin(bot, call, action, promiseid):
    user = Botuser(call.message.chat.id)
    promisedata = user.getrequestinfo(requestid=promiseid)
    promisetext = promisedata[1]
    try:
        promisedate = datetime.datetime.strptime(promisedata[2], '%Y-%m-%d %H:%M:%S').strftime("%d.%m.%Y")
    except ValueError:
        promisedate = promisedata[2]
    if action == 'accept':
        actiontomessage = 'выполнено'
    elif action == 'break':
        actiontomessage = 'нарушено'
    promisesender = promisedata[4]
    sendmessagetext = ('Обещание {}\n{}\nДата обещания: {}'.format(actiontomessage, promisetext, promisedate))
    user.promisefin (promiseid=promiseid, action=action)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=sendmessagetext)
    if promisesender != user.uid:
        bot.send_message(chat_id=promisesender, text=sendmessagetext)


def choosepromiselisttype (bot, message):
    user = Botuser(message.chat.id)
    keyboard = keyboardhelper.getchoosepromisetypekeyboard()
    bot.send_message(chat_id=message.chat.id, text='Выберите обещания', reply_markup=keyboard)


def getpromiselist(bot, call, promisetype):
    user = Botuser(call.message.chat.id)
    print (promisetype)
    if promisetype == 'promiseme':
        promiselist = user.getactivepromisesme()
        #id, request_text, promise_text, promise_date, user_id_give
        sendmessage = 'Обещания мне\n'
    elif promisetype == 'promisemy':
        promiselist = user.getactivepromisesmy()
        #id, request_text, promise_text, promise_date, user_id_get
        sendmessage = 'Я обещал:\n'
    elif promisetype == 'request':
        promiselist = user.getununsweredrequestsme()
        keyboard = keyboardhelper.getemptyinlinekeyboard()
        #id, request_text, promise_text, promise_date, user_id_give
        sendmessage = 'Неотвеченные запросы\n'

    if promiselist:
        i = 1
        for promise in promiselist:
            if promisetype == 'request':
                promisetext = promise[1]
            else:
                promisetext = promise[2]

            try:
                promisedate = datetime.datetime.strptime(promise[3], '%Y-%m-%d %H:%M:%S').strftime("%d.%m.%Y")
            except ValueError:
                promisedate = promise[3]

            promisesender = Botuser(promise[4])
            promisesendername = promisesender.getusername()
            if promisetype == 'request' or promisetype == 'promisemy':
                sendmessage = sendmessage + """\n{}. {}\nКому: {}\nДата обещания: {}""".format(i, promisetext,
                                                                                         promisesendername, promisedate)

            elif promisetype == 'promiseme':
                sendmessage = sendmessage + """\n{}. {}\nОт: {}\nДата обещания: {}""".format(i, promisetext,
                                                                                               promisesendername,
                                                                                               promisedate)

            if promisetype == 'request':
                keyboard.add(keyboardhelper.getpromsieinlinebutton('delete', promise[0], i))
            i += 1
        if promisetype == 'request':
            sendmessage = sendmessage + '\n\nВыберите номер запроса для удаления'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=sendmessage, reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=sendmessage)
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Ничего нет')


def promisecancel(bot, call, promiseid):
    user = Botuser(call.message.chat.id)
    user.promisecancel(promiseid)
    getpromiselist(bot, call, 'request')