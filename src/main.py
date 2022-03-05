from flask import Flask, request, abort, render_template, jsonify
from flask_bootstrap import Bootstrap
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    # PostbackEvent,
    StickerSendMessage,
    TextMessage,
    FlexSendMessage,
    TextSendMessage,
)
from reply_json import get_register_tag_carousel
import os
import dotenv

app = Flask(__name__)
bootstrap = Bootstrap(app)

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
# LINEBOTの返信機能
# =========================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('handle_message')
    print(event.reply_token)
    text_sent_by_user = event.message.text

    # ユーザーのタグ登録を開始
    if text_sent_by_user == "登録する":
        line_bot_api.reply_message(
            event.reply_token,
            messages=FlexSendMessage.new_from_json_dict(
                get_register_tag_carousel()
            )
        )
    # タグを登録
    elif text_sent_by_user.endswith("を登録する"):
        tag = text_sent_by_user[:len("を登録する")]
        # TODO: firebase に登録
        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=f'{tag}を登録しました')
        )
    # タグを登録解除
    elif text_sent_by_user.endswith("を登録解除する"):
        tag = text_sent_by_user[:len("を登録解除する")]
        # TODO: firebase から削除
        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=f'{tag}を登録解除しました')
        )


# =========================
# LIFE
# =========================
@app.route('/cheer-form', methods=['GET'])
def get_cheer_form():
    return render_template('index.html')


@app.route('/cheer-form', methods=['POST'])
def post_cheer_form():
    event = request.form.to_dict()
    print(event)

    # TODO: firebase に保存
    tag = event['tag']
    message = event['message']
    reply_message = f'応援メッセージを送信しました。\n\n{tag}へ\n{message}'

    userId = event['userId']
    line_bot_api.push_message(
        userId,
        [
            TextSendMessage(text=reply_message),
            StickerSendMessage(package_id=6325, sticker_id=10979912),
        ])

    return jsonify({'message': 'SUCCESS: post message to firebase'})


# python main.py　で動作
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
