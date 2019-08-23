import pickle
import numpy as np

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter


SLACK_TOKEN = "xoxb-672132413312-731749089136-zv2DkNPz7HsHgMq5hvn1vIVa"
SLACK_SIGNING_SECRET = "593460215039d772d31b544c37a49f10"

app = Flask(__name__)


slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

# Req. 2-1-1. pickle로 저장된 model.clf 파일 불러오기
with open('model.clf', 'rb') as fout:
    data = pickle.load(fout)

print(data.coef_)

# Req. 2-1-2. 입력 받은 광고비 데이터에 따른 예상 판매량을 출력하는 lin_pred() 함수 구현
def lin_pred(test_str):

    test_str = test_str.replace("<@UMHN12M40> ", "")
    arr = test_str.split(" ")
    result = (float(arr[0]) * data.coef_[0][0]) + (float(arr[1]) * data.coef_[0][1]) + (
                float(arr[2]) * data.coef_[0][2]) + data.intercept_[0]
    return result

# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    keywords = lin_pred(text)
    slack_web_client.chat_postMessage(
        channel=channel,
        text=keywords
    )

@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"

if __name__ == '__main__':
    app.run()
