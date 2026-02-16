import os
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

from dynamodb_query import get_user, get_latest_question, put_question
from openai_query import user_dict_to_user_info, generate_question, generate_feedback

access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
channel_secret = os.environ.get("LINE_CHANNEL_SECRET")
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
    text: str = event.message.text
    user_id: str = event.source.user_id
    reply_token = event.reply_token

    if text == "出題":
        _push_new_question(user_id)
    else:
        _reply_feedback(user_id, text, reply_token)


def _push_new_question(user_id: str):
    user = get_user(user_id)
    if not user:
        return
    question = generate_question(user_dict_to_user_info(user))  # type: ignore
    message = (
        "【出題】\n"
        "以下の和文を英訳してください。\n\n"
        f"{question}"
    )
    push_message(user_id, message)
    put_question(user_id, question)


def _reply_feedback(user_id: str, text: str, reply_token: str):
    user = get_user(user_id)
    if not user:
        return
    question = get_latest_question(user_id)
    question = question.get("question_text") if question else ""
    feedback = generate_feedback(question, text)  # type: ignore
    message = (
        "【フィードバック】\n\n"
        f"{feedback}"
    )

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                replyToken=reply_token,
                messages=[TextMessage(
                    text=message, quickReply=None, quoteToken=None,
                )],
                notificationDisabled=None,
            )
        )
