import streamlit as st

from app import models
from config.settings import db
from sqlalchemy.orm import load_only


def handle():
    st.title("要約の表示")

    books = db.query(models.Book).all()
    book_contents = (
        db.query(models.BookContent)
        .options(
            load_only(
                models.BookContent.id,
                models.BookContent.book_id,
                models.BookContent.title,
            )
        )
        .all()
    )
    group_book_id_book_contents = {}
    for book_content in book_contents:
        if book_content.book_id not in group_book_id_book_contents:
            group_book_id_book_contents[book_content.book_id] = []
        group_book_id_book_contents[book_content.book_id].append(book_content)

    with st.form(key="file_results_form"):
        checked_ids = []
        for book in books:
            with st.expander(f"{book.title}"):
                for book_content in group_book_id_book_contents[book.id]:
                    is_checked = st.checkbox(
                        label=book_content.title, key=book_content.id
                    )
                    if is_checked:
                        checked_ids.append(book_content.id)

        # 送信ボタンを追加
        submit_button = st.form_submit_button("要約を表示")

        if submit_button:
            book_contents = (
                db.query(
                    models.BookContentSummary.content.label(
                        "book_content_summary_content"
                    ),
                    models.BookContent.title.label("book_content_title"),
                )
                .join(
                    models.BookContent,
                    models.BookContent.id == models.BookContentSummary.book_content_id,
                )
                .filter(models.BookContent.id.in_(checked_ids))
                .all()
            )

            for book_content in book_contents:
                # st.write(f"## {book_content.book_content_title}")s
                st.write(book_content.book_content_summary_content)

                st.write("# ------------------------------------")
