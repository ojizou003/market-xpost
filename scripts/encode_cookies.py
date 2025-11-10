#!/usr/bin/env python3
"""
クッキーファイルをBase64エンコードするスクリプト
GitHub Actionsのシークレット登録用に使用します。
"""

import base64
import pickle
import os
import sys


def encode_cookies_file(file_path="cookies.pkl"):
    """クッキーファイルをBase64エンコードする"""
    try:
        # クッキーファイルを読み込み
        with open(file_path, "rb") as f:
            cookies_data = pickle.load(f)

        # データを検証
        if not isinstance(cookies_data, list):
            raise ValueError("クッキーデータがリスト形式ではありません")

        print(f"クッキー数: {len(cookies_data)}")

        # クッキーをシリアライズしてBase64エンコード
        serialized_data = pickle.dumps(cookies_data)
        encoded_data = base64.b64encode(serialized_data).decode('utf-8')

        print(f"エンコード完了: {len(encoded_data)} 文字")
        print("=" * 50)
        print("GitHub Actionsのシークレット登録用文字列:")
        print("=" * 50)
        print(encoded_data)
        print("=" * 50)

        return encoded_data

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません")
        print("カレントディレクトリに cookies.pkl ファイルがあることを確認してください")
        sys.exit(1)
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)


def decode_cookies_test(encoded_data):
    """デコードテスト（オプション）"""
    try:
        decoded_data = base64.b64decode(encoded_data)
        cookies = pickle.loads(decoded_data)
        print(f"デコードテスト成功: {len(cookies)} 個のクッキー")
        return True
    except Exception as e:
        print(f"デコードテスト失敗: {e}")
        return False


def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "cookies.pkl"

    print(f"クッキーファイルをエンコードします: {file_path}")

    # ファイル存在確認
    if not os.path.exists(file_path):
        print(f"エラー: ファイルが存在しません: {file_path}")
        sys.exit(1)

    # エンコード実行
    encoded_data = encode_cookies_file(file_path)

    # デコードテスト
    print("\nデコードテストを実行...")
    if decode_cookies_test(encoded_data):
        print("✅ デコードテスト成功 - データは有効です")
    else:
        print("❌ デコードテスト失敗 - データを確認してください")
        sys.exit(1)

    print(f"\n手順:")
    print(f"1. 上記の長い文字列をコピー")
    print(f"2. GitHubリポジトリ > Settings > Secrets and variables > Actions")
    print(f"3. 'New repository secret' をクリック")
    print(f"4. Name: 'COOKIES_DATA'")
    print(f"5. Secret: [コピーした文字列を貼り付け]")
    print(f"6. 'Add secret' をクリック")


if __name__ == "__main__":
    main()