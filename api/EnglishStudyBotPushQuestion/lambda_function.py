import boto3
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
from boto3.dynamodb.conditions import Attr

from openai_query import UserInfo, generate_question  # type: ignore
from linebot_query import push_message  # type: ignore


dynamodb: DynamoDBServiceResource = boto3.resource("dynamodb")  # type: ignore
user_table = dynamodb.Table("english-study-bot-user")
quiz_table = dynamodb.Table("english-study-bot-quiz-history")


def lambda_handler(event, context):
    # ユーザ一覧取得
    users = []
    response = user_table.scan(
        FilterExpression=Attr('is_valid').eq(True)
    )
    users.extend(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = user_table.scan(
            FilterExpression=Attr('is_valid').eq(True)
        )
        users.extend(response.get("Items", []))

    # 各ユーザに出題
    for user in users:
        question = generate_question(UserInfo(
            english_word_count_indication=int(
                user.get("english_word_count_indication")
            ),
            english_level=user.get("english_level"),
            purpose=user.get("purpose"),
            occupation=user.get("occupation"),
        ))
        message = (
            "【英訳問題】以下の和文を英訳してください。\n\n"
            f"{question}"
        )
        push_message(message, user.get("user_id"))
