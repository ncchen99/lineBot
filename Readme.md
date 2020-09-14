# 我的第一個 lineBot🍔

> 非常感謝 [honor](https://github.com/honor2016tw) 教我用 requests 乾淨俐落的抓公佈欄和課表 🤓 　還有 [taro](https://github.com/taro0513) 和偶一起討論

> lineBot 的部份是參考北科程式設計研究社[韋辰](https://github.com/yaoandy107/line-bot-tutorial)前輩的[教學](https://blackmaple.me/line-bot-tutorial/)

> 文字分類本來是看[Xiangguo Sun](https://github.com/sunxiangguo/chinese_text_classification)所編寫的工程文件：[python 中文文字分類](https://blog.csdn.net/github_36326955/article/details/54891204)依此教學文章修改作者的程式而來的。

但是後來發現效果並沒有到很理想，所以直接使用學校公佈欄ㄉ處室和關鍵字加以分類，結果還不錯
陸續增加幾個類別方便大家查詢 🐞

比較特別的是資料都是存在功能簡單的 firestore 那裡的

## 🍆 格式大概長醬子：

| 使用者資訊 | 上次儲存時間  |  公告 | 課表 |
| ---------- | :-----------: | ----: | ---- |
| user       | lastTimeStore | posts | cs   |

| ![](https://i.imgur.com/tEi6Ixr.png) | ![](https://i.imgur.com/0uTHwgE.png) |
| ------------------------------------ | ------------------------------------ |


每次撈資料都要全部拿出來檢查，好像沒有其他方法，時間複雜度很差，不過資料不多還好 🙁

## 🦚 學校網頁是 ischool ㄉ好像都可以用

改一下 `OPData/crawlData.py` 當中的 `uid` 參數和 post 的 `url` 即可 🦄

## 🍖 爬學校課表注意事項

需要塞 cookie 給它，目前還沒看出 cookie 的規律，所以每次更新課表都需要複製新的 cookie🐖

## 目前是佈署到 heroku

想要自己用一個記得 clone 下來之後要新增這兩個檔案：`config.ini` 、　`serviceAccountKey.json`

1.  `config.ini`

    ```ini
    [line-bot]
    channel_access_token = 你的channel_access_token
    channel_secret = 你的channel_secret
    ```

2.  `serviceAccountKey.json`

    ```json
    {
      "type": "service_account",
      "project_id": "你的firestore資訊",
      "private_key_id": "",
      "private_key": "",
      "client_email": "",
      "client_id": "",
      "auth_uri": "",
      "token_uri": "",
      "auth_provider_x509_cert_url": "",
      "client_x509_cert_url": ""
    }
    ```

## 執行畫面

![](https://i.imgur.com/UbyjevN.jpg)

<!--
結合[Selenium](https://github.com/SeleniumHQ/selenium)與[Beautiful Soup](https://github.com/waylan/beautifulsoup)爬取學校網頁的公告，使用TF-IDF加權技術，對每則公告做分類，回覆有用資訊給使用者。

其中使用[jieba](https://github.com/fxsjy/jieba)做為中文的分詞工具，接著使用 Scikit-Learn 函式庫中的[Bunch](https://github.com/dsc/bunch)數據結構來表示資料集，最後把資料集轉換至 TF-IDF 詞向量空間，對測試資料做預測。　-->
