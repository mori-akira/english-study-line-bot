from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage,
)

from .secrets_manager import get_secret  # type: ignore

secrets = get_secret("englishStudyBot")
access_token = secrets.get("LINE_CHANNEL_ACCESS_TOKEN")
channel_secret = secrets.get("LINE_CHANNEL_SECRET")
configuration = Configuration(access_token=access_token)


def push_message(message: str, to: str):
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
