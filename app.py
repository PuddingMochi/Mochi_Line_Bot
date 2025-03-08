from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    TemplateMessage,
    ButtonsTemplate,
    PostbackAction,
    PushMessageRequest,
    BroadcastRequest,
    MulticastRequest,
    Emoji,
    VideoMessage,
    AudioMessage,
    LocationMessage,
    StickerMessage,
    ImageMessage,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    MessageAction,
    URIAction,
    DatetimePickerAction,
    FlexMessage,
    FlexBubble,
    FlexImage,
    FlexMessage,
    FlexBox,
    FlexText,
    FlexIcon,
    FlexButton,
    FlexSeparator,
    FlexContainer,
    ImagemapArea,
    ImagemapBaseSize,
    ImagemapExternalLink,
    ImagemapMessage,
    ImagemapVideo,
    URIImagemapAction,
    MessageImagemapAction,
    QuickReply,
    QuickReplyItem,
    PostbackAction,
    MessageAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    MessagingApiBlob,
)
from linebot.v3.webhooks import (
    MessageEvent,
    FollowEvent,
    PostbackEvent,
    TextMessageContent
)
import requests
import json
import os

app = Flask(__name__)


configuration = Configuration(access_token = os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('YOUR_CHANNEL_SECRET'))
#url_root = 'https://github.com/PuddingMochi/Mochi_Line_Bot/blob/main/'
url_root = 'https://puddingmochi.github.io/Mochi_Line_Bot/'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@line_handler.add(FollowEvent)
def handle_follow(event):
    print(f'Got {event.type} event')

@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        '''if event.message.text == 'postback':
            buttons_template = ButtonsTemplate(
                title='Postback Sample',
                text='Postback Action',
                actions=[
                    PostbackAction(label='Postback Action', text='Postback Action Button Clicked!', data='postback'),
                ])
            template_message = TemplateMessage(
                alt_text='Postback Sample',
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )'''
        if text == '文字':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="嗨呀~")]
                )
            )
        elif text == '表情符號':
            emojis = [
                Emoji(index=0, product_id="5ac21c4e031a6752fb806d5b", emoji_id="001"),
                Emoji(index=1, product_id="5ac21c4e031a6752fb806d5b", emoji_id="046"),
                Emoji(index=2, product_id="5ac21c4e031a6752fb806d5b", emoji_id="008"),
                Emoji(index=14, product_id="5ac2213e040ab15980c9b447", emoji_id="058"),
            ]
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='$$$ LINE 表情符號 $', emojis=emojis)]
                )
            )
        elif text == '貼圖':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[StickerMessage(package_id="6362", sticker_id="11087922")]
                )
            )
        elif text == '圖片':
            #url = url_root + 'static/231031.png'
            #url = url.replace("http", "https")
            url = 'https://i.imgur.com/iLDesSr.png'
            app.logger.info("url=" + url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(original_content_url=url, preview_image_url=url)
                    ]
                )
            )
        elif text == '影片':
            #url = url_root + 'static/GAME_20240722-170540.mp4'
            #url = url.replace("http", "https")
            url = 'https://i.imgur.com/RZmq1u4.mp4'
            app.logger.info("url=" + url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        VideoMessage(original_content_url=url, preview_image_url=url)
                    ]
                )
            )
        elif text == '音訊':
            #url = url_root + 'static/knights.mp3'
            #url = url.replace("http", "https")
            url = 'https://res.cloudinary.com/dmxvf8yqt/video/upload/v1741433598/knights_ii3rvg.mp3'
            app.logger.info("url=" + url)
            duration = 10000  # in milliseconds
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        AudioMessage(original_content_url=url, duration=duration)
                    ]
                )
            )
        elif text == '位置':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        LocationMessage(title='Location', address="Taipei", latitude=25.0475, longitude=121.5173)
                    ]
                )
            )
        elif text == '確認':
            confirm_template = ConfirmTemplate(
                text='吃飯了沒?',
                actions=[
                    MessageAction(label='是', text='是!'),
                    MessageAction(label='否', text='否!')
                ]
            )
            template_message = TemplateMessage(
                alt_text='Confirm alt text',
                template=confirm_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )
        # Buttons Template
        elif text == '按鈕':
            #url = url_root + 'static/1415413-4-1.png'
            #url = url.replace("http", "https")
            url = 'https://i.imgur.com/qj1qAII.png'
            app.logger.info("url=" + url)
            buttons_template = ButtonsTemplate(
                thumbnail_image_url=url,
                title='Mochi Bot',
                text='文字的說明啦啦啦',
                actions=[
                    URIAction(label='神秘的連結', uri='https://page.kakao.com/content/48772021'),
                    PostbackAction(label='回傳值', data='ping', displayText='傳了'),
                    MessageAction(label='傳"哈囉"', text='哈囉'),
                    DatetimePickerAction(label="選擇時間", data="時間", mode="datetime"),
                    #CameraAction(label='拍照'),
                    #CameraRollAction(label='選擇相片'),
                    #LocationAction(label='選擇位置')
                ]
            )
            template_message = TemplateMessage(
                alt_text="This is a buttons template",
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )
        # Carousel Template
        elif text == '輪播':
            #url = url_root + 'static/1415413-4-1.png'
            #url = url.replace("http", "https")
            url = 'https://i.imgur.com/qj1qAII.png'
            app.logger.info("url=" + url)
            carousel_template = CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=url,
                        title='1',
                        text='什麼的描述1',
                        actions=[
                            URIAction(
                                label='놀러와마이홈漫畫',
                                uri='https://page.kakao.com/content/48772021'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=url,
                        title='2',
                        text='什麼的描述2',
                        actions=[
                            URIAction(
                                label='光遇的燒錢商店',
                                uri='http://thatskyshop.com/?srsltid=AfmBOorEda8cCHKblHJL5PFK3-subRaYYKhI2KvQF93WILvtI6N0BmGr'
                            )
                        ]
                    )
                ]
            )

            carousel_message = TemplateMessage(
                alt_text='這是 Carousel Template',
                template=carousel_template
            )

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages =[carousel_message]
                )
            )
        # ImageCarousel Template
        elif text == '圖片輪播':
            url = url_root + 'static/'
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            image_carousel_template = ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        #image_url=url+'1415413-4-1.png',
                        image_url = 'https://i.imgur.com/qj1qAII.png',
                        action=URIAction(
                            label='놀러와마이홈漫畫',
                            uri='https://page.kakao.com/content/48772021'
                        )
                    ),
                    ImageCarouselColumn(
                        #image_url=url+'1415413-4-2.png',
                        image_url = 'https://i.imgur.com/kukgTOV.png',
                        action=URIAction(
                            label='光遇的燒錢商店',
                            uri='http://thatskyshop.com/?srsltid=AfmBOorEda8cCHKblHJL5PFK3-subRaYYKhI2KvQF93WILvtI6N0BmGr'
                        )
                    ),
                    ImageCarouselColumn(
                        #image_url=url+'1415413-4-3.png',
                        image_url = 'https://i.imgur.com/tPXA5ts.png',
                        action=URIAction(
                            label='夢幻城資訊',
                            uri='https://forum.gamer.com.tw/B.php?bsn=75719'
                        )
                    ),
                ]
            )

            image_carousel_message = TemplateMessage(
                alt_text='圖片輪播範本',
                template=image_carousel_template
            )

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[image_carousel_message]
                )
            )
        elif text == 'flex1':
            line_flex_json = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2325290/header.jpg?t=1737583134",
                    "size": "full",
                    "aspectRatio": "20:10",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "Sky.光遇",
                        "weight": "bold",
                        "size": "xl",
                        "contents": [
                            {
                                "type": "span",
                                "text": "Sky光.遇"
                            },
                            {
                                "type": "span",
                                "text": "因光而遇",
                                "size": "sm",
                                "style": "italic"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                        {
                            "type": "icon",
                            "size": "sm",
                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                        },
                        {
                            "type": "icon",
                            "size": "sm",
                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                        },
                        {
                            "type": "icon",
                            "size": "sm",
                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                        },
                        {
                            "type": "icon",
                            "size": "sm",
                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                        },
                        {
                            "type": "icon",
                            "size": "sm",
                            "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                        },
                        {
                            "type": "text",
                            "text": "5.0",
                            "size": "sm",
                            "color": "#999999",
                            "margin": "md",
                            "flex": 0
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": "Address",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 3
                            },
                            {
                                "type": "text",
                                "text": "Flex Tower, 7-7-4 Midori-ku, Tokyo",
                                "wrap": True,
                                "color": "#666666",
                                "size": "sm",
                                "flex": 7
                            }
                            ]
                        }
                        ]
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "button",
                        "action": {
                        "type": "uri",
                        "label": "官網",
                        "uri": "https://www.thatskygame.com/"
                        },
                        "style": "primary",
                        "margin": "sm"
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "uri",
                        "label": "商店",
                        "uri": "https://webshop.thatskygame.com/zh-TW/"
                        },
                        "style": "secondary",
                        "margin": "sm"
                    }
                    ]
                }
            }
            line_flex_str = json.dumps(line_flex_json)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(alt_text='詳細說明', contents=FlexContainer.from_json(line_flex_str))]
                )
            )
        elif text == 'imagemap':
            url1 = url_root + 'static/imagemap'
            url1 = url1.replace("http", "https")
            app.logger.info("url=" + url1)
            #url2 = url_root + 'static/GAME_20240722-170540.mp4'
            #url2 = url2.replace("http", "https")
            url2 = 'https://i.imgur.com/RZmq1u4.mp4'
            app.logger.info("url=" + url2)
            #url3 = url_root + 'static/preview.png'
            #url3 = url3.replace("http", "https")
            url3 = 'https://i.imgur.com/0MOcyJD.png'
            app.logger.info("url=" + url3)

            imagemap_message = ImagemapMessage(
                base_url=url1,
                alt_text='this is an imagemap',
                base_size=ImagemapBaseSize(height=1040, width=1040),
                video=ImagemapVideo(
                    original_content_url=url2,
                    preview_image_url=url3,
                    area=ImagemapArea(
                        x=0, y=540, width=1040, height=500
                    ),
                    external_link=ImagemapExternalLink(
                        link_uri='https://www.thatskygame.com/',
                        label='光遇官網',
                    ),
                ),
                actions=[
                    URIImagemapAction(
                        type = "uri",
                        linkUri='https://forum.gamer.com.tw/B.php?bsn=75719',
                        area=ImagemapArea(
                            x=0, y=0, width=555, height=540
                        )
                    ),
                    MessageImagemapAction(
                        type ="message",
                        text='一個漫畫https://page.kakao.com/content/48772021',
                        area=ImagemapArea(
                            x=555, y=0, width=485, height=540
                        )
                    )
                ]
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[imagemap_message]
                )
            )
        if text == 'quick_reply':
            #postback_icon = url_root + 'static/postback.png'
            #postback_icon = postback_icon.replace("http", "https")
            #message_icon = url_root + 'static/message.png'
            #message_icon = message_icon.replace("http", "https")
            #datetime_icon = url_root + 'static/calendar.png'
            #datetime_icon = datetime_icon.replace("http", "https")
            #date_icon = url_root + 'static/calendar.png'
            #date_icon = date_icon.replace("http", "https")
            #time_icon = url_root + 'static/time.png'
            #time_icon = time_icon.replace("http", "https")
            postback_icon = 'https://i.imgur.com/LLO4uKI.png'
            message_icon = 'https://i.imgur.com/V4QJdDU.png'
            datetime_icon = 'https://i.imgur.com/MBe8kcO.png'
            date_icon = 'https://i.imgur.com/MBe8kcO.png'
            time_icon = 'https://i.imgur.com/5izaTp1.png'

            quickReply = QuickReply(
                items=[
                    QuickReplyItem(
                        action=PostbackAction(
                            label="Postback",
                            data="postback",
                            display_text="postback"
                        ),
                        image_url=postback_icon
                    ),
                    QuickReplyItem(
                        action=MessageAction(
                            label="Message",
                            text="message"
                        ),
                        image_url=message_icon
                    ),
                    QuickReplyItem(
                        action=DatetimePickerAction(
                            label="Date",
                            data="date",
                            mode="date"
                        ),
                        image_url=date_icon
                    ),
                    QuickReplyItem(
                        action=DatetimePickerAction(
                            label="Time",
                            data="time",
                            mode="time"
                        ),
                        image_url=time_icon
                    ),
                    QuickReplyItem(
                        action=DatetimePickerAction(
                            label="Datetime",
                            data="datetime",
                            mode="datetime",
                            initial="2024-01-01T00:00",
                            max="2025-01-01T00:00",
                            min="2023-01-01T00:00"
                        ),
                        image_url=datetime_icon
                    ),
                    QuickReplyItem(
                        action=CameraAction(label="Camera")
                    ),
                    QuickReplyItem(
                        action=CameraRollAction(label="Camera Roll")
                    ),
                    QuickReplyItem(
                        action=LocationAction(label="Location")
                    )
                ]
            )
            
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text='請選擇項目',
                        quick_reply=quickReply
                    )]
                )
            )
        else:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)]
                )
            )

'''@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'postback':
        print('Postback event is triggered')'''

@line_handler.add(PostbackEvent)
def handle_postback(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        postback_data = event.postback.data
        if postback_data == 'postback':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='Postback')]
                )
            )
        elif postback_data == 'date':
            date = event.postback.params['date']
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=date)]
                )
            )
        elif postback_data == 'time':
            time = event.postback.params['time']
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=time)]
                )
            )
        elif postback_data == 'datetime':
            datetime = event.postback.params['datetime']
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=datetime)]
                )
            )
        elif postback_data == 'send_image':
            #url = 'https://drive.google.com/file/d/1uAyHTPwgxL_su4qzFLwHAOiPaR-3kll5/view?usp=drive_link'
            url = 'https://i.imgur.com/qzHBXVE.jpg'
            #url = 'static/20210322_151237.JPG'
            #url = url.replace("http", "https")
            app.logger.info("url=" + url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(original_content_url=url, preview_image_url=url)
                    ]
                )
            )
        elif postback_data=='menu1':
            reply_text = "Hiiii"
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)]
                )
            )
        elif postback_data=='menu2':
            reply_text = "10折"
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)]
                )
            )

def create_rich_menu():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_blob_api = MessagingApiBlob(api_client)

        # Create rich menu
        headers = {
            'Authorization': 'Bearer ' + os.getenv('CHANNEL_ACCESS_TOKEN'),
            'Content-Type': 'application/json'
        }
        body = {
                    "size": {
                        "width": 2500,
                        "height": 1686
                    },
                    "selected": True,
                    "name": "圖文選單 1",
                    "chatBarText": "查看更多資訊",
                    "areas": [
                        {
                        "bounds": {
                            "x": 0,
                            "y": 0,
                            "width": 828,
                            "height": 861
                        },
                        "action": {
                            "type": "postback",
                            "data": "menu1"
                        }
                        },
                        {
                        "bounds": {
                            "x": 828,
                            "y": 0,
                            "width": 874,
                            "height": 870
                        },
                        "action": {
                            "type": "postback",
                            "data": "menu2"
                        }
                        },
                        {
                        "bounds": {
                            "x": 1698,
                            "y": 0,
                            "width": 802,
                            "height": 857
                        },
                        "action": {
                            "type": "postback",
                            "data": "send_image"
                        }
                        },
                        {
                        "bounds": {
                            "x": 0,
                            "y": 866,
                            "width": 836,
                            "height": 820
                        },
                        "action": {
                            "type": "message",
                            "text": "4"
                        }
                        },
                        {
                        "bounds": {
                            "x": 828,
                            "y": 862,
                            "width": 861,
                            "height": 823
                        },
                        "action": {
                            "type": "datetimepicker",
                            "label": "選擇日期和時間",
                            "data": "datetime",
                            "mode": "datetime",
                            "initial": "2025-03-05T20:29",
                            "max": "2027-03-13T20:29",
                            "min": "2024-03-05T20:29"
                        }
                        },
                        {
                        "bounds": {
                            "x": 1689,
                            "y": 857,
                            "width": 811,
                            "height": 829
                        },
                        "action": {
                            "type": "uri",
                            "uri": "https://www.thatskygame.com/"
                        }
                        }
                    ]
                }
        
        response = requests.post('https://api.line.me/v2/bot/richmenu', headers=headers, data=json.dumps(body).encode('utf-8'))
        response = response.json()
        print(response)
        rich_menu_id = response["richMenuId"]
        
        # Upload rich menu image
        with open('static/menu.png', 'rb') as image:
            line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_id,
                body=bytearray(image.read()),
                _headers={'Content-Type': 'image/jpeg'}
            )

        line_bot_api.set_default_rich_menu(rich_menu_id)

create_rich_menu()
if __name__ == "__main__":
    app.run()
