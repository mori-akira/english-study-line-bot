from typing import Any
import boto3
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
from boto3.dynamodb.conditions import Attr

dynamodb: DynamoDBServiceResource = boto3.resource("dynamodb")  # type: ignore
user_table = dynamodb.Table("english-study-bot-user")
quiz_table = dynamodb.Table("english-study-bot-quiz-history")


def list_users() -> list[dict[str, Any]]:
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
    return users
