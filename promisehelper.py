import datetime

import keyboards
from dbconnector import Botuser


def promisehandler(bot, message, action):
    keyboard = keyboards.getemptyinlinekeyboard()
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
            promisesender = promise[4]
            keyboard.add (keyboards.getpromsieinlinebutton(text=i, promiseid=promise_id, action=action))
            sendmessage = sendmessage + """\n{}. {}\nДата обещания: {}""".format(i, promisetext, promisedate)
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
    promisesender = promisedata[3]
    sendmessagetext = ('Обещание {}\n{}\nДата обещания: {}'.format(actiontomessage, promisetext, promisedate))
    user.promisefin (promiseid=promiseid, action=action)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=sendmessagetext)
    if promisesender != user.uid:
        bot.send_message(chat_id=promisesender, text=sendmessagetext)


def getsimlpepromiselist (type):
    pass
