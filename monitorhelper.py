from dbconnector import Botuser

def monitor(bot, message):
    user = Botuser(message.chat.id)
    groupuserslist = user.getgroupusers()
    sendmessage = ''
    for curruser in groupuserslist:
        curruserstat = user.getuserstat (curruser.get('id'))
        name = curruserstat[4]
        likes = curruserstat[1]
        dislikes = curruserstat[2]
        trust = curruserstat[3]

        sendmessage = sendmessage + '\n{}:\nЛайки: {}\nДизлайки: {}\nУровень доверия: {}\n'.format(name, likes, dislikes, trust)
    bot.send_message(chat_id=user.uid, text=sendmessage)

