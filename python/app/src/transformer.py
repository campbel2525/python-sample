from app.services import transformer_service

sentences = [
    "雰囲気が良くて、スタッフさんたちもアットホーム感があってすごくよかったです。髪の性質などを細かく教えてくれたりして、とても勉強にもなりました(*≧∀≦*)ありがとうございました(・∀・)ノ",  # noqa
    "徳島で取り扱いの少ないエアーウェーブvita格安で体験させて頂きました。私の髪はもともと細く、よく傷みやすいのですが、このパーマでは傷みを感じませんでした。カールも柔らかく気にいりました。またお世話になろうと思ってます☆ありがとうございました。",  # noqa
]

x = transformer_service.Summary().summary_sentences(sentences)
print(x)

y = transformer_service.Embedding().embedding_sentences(sentences)
print(y)

z = transformer_service.Sentiment().sentiment_sentences(sentences)
print(z)
