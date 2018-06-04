# -*- coding: utf-8 -*-

import requests
import json
import enviroment
import pandas as pd
import MeCab
import sqlite3
import re


if __name__ == "__main__":
    # 絵文字リスト取得用のurl
    url = 'https://slack.com/api/emoji.list'
    # 認証用のパラメータ
    param={"token":enviroment.SLACK_LEGACY_TOKEN}
    # おまじない
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    # 絵文字リストを取得
    file = requests.get(url, params=param, headers=headers)
    # 受け取ったjsonは実はstring型に変換されているのでjsonに変換
    json_dict = json.loads(file.text)


    # データベースにつなぐ
    dbname = "custom_emojis.db"
    conn = sqlite3.connect(dbname)
    c = conn.cursor()


    # データベースを作ってなければ生成
    c.execute('''CREATE TABLE IF NOT EXISTS custom_emojis (pos text)''')


    for emoji_name in json_dict["emoji"]:
        # すでにデータベースに入っているか検索
        c.execute("SELECT * FROM custom_emojis WHERE pos=?", (emoji_name,))
        if c.fetchone() == None:
            # 入っていない時は挿入
            insert_sql = "INSERT INTO custom_emojis (pos) VALUES (?)"
            insert_data = (emoji_name,)
            c.execute(insert_sql, insert_data)
            
    # 変更を反映
    conn.commit()

    for i in c.execute('select * from custom_emojis'):
        print(i)

    # データベースを閉じる
    conn.close()
