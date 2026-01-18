#!/usr/bin/env bash
# エラーが出たらそこで停止
set -o errexit

# ライブラリのインストール
pip install -r requirements.txt

# 静的ファイルの準備
python manage.py collectstatic --no-input

# データベースの更新
python manage.py migrate
