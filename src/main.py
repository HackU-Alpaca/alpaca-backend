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
import os
import dotenv

app = Flask(__name__)

# =========================
# 環境変数取得
# LINE Developers: アクセストークン/ChannelSecret
# =========================
dotenv.load_dotenv()
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


# =========================
# Webhookからのリクエストの署名検証部分
# =========================
@app.route("/callback", methods=['POST'])
def callback():
    # 署名検証のための値
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 署名検証
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:  # 失敗したとき エラー
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# =========================
# おうむ返し機能
# =========================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text_sent_by_user = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text_sent_by_user)
    )


# python main.py　で動作
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
