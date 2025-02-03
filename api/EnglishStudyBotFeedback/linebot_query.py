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

from secrets_manager import get_secret
from dynamodb_query import get_user, get_latest_question, put_question
from openai_query import user_dict_to_user_info, generate_question, generate_feedback

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
    text: str = event.message.text
    user_id: str = event.source.user_id
    reply_token = event.reply_token

    if text == "出題":
        push_new_question(user_id)
    else:
        reply_feedback(user_id, text, reply_token)


def push_new_question(user_id: str):
    user = get_user(user_id)
    question = generate_question(user_dict_to_user_info(user))  # type: ignore
    message = (
        "【英訳問題】以下の和文を英訳してください。\n\n"
        f"{question}"
    )
    push_message(user_id, message)
    put_question(user_id, question)


def reply_feedback(user_id: str, text: str, reply_token: str):
    question = get_latest_question(user_id)
    question = question.get("question_text") if question else ""
    feedback = generate_feedback(question, text)  # type: ignore

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                replyToken=reply_token,
                messages=[TextMessage(
                    text=feedback, quickReply=None, quoteToken=None,
                )],
                notificationDisabled=None,
            )
        )
