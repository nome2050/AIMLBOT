import aiml,os,json,random,secrets
from flask import Flask, render_template, request, jsonify

bot = aiml.Kernel()
# username = ''
# password = ''

bot.setBotPredicate(name="name", value="GrandBot")

if os.path.isfile("bot_brain.brn"):
      bot.bootstrap(brainFile = "bot_brain.brn")
else:
    bot.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands ="load aiml b")
    bot.saveBrain("bot_brain.brn")

# def createuser():
# #     sessionId=secrets.token_hex()
# #     sessionkey = {'sessid':sessionId}
# #     username=input("Enter a UserName")
# #     password = input("Enter a Password")
# #     if os.path.isfile(username + ".jarvis.txt"):
# #         print("Username Already in Use")
# #         createuser()
# #     else:
# #         with open(username+'.jarvis.txt', 'w') as outfile:
# #             json.dump(sessionkey, outfile)
# #     return sessionId


def remember(KeyId,bot):
    if os.path.isfile(KeyId+".jarvis.txt"): #Load saved session
        with open(KeyId + ".jarvis.txt") as json_file:
            data = json.load(json_file)
        for pre, value in data.items():
            print(pre,value)
            bot.setPredicate(pre, value,KeyId)
        return (KeyId)
    else:
        return ("No Such User , Your data cannot be loaded")


def savingdata(KeyId):
    sessionfile = bot.getSessionData( KeyId )
    print(sessionfile)

    if os.path.isfile(KeyId + ".jarvis.txt"):
        with open(KeyId + ".jarvis.txt") as json_file:
            loaded = json.load(json_file)


        # with open(KeyId + ".jarvis.txt") as json_file:
        #     data = json.load(json_file)
        # KeyId['sessid'] = data['sessid']

        with open(KeyId + ".jarvis.txt", 'w') as json_file:
            data = json.dump(sessionfile, json_file)
    else:
        return ("Key not Found")

#
app = Flask(__name__)
@app.route("/",methods = ['GET'])
def get():
    if 'KeyId' in request.args:
        KeyId = request.args['KeyId']
    if 'query' in request.args:
        message = request.args['query']
        remember(KeyId,bot)

        if message == "quit":
            savingdata(KeyId)
            # bot.saveBrain("bot_brain.brn")
            exit()
        elif message=='save':
             savingdata(KeyId)
            # elif message=='login':
            #         KeyId=input("Enter Key")
            #         currentsession,use=remember(KeyId,bot)
            #         KeyId=currentsession
            # elif message=='register':
            #     currid = createuser()
            #     KeyId = currid
        elif message == 'session':
             return ( KeyId )
        else:
           hum = KeyId
           bot_response = bot.respond(message, hum)
           return (bot_response)


if __name__ == '__main__':
   app.run()