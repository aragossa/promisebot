from dbconnector import Botuser
from keyboardhelper import getsettingskeyboard


def settingsmenu (bot, message):
    user = Botuser(message.chat.id)
    statinfo = user.getsetting()
    sendmessage = 'Текущие параметры:\n'
    for parameter in statinfo:
        name = parameter[1]
        value = parameter[2]
        sendmessage = sendmessage + '\n{}: {}'.format(name, value)
    keyboard = getsettingskeyboard()
    bot.send_message (chat_id=message.chat.id, text=sendmessage, reply_markup=keyboard)


def resetstatistics (bot, call):
    user = Botuser(call.message.chat.id)
    user.resetstatistics()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Статистика сброшена')


def updatesetttings(bot, call, parameter):
    user = Botuser(call.message.chat.id)
    user.updateuserstate(parameter)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите значение параметра {}:'.format(parameter))

