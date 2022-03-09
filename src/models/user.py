from firebase_admin import firestore
from settings import db

user_collection = db.collection('user')


# タグから該当するユーザーのIDを返す
def user_ids_from_tag(tag):
    docs = user_collection.where(
        u'tags', u'array_contains_any', [tag]
    ).get()
    return [doc.id for doc in docs]


class User(object):
    def __init__(
        self,
        ref,
        tags=[],
        created_at=firestore.firestore.SERVER_TIMESTAMP,
        updated_at=firestore.firestore.SERVER_TIMESTAMP
    ):
        self.ref = ref
        self.tags = tags
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def from_uid(uid):
        ref = user_collection.document(uid)
        doc = ref.get()

        return User.from_dict(
            ref,
            doc.to_dict()
        ) if doc.exists else User(ref)

    @staticmethod
    def from_dict(ref, source):
        return User(
            ref,
            source["tags"],
            source["createdAt"],
            source["updatedAt"]
        )

    def to_dict(self):
        return {
            "tags": self.tags,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }

    def __repr__(self):
        return(
            f'User(\
                tags={self.tags}, \
                created_at={self.created_at}, \
                updated_at={self.updated_at} \
            )'
        )

    # タグを追加
    def add_tag(self, tag):
        self.tags.append(tag)
        self.updated_at = firestore.firestore.SERVER_TIMESTAMP

    # タグを削除
    def remove_tag(self, tag):
        self.tags.remove(tag)
        self.updated_at = firestore.firestore.SERVER_TIMESTAMP
