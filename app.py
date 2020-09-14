import os
import configparser
import re
from OPData import fireDB, crawlData, urlShorter, CSImg

# 自己寫的模組operateData
from flask import Flask, request, abort
from datetime import date
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from linebot.models import *

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read("config.ini")

# Channel Access Token
line_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))
# Channel Secret
handler = WebhookHandler(config.get("line-bot", "channel_secret"))

# 常數資訊
postCategory = [["偶挑的🦄", "最近熱門🐞", "考試通知🐂"],
                ["重補修🐛", "補考通知🐡", "交通車🚌"],
                ["繳錢🐻", "晚自習🎓", "編班🤑"]]
cateTrans = {"偶挑的🦄": "iPicked", "最近熱門🐞": "hotRecently", "考試通知🐂": "testNotifications",
             "重補修🐛": "reClass", "補考通知🐡": "reTest", "交通車🚌": "bus",
             "繳錢🐻": "giveMoney", "晚自習🎓": "nightStudy", "編班🤑": "arrangeClass"}

# 變數紀錄
replyAns = 0

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=1)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# 回覆圖片訊息


def replyImgMsg(event, url):
    message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
    )
    line_bot_api.reply_message(event.reply_token, message)


# 回覆訊息函式
def replyMsg(event, msg):
    message = TextSendMessage(msg)
    line_bot_api.reply_message(event.reply_token, message)


# 回覆按鈕介面訊息
def replyBtnMsg(event, imgUrl, title, text, *args):
    message = TemplateSendMessage(
        alt_text="🍫",
        template=ButtonsTemplate(
            thumbnail_image_url=imgUrl,
            title=title,
            text=text,
            actions=[MessageTemplateAction(
                label=e,
                text=e,
            ) for e in args],
        ),
    )
    line_bot_api.reply_message(event.reply_token, message)


# 回覆多個按鈕界面訊息
def replyCarouselMsg(event, imgUrl, title, text, btnText):
    message = TemplateSendMessage(
        alt_text="🐻",
        template=CarouselTemplate(columns=[
            CarouselColumn(
                thumbnail_image_url=imgUrl[i],
                title=title[i],
                text=text[i],
                actions=[
                    MessageTemplateAction(label=e, text=e) for e in btnText[i]
                ],
            ) for i in range(len(imgUrl))
        ]),
    )
    line_bot_api.reply_message(event.reply_token, message)


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global replyAns
    if "學測" in event.message.text or "學測剩幾天🐖" == event.message.text:
        if (date(2021, 1, 22) - date.today()).days > 0:
            replyMsg(
                event,
                "葛膜🍄🐻📺🀄 " + " 距離學測剩下 " + str(
                    (date(2021, 1, 22) - date.today()).days) + " 天惹😭",
            )
        else:
            replyMsg(event, "葛膜🍟 指考加油喇😲")
        replyAns = 0
    elif event.message.text == "尼整理的學校公佈欄💊":
        replyCarouselMsg(
            event,
            ["https://cdn.pixabay.com/photo/2020/06/26/00/25/summer-5341326_960_720.jpg",
             "https://cdn.pixabay.com/photo/2020/09/05/22/37/raspberries-5547660_1280.jpg",
             "https://cdn.pixabay.com/photo/2020/05/31/15/31/migratory-birds-5242969_1280.jpg"],
            ["阿🧤尼想看葛膜🕶️", "阿🧤尼想看葛膜👓", "阿🧤尼想看葛膜🕶️"],
            ["比較有用ㄉ東西🦄", "可能有用ㄉ東西🐴", "可能有用ㄉ東西🦧"],
            postCategory
        )
        replyAns = 0
    elif any(event.message.text in item for item in postCategory):
        replyMsg(
            event,
            "最近" + event.message.text + "ㄉ🐻\n" + "".join("『" + s["unitName"]+"』 " + s["title"] + "\n" + urlShorter.makeShorten(s["url"])+"\n"
                                                         for s in fireDB.getPosts(cateTrans[event.message.text])),
        )
        replyAns = 0
    elif (re.match(r"[1-3][0-1][0-9]", event.message.text) and not re.match(r"[1-3][0][0]", event.message.text)) or re.match(r"[1-3][2][0]", event.message.text):
        if replyAns == 1:
            fireDB.storeUserInfo(event.source.user_id, event.message.text)
            # 從課表設定
            replyImgMsg(event, CSImg.getImg(event.message.text))
        elif replyAns == 2:
            fireDB.storeUserInfo(event.source.user_id, event.message.text)
            # 從設定班級設定
            replyMsg(event, "OK😎可以開始查東西惹")
        elif replyAns == 3:
            fireDB.storeUserInfo(event.source.user_id, event.message.text)
            # 從下節課設定
            replyMsg(event, fireDB.getNextClassName(
                fireDB.getUserInfo(event.source.user_id)))
        else:
            replyImgMsg(event, CSImg.getImg(event.message.text))
        replyAns = 0
    elif any(item in event.message.text for item in ["下一節課4葛膜🐂", "下一節", "下節課", "等一下上"]):
        if fireDB.getUserInfo(event.source.user_id) != "null":
            replyMsg(event, fireDB.getNextClassName(
                fireDB.getUserInfo(event.source.user_id)))
            replyAns = 0
        else:
            replyMsg(event, "尼4幾班ㄉ🦙 格式如:308")
            replyAns = 3
    elif event.message.text == "設定班級🦀":
        replyMsg(event, "尼4幾班ㄉ🦙 格式如:308")
        replyAns = 2
    elif any(item in event.message.text for item in ["偶的課表🍭", "課表"]):
        if fireDB.getUserInfo(event.source.user_id) != "null":
            replyImgMsg(event, CSImg.getImg(
                fireDB.getUserInfo(event.source.user_id)))
            replyAns = 0
        else:
            replyMsg(event, "尼4幾班ㄉ🦙 格式如:308")
            replyAns = 1
    elif any(item in event.message.text for item in ["葛膜", "膈哞", "葛模", "隔膜"]):
        replyMsg(event, "葛膜葛膜🐻")
        replyAns = 0
    else:
        replyBtnMsg(
            event,
            "https://cdn.pixabay.com/photo/2020/08/31/09/33/beach-5531919_1280.jpg",
            "殘酷4選一🤢",
            "尼要看葛膜東東餒👩🏼‍🔧",
            "尼整理的學校公佈欄💊",
            "偶的課表🍭",
            "下一節課4葛膜🐂",
            "設定班級🦀"
        )
        #   "學測剩幾天🐖",
        replyAns = 0
    fireDB.updateData()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
