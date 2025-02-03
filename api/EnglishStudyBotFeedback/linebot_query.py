from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from secrets_manager import get_secret  # type: ignore

secrets = get_secret("englishStudyBot")
access_token = secrets.get("LINE_CHANNEL_ACCESS_TOKEN")
channel_secret = secrets.get("LINE_CHANNEL_SECRET")
configuration = Configuration(access_token=access_token)
handler = WebhookHandler(channel_secret)


def push_message(to: str, message: str):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.push_message(
            PushMessageRequest(
                to=to,
                messages=[TextMessage(
                    text=message, quickReply=None, quoteToken=None
                )],
                notificationDisabled=None,
                customAggregationUnits=None,
            )
        )


def handle_message(body, signature):
    handler.handle(body, signature)


@handler.add(MessageEvent, message=TextMessageContent)
def add_handler(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[TextMessage(
                    text="event.message.text", quickReply=None, quoteToken=None,
                )],
                notificationDisabled=None,
            )
        )
