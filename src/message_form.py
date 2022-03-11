from flask_wtf import FlaskForm
from wtforms import (HiddenField, SelectField, SubmitField, TextAreaField,
                     ValidationError)

from NGdetector.NGdetector import NGdetector


class MessageForm(FlaskForm):
    message = TextAreaField(
        "Message",
        id="message",
        name="message",
        render_kw={"rows": 4}
    )
    submit = SubmitField('送信')
    userId = HiddenField(id="userId", name="userId")
    # tag = SelectField()
    ng_detector = NGdetector()

    def validate_message(self, message):
        """バリデーション内容:
        - 未入力は禁止
        - 文字数が5文字以上は禁止
        - 禁止ワードを含むことは禁止
        """
        if message.data == "":
            raise ValidationError("メッセージを入力してください")

        if len(message.data) < 5:
            raise ValidationError("メッセージは5文字以上にしてください。")

        if not self.ng_detector.check(message.data):
            raise ValidationError("メッセージに禁止ワードが入っています。")

# メソッド名は validate_*(self, formのプロパティ)
