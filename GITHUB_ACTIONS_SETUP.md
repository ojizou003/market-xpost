# GitHub Actions セットアップガイド

このプロジェクトを GitHub Actions で定期実行するためのセットアップ手順です。

## 前提条件

- GitHub リポジトリにプッシュ済みであること
- `cookies.pkl`ファイルがローカルに存在すること

## セットアップ手順

### 1. cookies.pkl を Base64 エンコードする

以下のコマンドを実行して、`cookies.pkl`を Base64 エンコードします：

```bash
python encode_cookies.py
```

出力された Base64 文字列をコピーしてください。

### 2. GitHub Secrets に設定する

1. GitHub リポジトリのページに移動
2. **Settings** > **Secrets and variables** > **Actions** を選択
3. **New repository secret** をクリック
4. 以下の情報を入力：
   - **Name**: `COOKIES_PKL_BASE64`
   - **Secret**: ステップ 1 でコピーした Base64 文字列を貼り付け
5. **Add secret** をクリック

### 3. ワークフローファイルをコミット・プッシュする

以下のファイルをコミットしてプッシュします：

```bash
git add .github/workflows/scheduled-post.yml
git add x-market.py  # CI環境対応の変更が含まれます
git add encode_cookies.py
git commit -m "Add GitHub Actions workflow for scheduled posting"
git push
```

### 4. 動作確認

#### 手動実行でテスト

1. GitHub リポジトリの **Actions** タブに移動
2. 左側のメニューから **Scheduled Market Post** を選択
3. **Run workflow** ボタンをクリック
4. ワークフローの実行を確認

#### スケジュール実行の確認

- スケジュールは日本時間の月～金の 12:05 に実行されます
- 初回実行は、次のスケジュール時刻まで待つ必要があります
- または、手動実行でテストできます

## スケジュール設定

現在の設定：

- **実行時間**: 日本時間 月～金 12:05
- **UTC 時間**: 03:05（日本時間 = UTC+9）

スケジュールを変更する場合は、`.github/workflows/scheduled-post.yml`の`cron`行を
編集してください。

cron 形式: `分 時 日 月 曜日`

- 曜日: 0=日曜日、1=月曜日、...、6=土曜日

## トラブルシューティング

### cookies.pkl が見つからないエラー

- GitHub Secrets に`COOKIES_PKL_BASE64`が正しく設定されているか確認
- Base64 文字列が正しくコピーされているか確認
- `encode_cookies.py`を再実行して新しい Base64 文字列を生成

### Chrome の起動エラー

- ワークフローログを確認
- `x-market.py`が CI 環境用のオプション（--no-sandbox 等）を使用しているか確認

### スケジュールが実行されない

- GitHub Actions の無料プランでは、リポジトリが 60 日間非アクティブの場合、スケ
  ジュール実行が無効になる可能性があります
- 手動でワークフローを実行して、リポジトリをアクティブに保つことをお勧めします

## セキュリティについて

- `cookies.pkl`は機密情報を含むため、GitHub Secrets に保存してください
- リポジトリに直接コミットしないでください
- `.gitignore`に`cookies.pkl`が含まれていることを確認してください
