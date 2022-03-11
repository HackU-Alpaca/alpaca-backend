import os

from flask import Flask, abort, jsonify, render_template, request
from flask_bootstrap import Bootstrap
from linebot.exceptions import InvalidSignatureError
from linebot.models import (FlexSendMessage, MessageEvent, StickerSendMessage,
                            TextMessage, TextSendMessage)
from message_form import MessageForm
from models.message import *
from models.tag import tag_collection
from models.user import User, user_ids_from_tag
from reply_json import get_flex_message, get_register_tag_carousel
from settings import LIFFID, handler, line_bot_api

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = SECRET_KEY  # formのCSRFトークンのSecretKey


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
    user_id = event.source.user_id
    text_sent_by_user = event.message.text

    # ユーザーのタグ登録を開始
    if text_sent_by_user == "登録する":
        line_bot_api.reply_message(
            event.reply_token,
            messages=[
                TextSendMessage(text='ご自身の所属を選択してください。'),
                FlexSendMessage.new_from_json_dict(
                    get_register_tag_carousel(user_id)
                )
            ]
        )
    # タグを登録
    elif text_sent_by_user.endswith("を登録する"):
        tag = text_sent_by_user[:- len("を登録する")]

        user = User.from_uid(user_id)
        user.add_tag(tag)
        user.ref.set(
            user.to_dict(),
        )

        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=f'{tag}を登録しました')
        )
    # タグを登録解除
    elif text_sent_by_user.endswith("を登録解除する"):
        tag = text_sent_by_user[:- len("を登録解除する")]

        user = User.from_uid(user_id)
        user.remove_tag(tag)
        user.ref.set(
            user.to_dict(),
        )

        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=f'{tag}を登録解除しました')
        )


# 毎日のメッセージを送信する
# 登録しているタグごとに 1日1回のメッセージを送信
# MEMO:
# schedule.every() などで実装すべきであるが，
# ハッカソンの発表で使用しやすいように /send_daily_message へのアクセルをトリガーとし,
# Heroku scheduler で定期実行を行う
@app.route('/send_daily_message', methods=['GET'])
def send_daily_message():
    result = {}

    tag_docs = tag_collection.stream()
    for tag_doc in tag_docs:
        user_ids = user_ids_from_tag(tag_doc.id)

        # ユーザーが存在する場合のみ処理を継続
        if len(user_ids) == 0:
            continue

        # 直近24時間以内のメッセージを検索
        message = get_flex_message(tag_doc.id)
        if message is None:
            continue

        # メッセージを送信（送信数をメモ）
        result[tag_doc.id] = len(user_ids)
        line_bot_api.multicast(
            user_ids,
            FlexSendMessage.new_from_json_dict(
                message
            )
        )

    return jsonify(result)


# =========================
# LIFE
# =========================
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/cheer-form', methods=['GET', 'POST'])
def cheer_form():
    form = MessageForm()

    if request.method == "POST":
        event = request.form.to_dict()
        tag = event['tag']
        message = event['message']
        userId = event['userId']
        if form.validate_on_submit():
            return render_template(
                'confirm.html',
                userId=userId,
                tag=tag,
                message=message)
    tag_docs = tag_collection.stream()
    return render_template(
        'index.html',
        form=form,
        LIFFID=LIFFID,
        tags=[tag_doc.id + "の皆様へ" for tag_doc in tag_docs]
    )


# 確認画面から投稿, 終了画面に遷移
# - Firebaseに保存
# - LINEに確認メッセージを送信
@app.route('/cheer-form-confirm', methods=['POST'])
def post_cheer_form_confirm():
    event = request.form.to_dict()

    tag = event['tag'][:- len("の皆様へ")]
    message = event['message']
    # Firebase に保存
    msg = Message(tag, message)
    message_collection.document(msg.id).set(
        msg.to_dict()
    )

    reply_message = f'応援メッセージを送信しました。\n\n{tag}の皆様へ\n{message}'

    userId = event['userId']
    line_bot_api.push_message(
        userId,
        [
            TextSendMessage(text=reply_message),
            StickerSendMessage(package_id=6325, sticker_id=10979912),
        ])

    return render_template('end.html')


@app.route('/get_messages_by_tag/', methods=['GET'])
def get_cheer_message_by_tag():
    req = request.args

    # パラメータ取得
    tag = req.get('tag')
    num_of_message = req.get('num_of_message', type=int)

    return get_messages_by_tag(tag, num_of_message)


# python main.py　で動作
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
