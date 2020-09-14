import os
import firebase_admin
import time
import datetime
import json
import ast
from bs4 import BeautifulSoup
from firebase_admin import credentials
from firebase_admin import firestore
from OPData import crawlData

# 常數資訊
f = open("./OPData/usefulCategory.json", "r")
# 仔入usefulCategory.json
cateDict = json.loads(f.read())
f.close()
cateToAction = {
    "iPicked": {"tag": "picked", "value": 1, "keyWords": [""]},
    "hotRecently": {"tag": "top", "value": 1, "keyWords": [""]},
    "bus": {"tag": "unitName", "value": "教官室", "keyWords": ["交通車", "搭車", "專車"]},
    "reClass": {"tag": "unitName", "value": "教學組", "keyWords": ["重補修", "重修班"]},
    "reTest": {"tag": "unitName", "value": "試務組", "keyWords": ["補考"]},
    "testNotifications": {"tag": "unitName", "value": "試務組", "keyWords": ["作業考", "假期考", "複習考", "考試範圍"]},
    "giveMoney": {"tag": "unitName", "value": "出納組", "keyWords": ["繳費", "註冊"]},
    "nightStudy": {"tag": "unitName", "value": "圖書館", "keyWords": ["晚自習", "晚自習預約"]},
    "arrangeClass": {"tag": "unitName", "value": "註冊組", "keyWords": ["班級", "班群", "編班"]}
}

# 更新資料


def updateData():
    if time.time() - list(db.collection("lastTimeStore").stream())[0].to_dict()["time"] > 3600:
        storePost(crawlData.getBillboard())

# 移除舊公告


def removeOldPost():
    for post in db.collection(path).stream():
        if time.time() - int(post.to_dict()["crawlTime"]) > 172800:
            db.collection(path).document(post.id).delete()

#　儲存公告至Firebase


def storePost(data):
    for row in data[1:]:
        if row["unit_name"] in cateDict and int(row["clicks"]) > 200:
            doc = {
                "newsId": row["newsId"],
                "crawlTime": time.time(),
                "title": row["title"],
                "postTime": row["time"],
                "clicks": row["clicks"],
                "url": "https://www.whsh.tc.edu.tw/ischool/widget/site_news/news_pop_content.php?newsId="+row["newsId"] + "&bid=0&uid=WID_0_2_518cd2a7e52b7f65fc750eded8b99ffcc2a7daca",
                "unitName": row["unit_name"],
                "top": row["top"],
                "picked": 1
            }
            db.collection(path).document(row["newsId"]).set(doc)
    db.collection("lastTimeStore").document("time").set({"time": time.time()})
    removeOldPost()


# 儲存課表至firebase
# g : grade
# c : class

def storeClassSchedule():
    for g in range(1, 4):
        for c in range(1, 21):
            soup = BeautifulSoup(crawlData.getClassSchedule(
                str(g*100+c)), "html.parser")
            courses = soup.find_all("td", class_="tdColumn")
            cTable = [[] for i in range(0, 6)]
            week = 0
            for course in courses[1:]:
                if len(course.getText()) > 2:
                    cTable[week].append(course.find_all(
                        "a")[0].getText().split()[0])
                else:
                    cTable[week].append(" ")
                week += 1
                week %= 6
            cTable = cTable[::-1]
            doc = [[
                str(i), str(week),
            ] for i, week in enumerate(cTable[1:], start=1)]
            db.collection(classSchedulePath).document(
                str(g*100+c)).set(dict(doc))

# 儲存使用者資訊


def storeUserInfo(userId, classN):
    doc = {
        "userId": userId,
        "classN": classN
    }
    db.collection(userInfoPath).document(userId).set(doc)


# 從firebase讀取資料


def getPosts(category):
    postsList = list()
    for post in list(db.collection(path).stream())[::-1]:
        post = post.to_dict()
        if post[cateToAction[category]["tag"]] == cateToAction[category]["value"] and any(item in post["title"] for item in cateToAction[category]["keyWords"]):
            postsList.append(post)
    return postsList if len(postsList) > 0 else [{"unitName": "挖",
                                                  "title": "👨‍💻目前迷有資料稍後再試ㄛ🤔 尼可以去文華那裡看看有迷有🐂",
                                                  "url": "https://www.whsh.tc.edu.tw/ischool/publish_page/0/"}]

# 取得使用者班級資訊


def getUserInfo(userId):
    classN = "null"
    for user in list(db.collection(userInfoPath).stream()):
        user = user.to_dict()
        if userId == user["userId"]:
            classN = user["classN"]
    return classN


# 取得下一節課
def getNextClassName(classN):
    for cTable in list(db.collection(classSchedulePath).stream()):
        if cTable.id == classN:
            os.environ['TZ'] = 'Asia/Taipei'
            time.tzset()
            dictClassTable = cTable.to_dict()
            if datetime.datetime.today().weekday()+1 > 5:
                return "假日偶不知道餒🐛"
            else:
                timeSegment = [[16, 24, 1], [0, 8, 1], [8, 9, 2], [9, 10, 3], [
                    10, 11, 4], [11, 13, 5], [13, 14, 6], [14, 15, 7], [15, 16, 8]]
                thisDay = ast.literal_eval(
                    dictClassTable[str(datetime.datetime.today().weekday()+1)])
                hour = int(time.strftime('%H'))
                minute = int(time.strftime('%M'))
                next = ""
                if hour > 17:
                    return "沒有課惹喇，明天在查ㄛ🐸"
                for segment in timeSegment:
                    if hour > segment[0] and hour <= segment[1]:
                        if minute > 10 and hour == segment[1]:
                            next = thisDay[segment[2]+1]
                        else:
                            next = thisDay[segment[2]]
                return "下一節課4" + (next if len(next) != 1 else "放學") + "ㄛ🐸"


if __name__ == "__main__":
    pass
else:
    # 引用私密金鑰
    # path/to/serviceAccount.json 請用自己存放的路徑
    cred = credentials.Certificate('./serviceAccountKey.json')
    # 初始化firebase，注意不能重複初始化
    firebase_admin.initialize_app(cred)
    # 初始化firestore
    db = firestore.client()
    path = "posts"
    classSchedulePath = "cs"
    userInfoPath = "user"
