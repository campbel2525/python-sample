import streamlit as st

from app import models
from app.services.file_services import PdfStreamService
from config.settings import db


def handle():
    st.title("ファイルアップロード")
    st.write("1回のアップロードで1冊の本を登録できます。")
    st.write("1冊の本は章ごとに手動で分割して順番通りに選択してください。")
    st.write("要約の実行は別のコマンドで行うため担当者に連絡してください。")

    with st.form(key="file_uploads_form1"):
        book_title = st.text_input("(必須)書籍名を入力してください", "")
        book_category = st.text_input("(必須)カテゴリを入力してください", "")
        titles = st.text_input(
            "ファイルごとの章名をカンマ区切りで入れてください。指定しないとファイル名が入ります",
            "",
        )

        uploaded_files = st.file_uploader(
            "ファイルを選択してください。順番通りに選択してください。",
            type=["pdf", "txt"],
            accept_multiple_files=True,
        )
        submit_button1 = st.form_submit_button("送信")

        title_array = titles.split(",")
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

                title = uploaded_file.name.split(".")[0]
                if len(title_array) > index + 1:
                    title = title_array[index]

                book_content = models.BookContent()
                book_content.book_id = book.id
                book_content.sort = index + 1
                book_content.title = title
                book_content.content = file_contents
                book_content.file_name = uploaded_file.name
                book_content.file_type = uploaded_file.type
                book_content.file_size = uploaded_file.size
                db.add(book_content)
                db.flush()

            db.commit()

    # db.close()
