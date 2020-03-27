from telebot import types

def getmainmenukeyboard (usertype):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Запрос обещания')
    btn2 = types.KeyboardButton('Подтвердить выполнение')
    btn3 = types.KeyboardButton('Зафиксировать невыполнение')
    btn4 = types.KeyboardButton('Актуальные обещания')
    btn5 = types.KeyboardButton('Монитор')
    if usertype == 'admin':
        btn6 = types.KeyboardButton('Настройки')
        keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)
    else:
        keyboard.add(btn1, btn2, btn3, btn4, btn5)
    return keyboard

def sendmainmenukeyaboard():
    print ('mainmenu')