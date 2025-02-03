from dynamodb_query import list_user, put_question  # type: ignore
from openai_query import UserInfo, generate_question  # type: ignore
from linebot_query import push_message  # type: ignore


def lambda_handler(event, context):
    # ユーザ一覧取得
    users = list_user()

    # 各ユーザに出題
    for user in users:
        user_id: str = user.get("user_id")  # type: ignore
        question = generate_question(UserInfo(
            english_word_count_indication=int(
                user.get("english_word_count_indication")  # type: ignore
            ),
            english_level=user.get("english_level"),  # type: ignore
            purpose=user.get("purpose"),  # type: ignore
            occupation=user.get("occupation"),  # type: ignore
        ))
        message = (
            "【英訳問題】以下の和文を英訳してください。\n\n"
            f"{question}"
        )
        push_message(user_id, message)
        put_question(user_id, question)
