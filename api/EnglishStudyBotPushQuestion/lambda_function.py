from openai_query import generate_question  # type: ignore
from linebot_query import push_message  # type: ignore


def lambda_handler():
    question = generate_question()
    push_message(question, "Uc1d198055dfe857defef8679cf21e8a3")
