from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage, ImageSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('9bOWsz4sqFPhRd1/COk2d6LY6+f3Zw3CGKAgIFXnaWl6t85U4KmH6dl7JeMtuzJuEhU1GgYDxJdMoNght//m2B3KerAUlgsGEnrk4eSrl6Y6Zjxg3SqDtLN2UWSaUw3goySF9GpTJqfq7EnqlyuSLgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fbd1ef7c832618765158ccbcfaa31961')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉，我不懂您在說什麼？'

    if msg in ['UR-515', 'UR515', 'ur515', 'ur-515']:
        image_message = ImageSendMessage(
        original_content_url='https://www.dropbox.com/s/a4f9wy74wjy0yni/1.jpg?dl=0',
        preview_image_url='https://www.dropbox.com/s/a4f9wy74wjy0yni/1.jpg?dl=0'
    )
        line_bot_api.reply_message(
        event.reply_token,
        image_message)

        return


    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
        package_id='446',
        sticker_id='1993'
    )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

        return

    if msg in ['hi', 'Hi']:
        r = 'hi'
    elif msg == '你吃飯了嗎？':
        r = '還沒吃飯'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位，是嗎？'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()
