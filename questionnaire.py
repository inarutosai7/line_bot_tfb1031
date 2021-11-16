import json
from linebot.models import *
from urllib.parse import parse_qsl


def questionnaire_info(event,backdata,line_bot_api ):

    if backdata.get('action') == 'gender':
        FlexMessage_travel_type = json.load(open('card_travel_type.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage_travel_type))
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text='測試成功'))
        mode_gender = backdata.get('mode')
        return mode_gender

    elif backdata.get('action') == 'travel_type':
        FlexMessage_recommended_room = json.load(open('card_room_style.json', 'r', encoding='utf-8'))
        mode_travel_type = backdata.get('mode')
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage_recommended_room ))
        return mode_travel_type

    elif backdata.get('action') == 'recommended_room':
        # FlexMessage_recommended_room = json.load(open('room_style.json', 'r', encoding='utf-8'))
        # line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage_recommended_room ))
        mode_remommended_room = backdata.get('mode')
        message = backdata.get('mode')
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = f"{message}已回傳至server"))
        return mode_remommended_room


