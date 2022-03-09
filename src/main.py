import os

from flask import Flask, abort, render_template, request
from flask_bootstrap import Bootstrap
from linebot.exceptions import InvalidSignatureError
from linebot.models import (FlexSendMessage, MessageEvent, StickerSendMessage,
                            TextMessage, TextSendMessage)

from reply_json import get_flex_message, get_register_tag_carousel
from settings import LIFFID, handler, line_bot_api, user_collection

app = Flask(__name__)
bootstrap = Bootstrap(app)


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
            messages=FlexSendMessage.new_from_json_dict(
                get_register_tag_carousel(user_id)
            )
        )
    # タグを登録
    elif text_sent_by_user.endswith("を登録する"):
        tag = text_sent_by_user[:- len("を登録する")]

        # ユーザーを取得
        user_ref = user_collection.document(user_id)
        user_doc = user_ref.get()
        # タグを追加
        tags = user_doc.to_dict()["tags"] if user_doc.exists else []
        tags.append(tag)
        user_ref.set(
            {u'tags': tags}, merge=True
        )

        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=f'{tag}を登録しました')
        )
    # タグを登録解除
    elif text_sent_by_user.endswith("を登録解除する"):
        tag = text_sent_by_user[:- len("を登録解除する")]

        # ユーザーを取得
        user_ref = user_collection.document(user_id)
        # タグを削除
        tags = user_ref.get().to_dict()["tags"]
        tags.remove(tag)
        user_ref.set(
            {u'tags': tags}, merge=True
        )

        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text=f'{tag}を登録解除しました')
        )


# 毎日のメッセージを送信する
@app.route('/send_daily_message', methods=['GET'])
def send_daily_message():
    # TODO:
    # 1. Firebase からタグ情報を全て取得する
    # 2. タグで forループ (3~5)
    # 3. where(tag) でユーザーを取得
    # 4. ユーザーが存在する場合に, get_flex_message でメッセージを取得
    # 5. ユーザーに対してメッセージを送信
    #    line_bot_api.push_message ...
    return get_flex_message()


# =========================
# LIFE
# =========================
@app.route('/cheer-form', methods=['GET'])
def get_cheer_form():
    # TODO: タグ一覧を渡す
    return render_template('index.html', LIFFID=LIFFID)


# 確認画面に遷移
# - バリデーション実行
@app.route('/cheer-form', methods=['POST'])
def post_cheer_form():
    event = request.form.to_dict()
    tag = event['tag']
    message = event['message']
    userId = event['userId']

    # TODO:
    # バリデーションを走らせる
    # 1. 値が入力されているかの確認
    # 2. 誹謗中傷フィルタリング

    return render_template(
        'confirm.html',
        userId=userId,
        tag=tag,
        message=message)


# 確認画面から投稿, 終了画面に遷移
# - Firebaseに保存
# - LINEに確認メッセージを送信
@app.route('/cheer-form-confirm', methods=['POST'])
def post_cheer_form_confirm():
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

    return render_template('end.html')


# python main.py　で動作
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
