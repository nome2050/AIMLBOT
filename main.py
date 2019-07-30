from flask import Flask, render_template, request, jsonify
import aiml
import os
import chatbotapi

app = Flask(__name__)
#
# @app.route("/")
# def hello():
#     return render_template('index.html')

@app.route("/", methods=['GET'])
def get():
	if 'id' in request.args:
		id = request.args['id']
		message = id.strip()
	else:
		message = 'welcome'


	kernel = aiml.Kernel()

	if os.path.isfile("bot_brain.brn"):
	    kernel.bootstrap(brainFile = "bot_brain.brn")
	else:
	    kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
	    kernel.saveBrain("bot_brain.brn")

	# kernel now ready for use
	while True:
	    if message == "quit":
	        exit()
	    elif message == "save":
	        kernel.saveBrain("bot_brain.brn")
	    else:
	        bot_response = kernel.respond(message)

	        return render_template('index.html',answer = bot_response)


if __name__ == '__main__':
    app.run(debug=True)
