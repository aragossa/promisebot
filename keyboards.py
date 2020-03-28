from telebot import types
from dbconnector import Botuser


def getmainmenukeyboard(usertype):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Запрос обещания')
    btn2 = types.KeyboardButton(text='Подтвердить выполнение')
    btn3 = types.KeyboardButton(text='Зафиксировать невыполнение')
    btn4 = types.KeyboardButton(text='Актуальные обещания')
    btn5 = types.KeyboardButton(text='Монитор')
    if usertype == 'admin':
        btn6 = types.KeyboardButton('Настройки')
        keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)
    else:
        keyboard.add(btn1, btn2, btn3, btn4, btn5)
    return keyboard


def getgroupusersinlinekeyboard(uid):
    keyboard = types.InlineKeyboardMarkup()
    user = Botuser(uid=uid)
    groupusers = user.getgroupusers()
    for curruser in groupusers:
        username = curruser.get('username')
        if curruser.get('id') == user.uid:
            username = 'Себе'
        keyboard.add(types.InlineKeyboardButton(text=username, callback_data=('select_{}'.format (curruser.get('id')))))
    return keyboard


def getdateinlinekeyboard():
    keyboard = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='✅ дата обещания', callback_data='request_addate')
    keyboard.add(btn)
    return keyboard


def getnodateinlinekeyboard():
    keyboard = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='❌ дата обещания', callback_data='request_nodate')
    keyboard.add(btn)
    return keyboard

def getrecipientrequestkeyboard(requestid):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='✅', callback_data='request_accept_{}'.format(requestid))
    btn2 = types.InlineKeyboardButton(text='❌', callback_data='request_reject_{}'.format(requestid))
    keyboard.add(btn1, btn2)
    return keyboard
