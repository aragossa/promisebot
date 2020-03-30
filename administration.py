from dbconnector import Botuser
from keyboardhelper import getmainmenukeyboard


def makemesuperuser(bot, message):
    user=Botuser(message.chat.id)
    user.makemesuperuser()

def keygen (bot, message):
    user=Botuser(message.chat.id)
    if user.issuperuser():
        newkey = user.getnewkey()
        bot.send_message(message.chat.id, 'Ключ для подключения: {0}. Пользователю необходимо будет выполнить при открытии чата с ботом (@pocketclerk_bot) команду:\n\n/addadmin {0}'.format(newkey))
    else:
        bot.send_message(message.chat.id, 'Доступ ограничен')


def addadmin(bot, message, key):
    user = Botuser(message.chat.id)
    username = message.from_user.username
    if username is None:
        username = 'Не задано'
        bot.send_message(message.chat.id, 'Не удалось определить имя пользователя. Используйте команду\n\n/setusername Ваше_Имя_Пользователя')
    check = user.addadmin(key=key, username=username)
    if check:
        usertype = user.getusertype()
        keyboard = getmainmenukeyboard(usertype=usertype)
        bot.send_message(message.chat.id, 'Поздравляем, Вы создали группу в боте, для подключения пользователей к Вашей группе в боте (@pocketclerk_bot), используйте команду:\n\n/joingroup {}'.format(user.uid), reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Активационный ключ недействительный или уже был активирован')


def adduser(bot, message, key):
    user = Botuser(message.chat.id)
    username = message.from_user.username
    if username is None:
        username = 'Не задано'
        bot.send_message(message.chat.id, 'Не удалось определить имя пользователя. Используйте команду\n\n/setusername Ваше_Имя_Пользователя')
    check = user.adduser(key=key, username=username)
    if check:
        usertype = user.getusertype()
        keyboard = getmainmenukeyboard(usertype=usertype)
        bot.send_message(message.chat.id, 'Поздравляем, Вы подключены к группе № {}'.format(key), reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Номер группы указан неверно')


def setusername(bot, message, username):
    user = Botuser(message.chat.id)
    user.setusername(username)