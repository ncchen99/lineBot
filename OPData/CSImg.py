import imgkit
import csv
from OPData import crawlData

# 儲存課表圖片


def storeClassScheduleImg():
    for g in range(1, 4):
        for c in range(1, 21):
            options = {
                'width': 600,
                'encoding': "utf8"
            }
            css = ['OPData/css/common.css', 'OPData/css/864.css']
            imgkit.from_string(crawlData.getClassSchedule(
                str(g*100+c)).replace("big5", "utf-8"), 'ClassScheduleImg/'+str(g*100+c)+'.jpg', options=options, css=css)

# 取得圖片連結


def getImg(className):
    classIndex = ((int(className)//100-1)*20) + (int(className) % 100)
    with open('OPData/classScheduleImgUrl.csv', newline='') as csvfile:
        # 讀取 CSV 檔案內容
        items = list(csv.reader(csvfile))
        # 以迴圈輸出每一列
        print(classIndex)
        return items[int(classIndex)][0]


if __name__ == "__main__":
    print('作為主程序運行')
else:
    print('CSImg...')
