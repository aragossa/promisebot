import datetime

import likeshelper
import monitorhelper
import settingshelper
from keyboardhelper import getmainmenukeyboard
from dbconnector import Botuser
import requesthelper, promisehelper

activeusersstate = ['REQUEST_INPUT',
                    'REQUEST_INPUT_DATE',
                    'REQUEST_INPUT_DATE_INPUT',
                    'PROMISE_INPUT',
                    'REJECT_REQUEST',
                    'COMPLITE_PROMISE',
                    'BREAK_PROMISE',
                    'SEND_LIKE',
                    'SEND_DISLIKE']


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
            requesthelper.requesthandler(bot=bot, message=message)
        elif message.text == '👍': # like
            likeshelper.likeshandler (bot=bot, message=message, action='like')
        elif message.text == '👎': # dislike
            likeshelper.likeshandler (bot=bot, message=message, action='dislike')
        elif message.text == 'Подтвердить выполнение':
            user.resetuserstate()
            promisehelper.promisehandler(bot=bot, message=message, action='promise_accept')
        elif message.text == 'Зафиксировать невыполнение':
            user.resetuserstate()
            promisehelper.promisehandler(bot=bot, message=message, action='promise_break')
        elif message.text == 'Актуальные обещания':
            user.resetuserstate()
            promisehelper.choosepromiselisttype(bot=bot, message=message)
        elif message.text == 'Монитор':
            user.resetuserstate()
            monitorhelper.monitor(bot=bot, message=message)
        elif message.text == 'Настройки':
            if user.isadmin():
                user.resetuserstate()
                settingshelper.settingsmenu(bot=bot, message=message)
            else:
                user.resetuserstate()
                bot.send_message(chat_id=user.uid, text='Доступ ограничен')
        elif user.getuserstate() in activeusersstate:
            inputvaluehandler(bot=bot, user=user, value=message.text)




def inputvaluehandler(bot, user, value):

    if user.getuserstate() == 'REQUEST_INPUT':
        selecteduser = user.getuserselecteduser()
        requestid = user.insertrequest(request=value, selecteduser=selecteduser)
        requesthelper.sendrequesttouser(bot=bot, selecteduser=selecteduser, requestid=requestid, act_user=user)
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
                requesthelper.sendrequesttouser(bot=bot, selecteduser=selecteduser, requestid=requestid, act_user=user)
            elif len(value) == 8:
                promisedate = datetime.datetime.strptime(value, '%d.%m.%y') + datetime.timedelta(hours=12)
                user.updaterequestdate(promiseid=requestid, promisedate=promisedate)
                user.resetuserstate()
                requesthelper.sendrequesttouser(bot=bot, selecteduser=selecteduser, requestid=requestid, act_user=user)
            else:
                bot.send_message(chat_id=user.uid, text='Неправильный формат даты. Введите дату (в формате ДД.ММ.ГГГГ)')
                user.updateuserstate('REQUEST_INPUT_DATE_INPUT')
        except ValueError:
            bot.send_message(chat_id=user.uid, text='Неправильный формат даты. Введите дату (в формате ДД.ММ.ГГГГ)')
            user.updateuserstate('REQUEST_INPUT_DATE_INPUT')


    elif user.getuserstate() == 'PROMISE_INPUT':
        requesthelper.promiseinput(bot=bot, user=user, value=value)
        user.resetuserstate()


    elif user.getuserstate() == 'PROMISE_INPUT':
        requesthelper.promiseinput(bot=bot, user=user, value=value)
        user.resetuserstate()


    elif user.getuserstate() == 'SEND_LIKE':
        likeshelper.sendlikes (bot=bot, user=user, value=value)


    elif user.getuserstate() == 'SEND_DISLIKE':
        likeshelper.sendlikes(bot=bot, user=user, value=value)


    elif user.getuserstate() == 'COMPLITE_PROMISE':
        user.updatesetting(parameter='COMPLITE_PROMISE', value=value)
        user.resetuserstate()


    elif user.getuserstate() == 'BREAK_PROMISE':
        user.updatesetting(parameter='BREAK_PROMISE', value=value)
        user.resetuserstate()


