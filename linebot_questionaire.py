from flask import Flask, request, abort
# import linebot related
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import configparser
import json
from urllib.parse import parse_qsl
import questionnaire as qu
import list_to_mysql
import linebot_data_to_kafka as ka

#this part read from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# create flask server
app = Flask(__name__)
# your linebot message API - Channel access token (from LINE Developer)
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
# your linebot message API - Channel secret
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
info_data = []

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Message event
@handler.add(MessageEvent)
def questionnaire_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    FlexMessage = json.load(open('card.json', 'r', encoding='utf-8'))
    FlexMessage_gender = json.load(open('card_gender.json', 'r', encoding='utf-8'))

    if message == '@填寫問卷':

        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))

    elif message == '開始填寫問卷':

        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage_gender))
    return user_id

@handler.add(PostbackEvent)  #PostbackTemplateAction觸發此事件
def questionnaire_postback(event):
    user_id = event.source.user_id
    backdata = dict(parse_qsl(event.postback.data))  # 取得data資料
    data = qu.questionnaire_info(event,backdata,line_bot_api)
    global info_data
    if backdata.get('action') == 'recommended_room':
        info_data.append(data)
        print(info_data)
        # print(get_info_data(user_id, info_data))
        consumer, check_data_from_kafka_consumer = ka.linebot_kafka_consumer()
        # print(check_data_from_kafka_consumer)
        ka.linebot_kafka_producer(user_id, info_data)
        print(check_data_from_kafka_consumer)
        # print(f'已確認資料送進test3：{check_data_from_kafka_consumer}')
        # info_data.clear()
    else:
        info_data.append(data)
        print(info_data)

def get_info_data(user_id, data):
    list_to_mysql.connect_to_tfb1031()
    list_to_mysql.insert_data_into_mysql(user_id, data)
    print(f'test{data}')
    insert_data_success = '已經將資料輸入進去MySQL了~'
    return insert_data_success


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=12345, debug=True)