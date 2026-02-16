import uuid
from typing import Any
from datetime import datetime, timedelta, timezone
import boto3
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
from boto3.dynamodb.conditions import Attr, Key

dynamodb: DynamoDBServiceResource = boto3.resource("dynamodb")  # type: ignore
user_table = dynamodb.Table("english-study-bot-user")
question_table = dynamodb.Table("english-study-bot-question-history")


def list_user() -> list[dict[str, Any]]:
    users = []
    response = user_table.scan(
        FilterExpression=Attr("is_valid").eq(True)
    )
    users.extend(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = user_table.scan(
            FilterExpression=Attr("is_valid").eq(True)
        )
        users.extend(response.get("Items", []))
    return users


def get_user(user_id: str):
    response = user_table.query(
        KeyConditionExpression=Key("user_id").eq(user_id),
        Limit=1,
    )
    items = response.get("Items", [])
    user = items[0] if items else None
    return user if user and user["is_valid"] else None


def get_latest_question(user_id: str):
    response = question_table.query(
        KeyConditionExpression=Key("user_id").eq(user_id),
        ScanIndexForward=False,
        Limit=1,
    )
    items = response.get("Items", [])
    return items[0] if items else None


def put_question(user_id: str, question: str):
    now = datetime.now(timezone.utc)
    expire_at = now + timedelta(days=7)

    item = {
        "question_id": str(uuid.uuid4()),
        "user_id": user_id,
        "question_text": question,
        "question_datetime": datetime.now(timezone.utc).isoformat(),
        "ttl": int(expire_at.timestamp()),
    }
    question_table.put_item(Item=item)
