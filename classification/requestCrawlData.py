import os
import requests
import json
from pprint import pprint

url = "https://www.whsh.tc.edu.tw/ischool/widget/site_news/news_query_json.php"

data = {
    'field': 'time',
    'order': 'DESC',
    'pageNum': '0',
    'maxRows': '15',
    'keyword': '',
    'flock': '',
    'uid': 'WID_0_2_518cd2a7e52b7f65fc750eded8b99ffcc2a7daca',
    'tf': '2',
    'auth_type': 'user'
}

fpath = "./train_corpus/"  # floderPath
if not os.path.exists(fpath):  # 是否存在分词目录，如果没有则创建该目录
    os.makedirs(fpath)

for i in range(1):
    data["pageNum"] = str(i)
    r = requests.post(url, data=data)
    resDict = json.loads(r.text)
    pprint(resDict)
    for row in resDict[1:]:
        print(row["title"])
        fileName = "".join(c for c in row["title"] if c.isalnum())
        # 去除不合法字元
        fileName = fileName[:25] if len(fileName) > 25 else fileName
        # 會有檔名太長問題，取前25字
        with open(fpath + fileName + ".txt", "w") as f:
            f.write(row["title"])
