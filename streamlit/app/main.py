import streamlit as st
from app.services.sentiment_service import SentimentService

# Streamlitアプリのタイトル
st.title("感情分析アプリ")

# ユーザーにテキスト入力を求める
user_input = st.text_area("ここにテキストを入力してください", "")

# 感情分析
if user_input:
    result = SentimentService().sentiment_sentences([user_input])[0]

    print(result)

    # # 分析結果の表示
    # st.write("### 分析結果")
    # if sentiment > 0:
    #     st.write(f"ポジティブな感情 ({sentiment:.2f})")
    # elif sentiment < 0:
    #     st.write(f"ネガティブな感情 ({sentiment:.2f})")
    # else:
    #     st.write("中立的な感情")
