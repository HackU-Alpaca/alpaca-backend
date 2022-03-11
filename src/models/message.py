import datetime
import json
import random
import string
import time

from firebase_admin import firestore
from settings import db

message_collection = db.collection('message')


# タグ名から応援メッセージの件数をカウント
def count_message_from_tag(tag):
    return len(message_collection.where(
        u'sendTo',
        u'==',
        tag).get())


# 1日1回, ユーザーに通知するメッセージを返す
# TODO: ここのロジックを詰める
def latest_message_from_tag(tag):
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    message = message_collection.where(
        u'sendTo',
        u'==',
        tag).where(
        u'createdAt',
        u'>',
        yesterday).limit(1).get()

    return Message.from_dict(
        message[0].to_dict()) if len(message) != 0 else None


def get_messages_by_tags(tags, num_of_massage):
    messages = message_collection.where(
        u'sendTo',
        u'in',
        tags).limit(num_of_massage).get()

    message_list = []
    for message in messages:
        message_list.append(message.to_dict())

    return_json = json.dumps({"messages": message_list},
                             default=str, ensure_ascii=False)
    return return_json


# n桁のランダム文字列を返す: 7we4CMGjTj
def random_id(n):
    random.seed(time.time())
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


class Message(object):
    def __init__(
            self,
            sendTo,
            context,
            id=None,  # メッセージ識別ID
            likes=0,
            created_at=firestore.firestore.SERVER_TIMESTAMP,
            last_displayed_at=firestore.firestore.SERVER_TIMESTAMP
    ):
        self.id = random_id(10) if id is None else id
        self.sendTo = sendTo
        self.context = context
        self.likes = likes
        self.created_at = created_at
        self.last_displayed_at = last_displayed_at

    @staticmethod
    def from_dict(source):
        return Message(
            source["id"],
            source["sendTo"],
            source["context"],
            source["likes"],
            source["createdAt"],
            source["lastDisplayedAt"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "sendTo": self.sendTo,
            "context": self.context,
            "likes": self.likes,
            "createdAt": self.created_at,
            "lastDisplayedAt": self.last_displayed_at,
        }

    def __repr__(self):
        return (
            f'Message(\
                id={self.id}, \
                sendTo={self.sendTo}, \
                context={self.context}, \
                likes={self.likes}, \
                created_at={self.created_at} \
                last_displayed_at={self.created_at} \
            )'
        )
