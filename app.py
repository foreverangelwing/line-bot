from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
