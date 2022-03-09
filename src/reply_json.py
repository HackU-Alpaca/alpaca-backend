from models.message import count_message_from_tag, latest_message_from_tag
from models.tag import Tag, tag_collection
from models.user import User


# タグを登録するカルーセルを返す
def get_register_tag_carousel(uid):
    contents = []

    user = User.from_uid(uid)

    # 全てのタグ情報からメッセージを作成する
    tag_docs = tag_collection.stream()
    for tag_doc in tag_docs:
        tag = Tag.from_dict(tag_doc.to_dict())

        contents.append(
            register_tag_message(
                tag.url,
                tag.name,
                count_message_from_tag(tag.name),
                tag.name in user.tags
            )
        )

    return {
        "type": "flex",
        "altText": "this is a flex message",
        "contents": {
            "type": "carousel",
            "contents": contents
        }
    }


# 登録済み・未登録のタグを返す
def register_tag_message(url, name, comment, registered):
    if not registered:
        register_icon_url = "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip14.png"
        register_button_message = '登録する'
        register_button_send_message = f'{name}を登録する'
        register_background_color = '#55BCABaa'  # 半透明緑
        status_message = '未登録'
        status_background_color = "#00B90044"  # 半透明LINEカラー
    else:
        register_icon_url = "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip14.png"
        register_button_message = '登録解除する'
        register_button_send_message = f'{name}を登録解除する'
        register_background_color = '#9C8E7Ecc'  # 半透明茶色
        status_message = '登録済み'
        status_background_color = "#00B900"  # LINEカラー

    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": url,
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "2:3",
                    "gravity": "top"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": name,
                                    "size": "xl",
                                    "color": "#ffffff",
                                    "weight": "bold"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "応援コメント数",
                                    "color": "#ebebeb",
                                    "size": "sm",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f'{comment}件',
                                    "color": "#ffffffcc",
                                    "decoration": "none",
                                    "gravity": "bottom",
                                    "flex": 0,
                                    "size": "sm",
                                    "weight": "bold"
                                }
                            ],
                            "spacing": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        },
                                        {
                                            "type": "icon",
                                            "url": register_icon_url
                                        },
                                        {
                                            "type": "text",
                                            "text": register_button_message,
                                            "color": "#ffffff",
                                            "flex": 0,
                                            "offsetTop": "-2px"
                                        },
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "spacing": "sm"
                                },
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    ]
                                }
                            ],
                            "borderWidth": "1px",
                            "cornerRadius": "4px",
                            "spacing": "sm",
                            "borderColor": "#ffffff",
                            "margin": "xxl",
                            "height": "40px",
                            "action": {
                                "type": "message",
                                "label": "action",
                                "text": register_button_send_message
                            }
                        }
                    ],
                    "position": "absolute",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px",
                    "backgroundColor": register_background_color,
                    "paddingAll": "20px",
                    "paddingTop": "18px"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": status_message,
                            "color": "#ffffff",
                            "align": "center",
                            "size": "xs",
                            "offsetTop": "3px"
                        }
                    ],
                    "position": "absolute",
                    "cornerRadius": "20px",
                    "offsetTop": "18px",
                    "backgroundColor": status_background_color,
                    "offsetStart": "18px",
                    "height": "25px",
                    "width": "53px"
                },

            ],
            "paddingAll": "0px"
        },

    }


def get_flex_message(tag):
    url = "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip3.jpg"
    message = latest_message_from_tag(tag)
    if message is None:
        return None

    return {
        "type": "flex",
        "altText": "this is a flex message",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "image",
                        "url": url,
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "1:1",
                        "gravity": "center",
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": message.sendTo,
                                "size": "xl",
                                "color": "#ffffff",
                                "contents": [],
                                "weight": "regular",
                                "flex": 0,
                            },
                            {
                                "type": "text",
                                "text": message.context,
                                "color": "#ffffff",
                                "size": "lg",
                                "wrap": True,
                                "maxLines": 8,
                                "gravity": "center",
                                "flex": 1,
                            },
                        ],
                        "position": "absolute",
                        "paddingAll": "20px",
                        "height": "100%",
                        "justifyContent": "flex-start",
                    },
                ],
                "paddingAll": "0px",
            },
        }
    }
