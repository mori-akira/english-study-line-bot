from openai_query import generate_question  # type: ignore
from linebot_query import push_message  # type: ignore


def lambda_handler(event, context):
    question = generate_question()
    message = (
        "【英訳問題】以下の和文を英訳してください。"
        f"{question}"
    )
    push_message(message, "Uc1d198055dfe857defef8679cf21e8a3")
