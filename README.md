# newEmojiNotficationBot

## 使い方

- python3をインストール

- ライブラリ`slackweb`をインストール

- SLACKのレガシートークンを取得

https://api.slack.com/custom-integrations/legacy-tokens から取得

- webhookの設定

https://slack.com/services/new/incoming-webhook から botが報告するチャンネルを設定し、インテグレーションを追加
また、Webhook URLを控えておく

- clone
```
$ git clone https://github.com/chocobo777/newEmojiNotficationBot.git
```

- 環境変数の設定
```
$ cd newEmojiNotficationBot
$ vi enviroment.py
```

レガシートークン と WebHookURL を設定
```
SLACK_LEGACY_TOKEN="***************************************************************************"
WEBHOOK_URL="**********************************************"
```

- init.pyを実行
```
$ python3 init.py
```

- emoji_noification.pyを実行
```
$ python3 emoji_notfication.py
```