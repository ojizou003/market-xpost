# GitHub Actionsでのスケジュール実行 - 実装計画

## 概要
WindowsタスクスケジューラからGitHub Actionsへの移行により、ローカルPCに依存しない安定した定期実行環境を構築する。

## 実行方式: Dockerコンテナ方式
- 採用理由: ブラウザ環境の完全な制御、バージョン固定による安定性、環境分離
- スケジュール: 月～金曜日、日本時間12時5分（UTC 3時5分）

## ファイル構成
```
project/
├── .github/
│   └── workflows/
│       └── scheduled-post.yml      # GitHub Actionsワークフロー
├── docs/
│   └── github_actions_implementation_plan.md  # 本ファイル
├── Dockerfile                     # Dockerイメージ定義
├── requirements.txt               # Python依存関係
├── x-market.py                   # メインスクリプト（既存）
└── cookies.pkl                   # Xログイン用クッキー（シークレットに登録）
```

## 実装手順

### 1. Dockerfileの作成
- Python 3.11-slimベース
- ChromeブラウザとChromeDriverのインストール
- 必要な依存関係のインストール
- アプリケーションコードの配置

### 2. requirements.txtの作成
- selenium==4.22.0
- その他必要なライブラリ

### 3. GitHub Actionsワークフロー
- トリガー: cron式 `5 3 * * 1-5`（月～金曜日、UTC 3時5分）
- Dockerコンテナでの実行
- タイムアウト設定: 10分
- シークレットからクッキーを読み込み

### 4. シークレット設定
- `COOKIES_DATA`: cookies.pklの内容をBase64エンコードして登録
- 登録手順:
  1. cookies.pklをBase64エンコード
  2. GitHubリポジトリのSettings > Secrets and variables > Actions
  3. New repository secretで登録

## 技術仕様

### スケジュール設定
- 日本時間: 12時5分
- UTC: 3時5分
- 曜日: 月曜日～金曜日
- cron式: `5 3 * * 1-5`

### Docker環境
- ベースイメージ: python:3.11-slim
- Chrome: 最新安定版
- ChromeDriver: Chromeバージョンに対応
- ヘッドレスモードで実行

### エラーハンドリング
- タイムアウト: 10分
- 基本的なエラー処理
- 通知機能はなし（要件により）

## 実装後の確認事項
1. 正常にスケジュール実行されるか
2. Xへの投稿が成功するか
3. エラーが発生した場合のログ確認
4. 実行時間の妥当性

## メンテナンス
- Chromeバージョンアップ時のDockerfile更新
- XのUI変更時のセレクタ修正
- クッキーの有効期限確認（定期的な再登録が必要）
