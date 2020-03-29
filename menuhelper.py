import datetime

from keyboards import getmainmenukeyboard
from dbconnector import Botuser
import requesthelper, promisehelper

activeusersstate = ['REQUEST_INPUT', 'REQUEST_INPUT_DATE', 'REQUEST_INPUT_DATE_INPUT','PROMISE_INPUT']


def sendmainmenu(bot, uid):
    user = Botuser(uid)
    if user.isauthorized():
        usertype = user.getusertype()
        keyboard = getmainmenukeyboard(usertype=usertype)
        bot.send_message(user.uid, 'Вы уже авторизованы', reply_markup=keyboard)
    else:
        bot.send_message(user.uid, 'Вы не авторизованы')


def textmessagehandle(bot, message):
    user = Botuser(message.chat.id)
    if user.isauthorized():
        if message.text == 'Запрос обещания':
            user.resetuserstate()
            requesthelper.senduserlist(bot=bot, message=message)
        elif message.text == 'Подтвердить выполнение':
            user.resetuserstate()
            promisehelper.promisehandler(bot=bot, message=message, action='promise_accept')
        elif message.text == 'Зафиксировать невыполнение':
            user.resetuserstate()
            promisehelper.promisehandler(bot=bot, message=message, action='promise_break')
        elif message.text == 'Актуальные обещания':
            user.resetuserstate()
        elif message.text == 'Монитор':
            user.resetuserstate()
        elif message.text == 'Настройки':
            if user.isadmin():
                user.resetuserstate()
            else:
                user.resetuserstate()
                bot.send_message(chat_id=user.uid, text='Доступ ограничен')
        elif user.getuserstate() in activeusersstate:
            inputvaluehandler(bot=bot, user=user, value=message.text)




def inputvaluehandler(bot, user, value):

    if user.getuserstate() == 'REQUEST_INPUT':
        selecteduser = user.getuserselecteduser()
        requestid = user.insertrequest(request=value, selecteduser=selecteduser)
        requesthelper.sendrequesttouser(bot=bot, selecteduser=selecteduser, requestid=requestid)
        user.resetuserstate()

    elif user.getuserstate() == 'REQUEST_INPUT_DATE':
        selecteduser = user.getuserselecteduser()
        user.insertrequest(request=value, selecteduser=selecteduser)
        bot.send_message (chat_id=user.uid, text='Введите дату (в формате ДД.ММ.ГГГГ)')
        user.updateuserstate('REQUEST_INPUT_DATE_INPUT')

    elif user.getuserstate() == 'REQUEST_INPUT_DATE_INPUT':
        requestid = user.getlastrequest()
        selecteduser = user.getuserselecteduser()
        try:
            if len(value) == 10:
                promisedate = datetime.datetime.strptime(value, '%d.%m.%Y') + datetime.timedelta(hours=12)
                user.updaterequestdate(promiseid=requestid, promisedate=promisedate)
                user.resetuserstate()
                requesthelper.sendrequesttouser(bot=bot, selecteduser=selecteduser, requestid=requestid)
            elif len(value) == 8:
                promisedate = datetime.datetime.strptime(value, '%d.%m.%y') + datetime.timedelta(hours=12)
                user.updaterequestdate(promiseid=requestid, promisedate=promisedate)
                user.resetuserstate()
                requesthelper.sendrequesttouser(bot=bot, selecteduser=selecteduser, requestid=requestid)
            else:
                bot.send_message(chat_id=user.uid, text='Неправильный формат даты. Введите дату (в формате ДД.ММ.ГГГГ)')
                user.updateuserstate('REQUEST_INPUT_DATE_INPUT')
        except ValueError:
            bot.send_message(chat_id=user.uid, text='Неправильный формат даты. Введите дату (в формате ДД.ММ.ГГГГ)')
            user.updateuserstate('REQUEST_INPUT_DATE_INPUT')

    elif user.getuserstate() == 'PROMISE_INPUT':
        requesthelper.promiseinput(bot=bot, user=user, value=value)


