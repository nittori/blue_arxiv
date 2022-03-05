import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import get_paper
import time
import datetime

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)
# ID of the channel you want to send the message to
channel_id = "<channel id>"#slackのチャンネルID

def post_message(message):
    try:
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=channel_id, 
            text=message
        )
        logger.info(result)
    
    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")

path=os.getcwd()#現在のワーキングディレクトリを取得
print(path)

authors,publish_dates,titles,urls = get_paper.get_paper(path)
num = len(authors)
today = datetime.date.today()#PCの時間
post_message("=======================\n"+\
             f"{today}  number of articles = {num}\n"+\
             "=======================\n")
for i in range(num):
    time.sleep(1)
    message = f"author : {authors[i]}\n"+\
              f"publish_date : {publish_dates[i]}\n"+\
              f"title : {titles[i]}\n"+\
              f"url : {urls[i]}\n"
    post_message(message)

    
    
