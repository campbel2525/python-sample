import streamlit as st

from app import models
from app.services.file_services import PdfStreamService
from config.settings import db


def handle():
    st.title("ファイルアップロード")

    with st.form(key="demo1_form"):
        book_title = st.text_input("書籍名を入力してください", "")
        book_category = st.text_input("カテゴリを入力してください", "")
        chapter_titles = st.text_input(
            "ファイルごとの章名をカンマ区切りで入れてください", ""
        )

        uploaded_files = st.file_uploader(
            "ファイルを選択してください",
            type=["pdf", "txt"],
            accept_multiple_files=True,
        )
        submit_button1 = st.form_submit_button("送信")

        chapter_title_array = chapter_titles.split(",")
        if submit_button1 and uploaded_files:

            book = models.Book()
            book.title = book_title
            book.category = book_category
            db.add(book)
            db.flush()

            for index, uploaded_file in enumerate(uploaded_files):
                if uploaded_file.type == "application/pdf":
                    file_contents = PdfStreamService(
                        uploaded_file.read()
                    ).get_documents()

                elif uploaded_file.type == "text/plain":
                    file_contents = uploaded_file.getvalue().decode("utf-8")

                if not file_contents:
                    continue

                # file_contents = file_contents.replace("\n", "<br>")

                chapter_title = uploaded_file.name.split(".")[0]
                if len(chapter_title_array) > index + 1:
                    chapter_title = chapter_title_array[index]

                book_content = models.BookContent()
                book_content.book_id = book.id
                book_content.sort = index + 1
                book_content.chapter_title = chapter_title
                book_content.content = file_contents
                book_content.file_name = uploaded_file.name
                book_content.file_type = uploaded_file.type
                book_content.file_size = uploaded_file.size
                db.add(book_content)
                db.flush()

            db.commit()

    # db.close()
