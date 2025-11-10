#!/usr/bin/env python3
"""
cookies.pklをBase64エンコードしてGitHub Secrets用の文字列を出力します。

使用方法:
1. このスクリプトを実行: python encode_cookies.py
2. 出力されたBase64文字列をコピー
3. GitHubリポジトリの Settings > Secrets and variables > Actions に移動
4. "New repository secret" をクリック
5. Name: COOKIES_PKL_BASE64
6. Secret: コピーしたBase64文字列を貼り付け
7. "Add secret" をクリック
"""

import base64
import sys
from pathlib import Path

def encode_cookies_file(file_path: str = "cookies.pkl") -> str:
    """cookies.pklファイルをBase64エンコードして返す"""
    cookie_path = Path(file_path)
    
    if not cookie_path.exists():
        print(f"Error: {file_path} が見つかりません", file=sys.stderr)
        sys.exit(1)
    
    with open(cookie_path, "rb") as f:
        cookie_data = f.read()
    
    base64_encoded = base64.b64encode(cookie_data).decode('utf-8')
    return base64_encoded

if __name__ == "__main__":
    try:
        encoded = encode_cookies_file()
        print("\n" + "="*80)
        print("GitHub Secrets用のBase64エンコード文字列:")
        print("="*80)
        print(encoded)
        print("="*80)
        print("\n上記の文字列を GitHub Secrets の COOKIES_PKL_BASE64 に設定してください。")
        print("\n手順:")
        print("1. GitHubリポジトリの Settings > Secrets and variables > Actions に移動")
        print("2. 'New repository secret' をクリック")
        print("3. Name: COOKIES_PKL_BASE64")
        print("4. Secret: 上記の文字列を貼り付け")
        print("5. 'Add secret' をクリック\n")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

