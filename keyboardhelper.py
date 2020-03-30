from telebot import types
from dbconnector import Botuser

def getemptyinlinekeyboard():
    return types.InlineKeyboardMarkup()


def getpromsieinlinebutton(action, promiseid, text):
    return types.InlineKeyboardButton(text=text, callback_data=('{}_{}'.format(action, promiseid)))


def getmainmenukeyboard(usertype):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Запрос обещания')
    btn2 = types.KeyboardButton(text='👍')
    btn3 = types.KeyboardButton(text='👎')
    btn4 = types.KeyboardButton(text='Подтвердить выполнение')
    btn5 = types.KeyboardButton(text='Зафиксировать невыполнение')
    btn6 = types.KeyboardButton(text='Актуальные обещания')
    btn7 = types.KeyboardButton(text='Монитор')
    if usertype == 'admin':
        btn8 = types.KeyboardButton('Настройки')
        keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    else:
        keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    return keyboard


def getgroupusersinlinekeyboard(uid):
    keyboard = types.InlineKeyboardMarkup()
    user = Botuser(uid=uid)
    groupusers = user.getgroupusers()
    for curruser in groupusers:
        username = curruser.get('username')
        if curruser.get('id') == user.uid:
            username = 'Себе'
        keyboard.add(types.InlineKeyboardButton(text=username, callback_data=('select_{}'.format(curruser.get('id')))))
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



def getsettingskeyboard():
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='REJECT_REQUEST', callback_data='new_REJECT_REQUEST')
    btn2 = types.InlineKeyboardButton(text='COMPLITE_PROMISE', callback_data='new_COMPLITE_PROMISE')
    btn3 = types.InlineKeyboardButton(text='BREAK_PROMISE', callback_data='new_BREAK_PROMISE')
    btn4 = types.InlineKeyboardButton(text='Обнуление статистики', callback_data='reset')
    keyboard.add(btn1, btn2, btn3, btn4)
    return keyboard


def getchoosepromisetypekeyboard():
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Мои', callback_data='getlist_promisemy')
    btn2 = types.InlineKeyboardButton(text='Мне', callback_data='getlist_promiseme')
    btn3 = types.InlineKeyboardButton(text='Неотвеченные', callback_data='getlist_request')
    keyboard.add(btn1, btn2, btn3)
    return keyboard