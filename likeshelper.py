from dbconnector import Botuser
from requesthelper import senduserlist


def likeshandler(bot, message, action):
    if action == 'like':
        userstate = 'SEND_LIKE'
    if action == 'dislike':
        userstate = 'SEND_DISLIKE'
    user = Botuser (message.chat.id)
    user.updateuserstate(newstate=userstate)
    senduserlist(bot=bot, message=message)

def sendlikes(bot, user, value):
    userstate = user.getuserstate()
    selecteduser = user.getuserselecteduser()
    user.sendlikes (userstate, selecteduser, value)
    username = user.getusername()
    if userstate == 'SEND_LIKE':
        sendmessage = 'Лайк'
    elif userstate == 'SEND_DISLIKE':
        sendmessage = 'Дизлайк'
    sendmessage = sendmessage + ' от {} за {}'.format(username, value)
    bot.send_message(selecteduser, text=sendmessage)
    user.resetuserstate()