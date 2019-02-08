#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
# from pymessenger.bot_higashi import Bot_Higashi
import os
import attr

app = Flask(__name__)

#ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
#VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

ACCESS_TOKEN = 'EAAFeCdfXrZBkBADLEfd4NjQ3BbbjmwYncxQFpz3yfLmM7nDvCZBvzI8snn8mEg6QNdHGYeKXZChlHAd8xZCt89uhL0FkZA0drgBzYCIgImkr3JUhNZAs8nc3vod86gPaIbzpbWQVDACF9BWzcmqxXtCG6JpAhWHCXCmB7t1Ete5wZDZD'
VERIFY_TOKEN = 'Verify_Token_Dev'

bot = Bot(ACCESS_TOKEN)
# bot_higashi = Bot_Higashi(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """
            正しいendpointかどうか認証するためのAPI
            Botに設定したurlが正しいかチェックする
            hub.verify_tokenが、事前に生成したtokenと合致するかチェック
            合致した場合、hub.challnegeをそのままレスポンスとして返す -> verify_fb_tokenの関数で実行
        """
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
                    response_sent_text = get_message(message['message'].get('text'))
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message(message['message'].get('attachments'))
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

"""
@attr.s
class QuickReply(object):
    
    content_type = attr.ib()
    title = attr.ib(default=None)
    payload = attr.ib(default=None)
    image_url = attr.ib(default=None)

    def __attrs_post_init__(self):
        assert self.content_type in {'text', 'location'}
        assert self.content_type == 'location' or self.title

        if not self.payload:
            self.payload = self.title
"""

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message(message):
    #sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    # return random.choice(sample_responses)
    if message == 'hello':
        return 'hello!'
    elif message == 'where?':
        return 'japan'
    elif message == 'where':
        return 'japan'
    elif message == 'Where?':
        return japan
    elif message == 'Where':
        return 'japan'
    elif message == 'how old?':
        return '27'
    elif message == 'how old':
        return '27'
    elif message == 'How old?':
        return '27'
    elif message == 'How old':
        return '27'

#    elif message == 'quick':
#        send_quick()

    else:
        return "Sorry. I don't know what to say. For example, please say "\
               + '"{}"'.format(random.choice(['hello', 'where?', 'how old?']))\
               + '.'

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

"""
def send_quick_reply(recipient_id, message, buttons):

    return bot.send_message(recipient_id, {
        'text': message,
        'quick_replies': buttons
        })

def send_quick():
    buttons = []
    button = QuickReply(content_type='text', title='Button 1', payload='btn1')
    buttons.append(button)
    button = QuickReply(content_type='text', title='Button 2', payload='btn2')
    buttons.append(button)
    message = 'Select'

    return send_quick_reply(recipient_id, message, buttons)
"""



"""
def send_quick_reply(recipient_id,
                     message,
                     buttons,
                     notification_type=NotificationType.regular):

    return bot.send_message(recipient_id, {
            'text': message,
            'quick_replies': buttons
        }, notification_type)

def send_quick():
    buttons = []
    button = 
"""

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5002))
    app.run(host="0.0.0.0", port=port)