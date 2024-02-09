import typer

from app import models
from app.enums.openai_enums import UseableOpenaiModel
from app.services.langchain_services import LangchainSendChatService
from config.settings import db

app = typer.Typer()


@app.command()
def summaries():
    book_contents = db.query(models.BookContent).all()
    for book_content in book_contents:

        messages = [
            {"role": "human", "content": book_content.content},
        ]
        content = LangchainSendChatService(
            model_name=UseableOpenaiModel.GPT_4_1106_PREVIEW.value,
            messages=messages,
        ).send_message()

        book_content_summary = models.BookContentSummary()
        book_content_summary.book_content_id = book_content.id
        book_content_summary.content = content
        db.add(book_content_summary)
    db.commit()


if __name__ == "__main__":
    app()
