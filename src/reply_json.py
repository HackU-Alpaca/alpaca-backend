# タグを登録するカルーセルを返す
def get_register_tag_carousel(user_id):
    # TODO: firebase から情報を取得
    print(user_id)

    url1 = "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip1.jpg"
    name1 = "医療従事者の皆さん"
    comment1 = 34
    registered1 = True

    url2 = "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip1.jpg"
    name2 = "コロナに感染した皆さん"
    comment2 = 120
    registered2 = False

    return {
        "type": "flex",
        "altText": "this is a flex message",
        "contents": {
            "type": "carousel",
            "contents": [
                register_tag_message(
                    url1,
                    name1,
                    comment1,
                    registered1
                ),
                register_tag_message(
                    url2,
                    name2,
                    comment2,
                    registered2
                )
            ]
        }
    }


# 登録済み・未登録のタグを返す
def register_tag_message(url, name, comment, registered):
    if registered:
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
