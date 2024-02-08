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

## メモ

- app/models のみモジュール化して使用するようにするように統一する？
  - リレーションの関係から、モジュールにした方がいい気がする
- jwt のアルゴリズムを HS256->RS256(cognito と同じ)にする
- 復習を兼ねて terraform のコードを追加する
- ~~シーダーの導入、ファクトリーの導入~~
- ~~DB リセットコマンドの作成~~
- エラーハンドラー追加
- 必要なミドルウェアを設定する
- クラス化する、クラス化しないものを精査する
  - ファイル名がモジュール名を解釈すれば、わざわざ class 化しなくても良い気がする
  - いろいろなコードを見てどちらが python らしいか確認する

## フォルダ構成の説明

factory: database/factories  
migration: database/migrations  
外部と連携するファイル: app/services  
便利な関数(プロジェクト全体で使用が可能なもの): app/helpers  
モデル: app/models  
enum: app/enums  
ログ: logs  
テストケース: tests  
ドキュメントをまとめるフォルダ: doc
