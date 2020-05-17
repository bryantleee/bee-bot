#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
from secrets import ACCESS_TOKEN
import nltk.data

sentences = []
sentence_counter = {} #keeps track of what sentence each recipient is on

app = Flask(__name__)
VERIFY_TOKEN = 'TORTTHETURTLEISAGOODTURTLE'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    # response_sent_text = get_message()
                    bee_movie_sentence = get_message(recipient_id)
                    send_message(recipient_id, bee_movie_sentence)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    bee_movie_sentence = get_message(recipient_id)
                    send_message(recipient_id, bee_movie_sentence)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message(recipient_id):
    if recipient_id in sentence_counter:
        sentence_counter[recipient_id] += 1
    else:
        sentence_counter[recipient_id] = 0
    index = sentence_counter[recipient_id]
    print(recipient_id,':', index)
    # return selected bee movie sentence to the user
    return sentences[index]

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    with open('./data/bee_movie_script.txt') as f:
        bee_movie_script = f.read()
    tokenizer = nltk.data.load('./data/english.pickle') 
    sentences = tokenizer.tokenize(bee_movie_script) #split bee movie into sentences
    app.run()