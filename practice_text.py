from flask import Flask
import configparser
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage, ImagemapSendMessage, BaseSize, MessageImagemapAction, URIImagemapAction, ImagemapArea, TemplateSendMessage, ButtonsTemplate, DatetimePickerTemplateAction
from urllib.parse import parse_qsl
import datetime

#this part read from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
key = "ea1adcf8e0a74185b07ddc7cac9d46ea"
endpoint = "https://textclaire.cognitiveservices.azure.com/"
# create flask server
app = Flask(__name__)
# your linebot message API - Channel access token (from LINE Developer)
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
# your linebot message API - Channel secret
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_content = event.message.text
    print(message_content)
    # result = text_analytics_client.analyze_sentiment(mtext)

    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=result)
    # )






if __name__ == '__main__':
    app.run(port=12345)
