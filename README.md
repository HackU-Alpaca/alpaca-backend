# alpaca-backend

## 環境構築
### Python
```
> python --version
Python 3.9.0
```
ライブラリのインストール
```
pip install -r requirements.txt
```
requirements.txt の更新方法<br>
プロジェクトのルートで以下を実行
```
pipreqs . --force
```

### Heroku
Heroku CLI をインストールして, remote の設定を行なっておく<br>
https://devcenter.heroku.com/ja/articles/heroku-cli

## Herokuへのデプロイ
LINEBOTの動作確認をするためには, コードをHerokuにデプロイする必要があります<br>
※ ローカルでサーバーを立ち上げて確認する方法もある(`ngrok`）が, 不安定でかつめんどくさいので，毎回デプロイしちゃいます！

### ローカルで開発時のデプロイ方法

ブランチを切る
```
git checkout -b feature/x
```
コードを変更するして以下を実行
```
git push (-f) heroku feature/x:main
```
デプロイが完了したらLINEBOTで動作確認を行う<br>
以下のコマンドでログを確認できる
```
heroku logs --tail
```

### 開発終了時のデプロイ方法
`main` ブランチにマージされた時に自動でデプロイするようにしてます！
