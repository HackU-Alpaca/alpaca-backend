import datetime

from firebase_admin import firestore
from settings import db

message_collection = db.collection('message')


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


class Message(object):
    def __init__(
        self,
        sendTo,
        context,
        likes=0,
        created_at=firestore.firestore.SERVER_TIMESTAMP,
    ):
        self.sendTo = sendTo
        self.context = context
        self.likes = likes
        self.created_at = created_at

    @staticmethod
    def from_dict(source):
        return Message(
            source["sendTo"],
            source["context"],
            source["likes"],
            source["createdAt"]
        )

    def to_dict(self):
        return {
            "sendTo": self.sendTo,
            "context": self.context,
            "likes": self.likes,
            "createdAt": self.created_at
        }

    def __repr__(self):
        return(
            f'Message(\
                sendTo={self.sendTo}, \
                context={self.context}, \
                likes={self.likes}, \
                created_at={self.created_at} \
            )'
        )
