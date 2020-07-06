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
    selectedusername = Botuser(selecteduser).getusername()
    if userstate == 'SEND_LIKE':
        sendmessage = '👍'
    elif userstate == 'SEND_DISLIKE':
        sendmessage = '👎'
    sendmessage = sendmessage + '\nот: {}\nкому: {}\n за {}'.format(username, selectedusername, value)
    for curuser in user.getgroupusers():
        bot.send_message(chat_id=curuser.get('id'), text=sendmessage)
    user.resetuserstate()


def likescausehelper(bot, call, action):
    if action == 'lies':
        action = 'Ложь'
    elif action == 'prop':
        action = 'Чужое имущество'
    elif action == 'true':
        action = 'Правда'
    elif action == 'help':
        action = 'Помощь без просьбы'
    user = Botuser(call.message.chat.id)
    sendlikes(bot=bot, user=user, value=action)
