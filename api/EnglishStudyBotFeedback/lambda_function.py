from linebot_query import handle_message


def lambda_handler(event, context):
    headers = event.get("headers", {})
    print(headers)
    signature = headers.get("x-line-signature")
    body = event.get("body", "{}")
    print(body)
    handle_message(body, signature)

    return {
        "statusCode": 200,
    }
