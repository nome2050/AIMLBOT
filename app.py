from flask import Flask, render_template, request, jsonify
import aiml, os, json, random
import secrets

bot = aiml.Kernel()
sessionId = 0
username = ''
password = ''

bot.setBotPredicate(name="name", value="GrandBot")

if os.path.isfile("bot_brain.brn"):
    bot.bootstrap(brainFile="bot_brain.brn")
else:
    bot.bootstrap(learnFiles=os.path.abspath("aiml/std-startup.xml"), commands="load aiml b")
    bot.saveBrain("bot_brain.brn")



def createuser():
    sessionId = secrets.token_hex()
    sessionkey = {'sessid': sessionId}
    username = input("Enter a UserName")
    password = input("Enter a Password")
    if os.path.isfile(username + ".jarvis.txt"):
        print("Username Already in Use")
        createuser()
    else:
        with open(username + '.jarvis.txt', 'w') as outfile:
            json.dump(sessionkey, outfile)
    return sessionId


def remember(username, password, bot):
    if os.path.isfile(username + ".jarvis.txt"):  # Load saved session
        with open(username + ".jarvis.txt") as json_file:
            data = json.load(json_file)
        sessionId = data['sessid']
        sessionId = int(sessionId)
        for pre, value in data.items():
            print(pre, value)
            bot.setPredicate(pre, value, sessionId)
        return (sessionId, username)
    else:
        return (0,'')


def savingdata(username):
    sessionfile = bot.getSessionData(sessionId)
    print(sessionfile)

    if os.path.isfile(username + ".jarvis.txt"):
        with open(username + ".jarvis.txt") as json_file:
            loaded = json.load(json_file)

        # finaldata = mergedata(sessionfile,loaded)

        with open(username + ".jarvis.txt") as json_file:
            data = json.load(json_file)
        sessionfile['sessid'] = data['sessid']

        with open(username + ".jarvis.txt", 'w') as json_file:
            data = json.dump(sessionfile, json_file)




app = Flask(__name__)


@app.route("/", methods=['GET'])
def get():
    if 'id' in request.args:
        id = request.args['id']
        message = id.strip()
    else:
        message = 'welcome'



    global sessionId, bot_response
    global username
    global password





    while True:
        if message == "quit":
            savingdata(username)
            bot.saveBrain("bot_brain.brn")
            exit()
        elif message == 'save':
            savingdata(username)
            bot_response = 'Saved in Successfully'
        elif message == 'login':
            username = input(" Enter Username : ")
            password = input(" Enter Password : ")
            currentsession, use = remember(username, password, bot)
            sessionId = currentsession
            username = use
            bot_response = 'Login Successfully'
        elif message == 'register':
            currid = createuser()
            sessionId = currid
            bot_response = 'Create Successfully'
        elif message == 'session':
            print(sessionId)
            bot_response = sessionId
        else:
            if sessionId == 0:
                bot_response = bot.respond(message)
            else:
                hum = sessionId
                print(hum)
                bot_response = bot.respond(message, hum)
        return render_template('index.html', answer=bot_response )



if __name__ == '__main__':
    app.run(debug=True)
