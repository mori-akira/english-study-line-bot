import uuid
from typing import Any
from datetime import datetime, timezone
import boto3
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
from boto3.dynamodb.conditions import Attr

dynamodb: DynamoDBServiceResource = boto3.resource("dynamodb")  # type: ignore
user_table = dynamodb.Table("english-study-bot-user")
question_table = dynamodb.Table("english-study-bot-question-history")


def list_user() -> list[dict[str, Any]]:
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


def put_question(user_id: str, question: str):
    item = {
        "question_id": str(uuid.uuid4()),
        "user_id": user_id,
        "question_text": question,
        "question_datetime": datetime.now(timezone.utc).isoformat()
    }
    question_table.put_item(Item=item)
