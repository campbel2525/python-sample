import typer

from app import models
from app.enums.openai_enums import UseableOpenaiModel
from app.services.langchain_services import LangchainSendChatService
from config.settings import db

app = typer.Typer()


DEFAULT_PROMPT = """
この章について、以下のことを踏まえて、本の紹介ではなく、本に書かれている内容をかなり詳しく、講義して欲しいです
- 日本語でお願いします
- 改行は`\n`でお願いします
- マークダウンを用いてください

下記のような物は必要ないです
- この章を通して〜〜のような本の説明
- 〜〜と紹介されている

翻訳して欲しい内容
```
{book_content}
```
"""


@app.command()
def summaries():
    book_contents = db.query(models.BookContent).all()
    for book_content in book_contents:
        book_content_summary = (
            db.query(models.BookContentSummary)
            .filter(models.BookContentSummary.book_content_id == book_content.id)
            .first()
        )
        if book_content_summary is not None:
            continue

        content = DEFAULT_PROMPT.format(book_content=book_content.content)
        messages = [
            {"role": "human", "content": content},
        ]
        ai_result = LangchainSendChatService(
            model_name=UseableOpenaiModel.GPT_4_TURBO_PREVIEW.value,
            messages=messages,
        ).send_message(max_tokens=4000)

        print(ai_result)

        book_content_summary = models.BookContentSummary()
        book_content_summary.book_content_id = book_content.id
        book_content_summary.content = ai_result
        db.add(book_content_summary)
        db.flush()

    db.commit()


if __name__ == "__main__":
    app()
