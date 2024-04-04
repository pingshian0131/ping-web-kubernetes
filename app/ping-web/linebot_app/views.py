import logging

from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from linebot.v3 import WebhookParser
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    AccountLinkEvent,
    ImageMessageContent,
    StickerMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    PushMessageRequest,
)
from linebot.v3.exceptions import InvalidSignatureError

from person.views import get_email_recipient
from linebot_app.models import LineBotUser


logger = logging.getLogger(__name__)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
configuration = Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)


@csrf_exempt
@require_http_methods(["POST"])
def callback(request):
    signature = request.headers["X-Line-Signature"]

    body = request.body.decode("utf-8")
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return HttpResponse(status=400)

    for event in events:
        user_id = event.source.user_id
        user_name = None
        try:
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                res = line_bot_api.get_profile(user_id)
                user_name = res.display_name
            user = LineBotUser(line_user_id=user_id, display_name=user_name)
            logger.warning(user_id)
            user.save()

        except IntegrityError as e:
            logger.warning(f"{str(e)}: {user_id}")

        if isinstance(event, MessageEvent):
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)

                if isinstance(event.message, TextMessageContent):
                    if user_name:
                        text = "已收到您的訊息, 請稍待。"
                        msg = f"{user_name} 已向您傳送訊息： {event.message.text}"
                        source = settings.EMAIL_HOST_USER
                        html_message = render_to_string(
                            "email.html",
                            {"name": user_name, "email": source, "message": msg},
                        )
                        # 寄送郵件
                        send_mail(
                            subject=f"來自 {user_name} 的一則 line 訊息",
                            message=msg,
                            from_email=f"Personal Line Official Account <{source}>",
                            recipient_list=get_email_recipient(),
                            fail_silently=False,
                            html_message=html_message,
                        )

                    else:
                        text = "發生錯誤, 請至 https://pingshian.simplesocool.cc/#contact 留下您的留言, 感謝。"

                else:
                    text = "已收到您的訊息, 但目前僅接受文字訊息, 請至 https://pingshian.simplesocool.cc/#contact 留下您的留言, 感謝。"

                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=text)],
                    )
                )

    return HttpResponse(status=200)
