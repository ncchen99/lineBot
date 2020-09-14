import requests
import json
from pprint import pprint

# 取得課表


def getClassSchedule(className):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'cookie': 'selWindow=Left; selArrange=R; ASPSESSIONIDASQBDSCT=DCMHOIPAOICDMEDBFNCCINGE; ASPSESSIONIDCSSCATDS=FCLNHNBBDIBEMCNBCHELPKCM; ASPSESSIONIDCSRAASDS=NHFPJLKCLIFFBEMCOOHNCADL; ASPSESSIONIDASRBCTDT=PCJFMCFDAANAAKHNPIHEENNM; ASPSESSIONIDAQSBDTDS=BFIHDOPDEJNCCDDIKAOHGCOF; ASPSESSIONIDCQSDASCT=NBGJMBABMDNNHDDPIBOGGAOG; ASPSESSIONIDCSSDATDT=CIEPLNBCIJPJCHMIIEMGAMLB'}
    url = "https://class.whsh.tc.edu.tw/109-1/down.asp?sqlstr=" + \
        str(className)+"&type=class&class=&weekno=undefined&selArrange=R&selWindow=Left"
    r = requests.get(url, headers=headers)
    r.encoding = 'big5'
    return r.text

#　取得公告欄


def getBillboard():
    url = "https://www.whsh.tc.edu.tw/ischool/widget/site_news/news_query_json.php"
    data = {
        'field': 'time',
        'order': 'DESC',
        'pageNum': '0',
        'maxRows': '30',
        'keyword': '',
        'uid': 'WID_0_2_518cd2a7e52b7f65fc750eded8b99ffcc2a7daca',
        'tf': '2',
        'auth_type': 'user'
    }
    r = requests.post(url, data=data)
    resDict = json.loads(r.text)
    return resDict


if __name__ == "__main__":
    print('作為主程序運行')
else:
    print('初始化...')
