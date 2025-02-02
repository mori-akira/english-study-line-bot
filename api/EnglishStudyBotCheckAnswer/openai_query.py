from openai import OpenAI


def generate_question(api_key: str):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o",
        store=True,
        messages=[
            {
                "role": "system",
                "content": (
                    "あなたは、日本人に英語を教える教師です。"
                    "毎日決まった時間に英訳問題を出題し、回答のフィードバックを送ります。"
                    "ユーザ毎に以下の条件が与えられるので、英語に翻訳する問題文となる和文を生成してください。\n"
                    "- 英単語数の目安\n"
                    "- 英語レベル (小中学生 / 高校生 / 大学生 / ビジネス)\n"
                    "- 学習目的 (日常会話 / ビジネス / 旅行 / TOEIC)\n"
                    "- 職業\n"
                    "なお、出力された文字列をシステムで処理するため、出力は問題文のみとし余計な装飾はしないでください。"
                    "また、出題は単なる日本文としてください。"
                ),
            },
            {
                "role": "user",
                "content": (
                    "英単語数の目安: 20\n"
                    "英語レベル: 大学生\n"
                    "学習目的: ビジネス\n"
                    "職業: システムエンジニア"
                ),
            },
        ],
        temperature=0.7,
    )
    content = completion.choices[0].message.content
    return content.strip() if content else ""


def feedback(api_key: str, question: str, answer: str):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o",
        store=True,
        messages=[
            {
                "role": "system",
                "content": (
                    "あなたは、日本人に英語を教える教師です。"
                    "毎日決まった時間に英訳問題を出題し、回答のフィードバックを送ります。"
                    "出題された和文とユーザが英訳した回答が与えられるため、フィードバックを生成してください。\n"
                    "なお、フィードバックは主に日本語とし、最終的に模範解答となる英文を示してください。"
                    "ただし、回答が十分良いものであれば無理に指摘せず、ユーザを賞賛してください。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"出題: {question}\n"
                    f"回答: {answer}"
                ),
            },
        ],
        temperature=0.7,
    )
    content = completion.choices[0].message.content
    return content.strip() if content else ""
