import aiml,os,json,random,secrets
bot = aiml.Kernel()
sessionId = 0
username = ''
password = ''

bot.setBotPredicate(name="name", value="GrandBot")


if os.path.isfile("bot_brain.brn"):
      bot.bootstrap(brainFile = "bot_brain.brn")
else:
    bot.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands ="load aiml b")
    bot.saveBrain("bot_brain.brn")

def createuser():
    sessionId=secrets.token_hex()
    sessionkey = {'sessid':sessionId}
    username=input("Enter a UserName")
    password = input("Enter a Password")
    if os.path.isfile(username + ".jarvis.txt"):
        print("Username Already in Use")
        createuser()
    else:
        with open(username+'.jarvis.txt', 'w') as outfile:
            json.dump(sessionkey, outfile)
    return sessionId



def remember(username,password,bot):
    if os.path.isfile(username+".jarvis.txt"): #Load saved session
        with open(username + ".jarvis.txt") as json_file:
            data = json.load(json_file)
        sessionId=data['sessid']
        for pre, value in data.items():
            print(pre,value)
            bot.setPredicate(pre, value,sessionId)
        return (sessionId,username)
    else:
        return ("No Such User , Your data cannot be loaded")


def savingdata(username):
    sessionfile = bot.getSessionData(sessionId)
    print(sessionfile)

    if os.path.isfile(username + ".jarvis.txt"):
        with open(username + ".jarvis.txt") as json_file:
            loaded = json.load(json_file)


        with open(username + ".jarvis.txt") as json_file:
            data = json.load(json_file)
        sessionfile['sessid'] = data['sessid']

        with open(username + ".jarvis.txt", 'w') as json_file:
            data = json.dump(sessionfile, json_file)
    else:
        return ("No Username Found")




while True:
    message = input("Enter your message to the bot: ")
    if message == "quit":
        savingdata(username)
        bot.saveBrain("bot_brain.brn")
        exit()
    elif message=='save':
        savingdata(username)
    elif message=='login':
            username=input(" Enter Username : ")
            password=input(" Enter Password : ")
            currentsession,use=remember(username,password,bot)
            sessionId=currentsession
            username=use
            print(username)
            print(sessionId)

    elif message=='register':
        currid = createuser()
        sessionId = currid
    elif message == 'session':
        print(sessionId)
    else:
            hum = sessionId
            print(hum)
            bot_response = bot.respond(message, hum)
            print(bot_response)
