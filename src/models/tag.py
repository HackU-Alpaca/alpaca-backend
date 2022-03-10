from firebase_admin import firestore
from settings import db

tag_collection = db.collection('type')


class Tag(object):
    def __init__(
        self,
        name,
        url,
        created_at=firestore.firestore.SERVER_TIMESTAMP,
    ):
        self.name = name
        self.url = url
        self.created_at = created_at

    @staticmethod
    def from_dict(source):
        return Tag(
            source["name"],
            source["url"],
            source["createdAt"]
        )

    def __repr__(self):
        return(
            f'Tag(\
                name={self.name}, \
                url={self.url}, \
                created_at={self.created_at} \
            )'
        )
