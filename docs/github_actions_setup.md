# GitHub Actionsセットアップ手順

## 概要

このドキュメントでは、X（Twitter）への自動投稿をGitHub Actionsで実行するためのセットアップ手順を説明します。

## 前提条件

- GitHubリポジトリが作成済み
- ローカル環境で動作するcookies.pklファイルがある
- Dockerがインストール済み（ローカルテスト用）

## セットアップ手順

### 1. クッキーデータの準備

1. ローカル環境でcookies.pklファイルを準備
2. 以下のコマンドでクッキーデータをBase64エンコード：

```bash
# Linux/macOSの場合
base64 -w 0 cookies.pkl

# Windowsの場合（PowerShell）
[Convert]::ToBase64String([System.IO.File]::ReadAllBytes("cookies.pkl"))
```

3. 出力されたBase64文字列をコピー

### 2. GitHubシークレットの登録

1. GitHubリポジトリで `Settings` > `Secrets and variables` > `Actions` に移動
2. `New repository secret` をクリック
3. 以下の情報を入力：
   - **Name**: `COOKIES_DATA`
   - **Secret**: ステップ1でコピーしたBase64文字列
4. `Add secret` をクリック

### 3. ファイルの配置

リポジトリに以下のファイルが配置されていることを確認：

```
project/
├── .github/
│   └── workflows/
│       └── scheduled-post.yml      # GitHub Actionsワークフロー
├── docs/
│   └── github_actions_setup.md     # 本ファイル
├── Dockerfile                      # Dockerイメージ定義
├── requirements.txt                # Python依存関係
├── x-market-ga.py                  # GitHub Actions対応版スクリプト
└── cookies.pkl                     # ローカルテスト用（Gitには含めない）
```

### 4. .gitignoreの設定

cookies.pklファイルがリポジトリに含まれないように、.gitignoreに追加：

```gitignore
# 既存の設定...
cookies.pkl
```

## ローカルテスト

GitHub Actionsにデプロイする前に、ローカルでDockerイメージをテスト：

```bash
# Dockerイメージをビルド
docker build -t market-xpost .

# ローカル環境でテスト（cookies.pklを使用）
docker run --rm -v $(pwd)/cookies.pkl:/app/cookies.pkl market-xpost

# GitHub Actions環境をシミュレート（Base64エンコードしたクッキーを使用）
COOKIES_BASE64=$(base64 -w 0 cookies.pkl)
docker run --rm -e COOKIES_DATA="$COOKIES_BASE64" -e GITHUB_ACTIONS=true market-xpost
```

## 実行スケジュール

- **実行時間**: 月～金曜日 12:05 JST
- **UTC時間**: 03:05 (月～金曜日)
- **cron式**: `5 3 * * 1-5`
- **タイムアウト**: 15分

## トラブルシューティング

### 1. クッキーの有効期限切れ

クッキーの有効期限が切れた場合：
1. ブラウザでXに手動ログイン
2. 新しいcookies.pklを取得
3. Base64エンコードしてGitHubシークレットを更新

### 2. ヘッドレスモードの問題

ヘッドレスモードでXのUI要素が正しく表示されない場合：
- x-market-ga.py内のセレクタを更新
- ウィンドウサイズやユーザーエージェントを調整

### 3. Chrome/ChromeDriverのバージョン不一致

バージョン不一致の場合：
- Dockerfileを更新してChromeとChromeDriverのバージョンを固定
- 再ビルドしてテスト

### 4. 実行ログの確認

GitHub Actionsの実行ログは以下の手順で確認：
1. GitHubリポジトリの `Actions` タブに移動
2. 該当のワークフロー実行をクリック
3. ジョブのログを確認

## セキュリティについて

- クッキーデータはBase64エンコードされていますが、これは暗号化ではありません
- GitHubシークレットは暗号化されて保存されます
- 定期的にクッキーを更新することを推奨します
- 不正アクセスが疑われる場合は、直ちにシークレットを更新してください

## メンテナンス

- 月に一度程度、ローカルテストを実施して動作確認
- XのUI変更時はセレクタの更新が必要
- Chromeのバージョンアップ時はDockerfileの更新が必要