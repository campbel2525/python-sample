from app.services.transformer_services import (
    EmbeddingService,
    SentimentService,
    SummaryService,
)

sentences = [
    "雰囲気が良くて、スタッフさんたちもアットホーム感があってすごくよかったです。髪の性質などを細かく教えてくれたりして、とても勉強にもなりました(*≧∀≦*)ありがとうございました(・∀・)ノ",  # noqa
    "徳島で取り扱いの少ないエアーウェーブvita格安で体験させて頂きました。私の髪はもともと細く、よく傷みやすいのですが、このパーマでは傷みを感じませんでした。カールも柔らかく気にいりました。またお世話になろうと思ってます☆ありがとうございました。",  # noqa
]

x = SummaryService().summary_sentences(sentences)
print(x)

y = EmbeddingService().embedding_sentences(sentences)
print(y)

z = SentimentService().sentiment_sentences(sentences)
print(z)
