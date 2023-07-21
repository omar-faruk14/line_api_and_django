from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Replace 'YOUR_CHANNEL_SECRET' with your actual channel secret
handler = WebhookHandler('f8f64fa9513dbfc006d0c1e44548305b')

@csrf_exempt
def line_webhook(request):
    if request.method == 'POST':
        signature = request.headers['X-Line-Signature']
        body = request.body.decode('utf-8')

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponse(status=400)

        return HttpResponse(status=200)
    elif request.method == 'GET':  # Handle GET requests for webhook verification
        return HttpResponse("Hello, this is your LINE bot webhook.")
    else:
        return HttpResponse(status=405)

