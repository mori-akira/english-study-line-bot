from linebot_query import handle_message


def lambda_handler(event, _):
    headers = event.get("headers", {})
    signature = headers.get("x-line-signature")
    body = event.get("body", "{}")
    print(f"headers: {headers}")
    print(f"body: {body}")
    handle_message(body, signature)

    return {
        "statusCode": 200,
    }
