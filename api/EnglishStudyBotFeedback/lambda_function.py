import json


def lambda_handler(event, context):
    # headers = event.get("headers", {})

    body = event.get("body", "{}")
    try:
        body_json = json.loads(body)
    except json.JSONDecodeError:
        body_json = {"error": "Invalid JSON"}

    return {
        "statusCode": 200,
        "body": json.dumps(body_json)
    }
