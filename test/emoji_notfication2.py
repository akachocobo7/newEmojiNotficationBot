# -*- coding: utf-8 -*-

import requests
import json
import enviroment
import sqlite3
import slackweb
from time import sleep



def main():
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


    # slackにつなぐ
    slack = slackweb.Slack(url=enviroment.WEBHOOK_URL)


    # データベースにつなぐ
    dbname = "custom_emojis.db"
    conn = sqlite3.connect(dbname)
    c = conn.cursor()


    # データベースを作ってなければ生成
    c.execute('''CREATE TABLE IF NOT EXISTS custom_emojis (pos text)''')


    '''
    slackで登録されている絵文字を辞書型で取得
    データベースにある絵文字を辞書型から消していく
    消す前にすでに辞書型に絵文字がない場合、slackからその絵文字が消えていることになる
    ので、slackに消えていることを通知
    データベースにある絵文字を全て辞書型から消した後、辞書型に残っている絵文字は
    新しく追加された絵文字なので、追加されていることをslackに通知
    '''
    emoji_dict = json_dict["emoji"]
    for db_emoji in c.execute("SELECT * FROM custom_emojis"):
        # タプル型で取り出されているので適当に処理
        emoji = db_emoji[0]
        # データベースにある絵文字がslackに残っているかを確認
        if emoji in emoji_dict:
            del emoji_dict[emoji]
        else:
            # 消えた絵文字をデータベースから削除
            delete_sql = "DELETE FROM custom_emojis WHERE pos == (?)"
            delete_data = (emoji,)
            c.execute(delete_sql, delete_data)

            # slackから削除された絵文字をslackに通知
            slack.notify(text="emoji :{0}: `{0}` が削除されました...".format(emoji), username="emoji-bot", icon_emoji=":sushi:")

    for emoji_name in emoji_dict:
        # 新しい絵文字をデータベースに追加
        insert_sql = "INSERT INTO custom_emojis (pos) VALUES (?)"
        insert_data = (emoji_name,)
        c.execute(insert_sql, insert_data)

        # 新しく入った絵文字をslackで通知
        slack.notify(text="emoji :{0}: `{0}` が追加されました！".format(emoji_name), username="emoji-bot", icon_emoji=":sushi:")
            
    # 変更を反映
    conn.commit()

    # データベースを閉じる
    conn.close()

if __name__ == "__main__":
    while(1):
        main()
        sleep(300)  # 5分間待ってやる