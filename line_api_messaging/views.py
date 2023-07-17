import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def line_webhook(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        events = body['events']
        for event in events:
            if event['type'] == 'message' and event['message']['type'] == 'text':
                reply_token = event['replyToken']
                message = event['message']['text']
                send_reply_message(reply_token, message)

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)

def send_reply_message(reply_token, message):
    reply_url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 0Py5K/6Cgg4BenRkERBjSbEjoNvPF/QkCdQs1UM4GFwlqy1TOLTbnnE45U07s9Ym/MrEORTmKal6dqx5cNZXiIxzIeMIyVWiSLfTq3XEqkmFsKnLlF52VFC+56R/BbXsmfKXEenH7TmiFWHRMcEpIQdB04t89/1O/w1cDnyilFU=',
    }
    data = {
        'replyToken': reply_token,
        'messages': [
            {
                'type': 'text',
                'text': message,
            },
        ],
    }
    response = requests.post(reply_url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Failed to send reply message. Status code: {response.status_code}")






