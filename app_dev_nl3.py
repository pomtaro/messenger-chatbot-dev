"""
    基本形完成
    動作確認済み
"""

import os
import sys
import json
from datetime import datetime

import requests
from flask import Flask, request

app = Flask(__name__)

ACCESS_TOKEN = 'EAAFcwgncLV0BAFHgUW60thZCZC2Nsq3ZB8PjZCexZCktXGxaA3k2K2hkBx8O3kD2mrOLj6xNG9lYT2rAzSyAoX06Hpqg1wjWzdg6YdERHzN6BK1yKKjyh1mTkKQzTM6luyeZB09NPx10ZATlptOTxxSv9hSYSdGIKZAsoXPGvfi3ewZDZD'
VERIFY_TOKEN = 'Verify_Token_Dev'

"""
chatbot-dev : 'EAAFcwgncLV0BAPduIt9AjwsONBl2MWTlAWX7yVZCSLn28ew5qlDIaOoEZBdkDOYC4ZAwqYvEPdfzARRTRT2TBNgQfwSi1vZAeytZBoug3PSd8uykY5cr6BVrm5GKNY0ZBo4ORRZCsJDaaHJiMOFjMm9J2JcCZCdFPmwF61YtZA1ZCnlAZDZD'
弁護士bot : 'EAAFcwgncLV0BAFHgUW60thZCZC2Nsq3ZB8PjZCexZCktXGxaA3k2K2hkBx8O3kD2mrOLj6xNG9lYT2rAzSyAoX06Hpqg1wjWzdg6YdERHzN6BK1yKKjyh1mTkKQzTM6luyeZB09NPx10ZATlptOTxxSv9hSYSdGIKZAsoXPGvfi3ewZDZD'
"""


def send_get_started():
    params = {
        "access_token": ACCESS_TOKEN  # os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "get_started": {
            "payload": "Welcome!"
        },
        "greeting": [
            {
                "locale": "default",
                "text": "開発用チャットボット"
            }
        ]
    })

    requests.post("https://graph.facebook.com/v2.6/me/messenger_profile", params=params, headers=headers, data=data)


send_get_started()

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN: # os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
#    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message
                    """
                        ユーザからメッセージが送られた時に実行される
                    """

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    if message_text == '離婚' or message_text == '不倫' or message_text == '相続' or message_text == '残業未払い' or message_text == 'パワハラ' or message_text == 'セクハラ':
                        text = 'あなたの性別を選んでください。'
                        buttons = ['男性', '女性']
                        send_quick_reply(sender_id, text, buttons)

                    elif message_text == '男性' or message_text == '女性':
                        text = '以下から選んでください。'
                        buttons = ['不倫した', '不倫された']
                        send_quick_reply(sender_id, text, buttons)

                    elif message_text == '不倫した' or message_text == '不倫された':
                        text = 'こちらをご覧ください。'
                        title = '不倫相談'
                        subtitle = '不倫は最低な行為です！'
                        url_str = 'https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1075132385'
                        image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVLAZdnZv1gJzt74h7gDiHioQJOxYAL8hdZAi7ulouVYKca6m8KA'
                        send_message(sender_id, text)
                        send_url_image(sender_id, title, subtitle, url_str, image_url)

                        text = '続ける場合は以下から選んでください。'
                        buttons = ['最初から始める']
                        send_quick_reply(sender_id, text, buttons)

                    elif message_text == '最初から始める' or message_text == 'チャットできる人はいますか？' or message_text == '質問があります。':
                        text = "お困りなことはございませんか？"
                        buttons = ["離婚", "不倫", "相続", "残業未払い", "パワハラ", "セクハラ"]
                        send_quick_reply(sender_id, text, buttons)


                    elif message_text == 'urlimage':
                        title = "test title"
                        subtitle = "test subtitle"
                        url_str = "https://pixabay.com/"
                        image_url = "https://cdn.pixabay.com/photo/2018/11/11/16/51/ibis-3809147_960_720.jpg"

                        send_message(sender_id, "こちらをご覧ください。")
                        send_url_image(sender_id, title, subtitle, url_str, image_url)

                    else:
                        buttons = ["A", "B", "C", "D", "E", "F"]
                        send_quick_reply(sender_id, "please select", buttons)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    """
                        「スタート」を押した時に実行される
                        ユーザがボットと会話を初めて開始した時
                    """

                    sender_id = messaging_event["sender"]["id"]
                    text = "お困りなことはございませんか？"
                    buttons = ["離婚", "不倫", "相続", "残業未払い", "パワハラ", "セクハラ"]
                    send_quick_reply(sender_id, text, buttons)

    return "ok", 200


def send_message(recipient_id, message_text):

#    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": ACCESS_TOKEN # os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text,
        }
    })

    """
    ここでrequests.postを実行した時点で指定urlにリクエストを送信し、
    botがメッセージを送信している
    """
    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

#    if r.status_code != 200:
#        log(r.status_code)
#        log(r.text)


def send_quick_reply(recipient_id, text, buttons):

    """
    :param recipient_id: string
    :param text: string
    :param buttons: list; string
    :return: post
    """

    params = {
        "access_token": ACCESS_TOKEN  # os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    quick_replies = []

    for button in buttons:
        quick_dict = {
            "content_type": "text",
            "title": button,
            "payload": "payload: {}".format(button)
        }
        quick_replies.append(quick_dict)

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": text,
            "quick_replies": quick_replies
        }
    })

    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

def send_url_image(recipient_id, title, subtitle, url_str, image_url):
    """
    :param recipient_id: string: bot送信する相手のID
    :param title: string: タイトル
    :param subtitle: string: サブタイトル
    :param url: string: リンク先のURL
    :param url_image: string: サムネイル画像が格納されているURL
    :return: POSTリクエスト
    """

    params = {
        "access_token": ACCESS_TOKEN  # os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": title,
                            "image_url": image_url,
                            "subtitle": subtitle,
                            "buttons": [
                                {
                                    "type":  "web_url",
                                    "url": url_str,
                                    "title": "View Website"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    })

    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


"""
def log(msg):# , *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        #else:
        #    msg = unicode(msg).format(*args, **kwargs)
        #print(u"{}: {}".format(datetime.now(), msg))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()
"""

if __name__ == '__main__':
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)