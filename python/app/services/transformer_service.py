from typing import Any, Dict, List


class Summary:
    def summary_sentences(self, sentences: str) -> List[str]:
        from transformers import pipeline

        # 日本語のテキスト要約モデルをロードします。
        summarizer = pipeline("summarization", model="sonoisa/t5-base-japanese")

        # 要約を生成します。ここでは長い日本語のテキストを例としています。
        summaries = summarizer(sentences, min_length=1, max_length=1000)

        return [summary["summary_text"] for summary in summaries]


class Embedding:
    def embedding_sentences(self, sentences: List[str]) -> List[float]:
        # 1. cl-tohoku/bert-base-japanese-whole-word-masking
        # このモデルは全単語マスキングを行ったBERTモデルで、単語レベルでの意味を捉えることができます。
        # したがって、単語の意味が重要なタスク（例えば、文章の意味理解や質問応答など）に適しています。
        #
        # 2. cl-tohoku/bert-base-japanese-char
        # このモデルは文字レベルでBERTモデルを訓練したもので、
        # 細かい文字レベルの情報を必要とするタスク（例えば、品詞タグ付けや固有表現抽出など）に適しています。

        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("cl-tohoku/bert-base-japanese-whole-word-masking")
        # model = SentenceTransformer("cl-tohoku/bert-base-japanese-whole-word-masking")
        sentence_embeddings = model.encode(sentences)

        return [
            sentence_embedding.tolist() for sentence_embedding in sentence_embeddings
        ]


class Sentiment:
    def sentiment_sentences(self, sentences: List[str]) -> List[Dict[str, Any]]:
        from transformers import pipeline

        model_name = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
        classifier = pipeline("sentiment-analysis", model=model_name)

        classifier_results = classifier(sentences)

        return classifier_results
