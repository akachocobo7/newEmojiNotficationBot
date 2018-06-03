# -*- coding: utf-8 -*-

import slackweb
import enviroment


if __name__ == "__main__":
    slack = slackweb.Slack(url=enviroment.WEBHOOK_URL)
    slack.notify(text="(ﾉ)`ω´(ヾ)")
