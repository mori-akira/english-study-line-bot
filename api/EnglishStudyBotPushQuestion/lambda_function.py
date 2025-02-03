from dynamodb_query import list_user, put_question  # type: ignore
from openai_query import UserInfo, generate_question  # type: ignore
from linebot_query import push_message  # type: ignore


def lambda_handler(event, context):
    # ユーザ一覧取得
    users = list_user()

    # 各ユーザに出題
    for user in users:
        user_id = user.get("user_id")
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
        push_message(user_id, message)
        put_question(user_id, question)
