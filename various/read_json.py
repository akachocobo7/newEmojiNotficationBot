# -*- coding: utf-8 -*-

import requests
import json
import enviroment

if __name__ == "__main__":
    # 絵文字リスト取得用のurl
    url = 'https://slack.com/api/emoji.list'
    # 認証用のパラメータ
    param={"token":enviroment.SLACK_TOKEN}
    # おまじない
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    # 絵文字リストを取得
    json_file = requests.get(url, params=param, headers=headers)
    # 受け取ったjsonは実はstring型になっているのでjsonに変換
    text = json.loads(json_file.text)
    
    # print(text["emoji"])

    for key in text["emoji"]:
        print(key)