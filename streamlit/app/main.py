import streamlit as st

from app.services.transformer import SentimentService

# Streamlitアプリのタイトル
st.title("感情分析アプリ")


# フォームの作成
with st.form(key="my_form"):
    user_input = st.text_area("テキストを入力してください", "")
    submit_button = st.form_submit_button("送信")


# 結果の表示
if submit_button and user_input:
    result = SentimentService().sentiment_sentences([user_input])[0]
    st.write(f'感情: {result["label"]}, 精度: {int(result["score"] * 100)}%')
