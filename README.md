## 概要

python とデータベースの docker 環境です  
m1 macbook では動作確認済みです

想定エディタ: vscode or cursor  
デバッグ: debugpy  
python バージョン: 3.10  
ライブラリ管理: pipenv  
orm: sqlqlchemy  
mysql: 8.0  
mysql の ipass やポートなどは`python/.env.example`を参照してください  
フォーマッターなど: flake8, mypy, black, isort

## 環境構築方法

手順 1
pc に docker が入っていない方は docker のインストールをしてください  
公式サイト: https://www.docker.com/ja-jp/

手順 2  
下記のコマンドを実行して docker の開発環境を作成します

```
make init
```

### コマンドについて

Makefile によく使うコマンドをまとめています

### 開発環境を止める

下記のコマンドを実行します

```
make down
```

### 開発環境を立ち上げる

下記のコマンドを実行します

```
make up
```

### 開発環境を削除する

下記のコマンドを実行します

```
make destroy
```

## ライブラリのインストール方法

docker を利用しているので モジュールをインストールする場合はコンテナの中に入ってインストールする必要があります  
またモジュールの管理に pipenv を使用しているため特別な方法でインストールを実行する必要があります  
以下にその方法を説明します

例  
numpy をインストールする方法

手順 1  
下記のコマンドでコンテナの中に入ります

```
make shell
```

手順 2  
下記のコマンドで numpy をインストールします

```
pipenv install numpy
```

## python の実行方法

docker を利用しているので python を実行する場合は、コンテナの中に入って python を実行する必要があります。  
またモジュールの管理に pipenv を使用しているため特別な方法で python を実行する必要があります  
以下にその方法を説明します

例  
`python/sample.py`を実行する場合

手順 1  
下記のコマンドでコンテナの中に入ります

```
make shell
```

手順 2  
下記のコマンドで `python/sample.py`を実行します

```
pipenv run python app/sample.py
```

python フォルダが docker の app にマウントしているため実行する python のファイルは`python/sample1.py`ではなく`sample1.py`となります。

## vscode で debugpy によるデバッグの方法

vscode で debugpy によるデバッグ方法を説明します  
参考: https://atmarkit.itmedia.co.jp/ait/articles/2107/16/news029.html

`python/sample.py` をデバッグする方法

手順 1  
vscode のプラグインの XXX をインストールします

手順 2  
`python/sample.py` のデバッグのコメントアウトを外します

手順 3  
「python の実行方法」を参考に実行し `python/sample.py` を実行します

手順４  
コンソールを確認すると

```
waiting ...
```

と表示されていることを確認

手順 5  
自分がデバッグを開始したい箇所にブレークポイントをセットします

手順 6  
F5 のキーを押します  
デバッグが開始されます。

## python コードのフォーマット、静的解析について

python にはプログラミングコードの品質を保つため、お勧めされているコードフォーマットや静的解析があります。  
下記のコマンドを実行することで python 配下の python コードが自動で整形がされ、また静的解析が行われます。

```
make format
```

## マイグレーションについて

`app/models`配下に定義してあるテーブルが管理されます  
新しくモデルのファイルを追加した場合は`app/models/__init__.py`に追記をする必要があります  
下記のコマンドを実行することでマイグレーションとマイグレートが実行できます

### マイグレーション作成

```
pipenv run alembic revision --autogenerate -m 'comment'
```

### マイグレート

```
pipenv run alembic upgrade head
```
