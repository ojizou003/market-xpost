# x-market-ga.py - GitHub Actions対応版
import os
import pickle
import base64
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def setup_chrome_options():
    """Chromeオプションを設定"""
    options = Options()

    # ヘッドレスモード
    options.add_argument("--headless")

    # GitHub Actions環境向け設定
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # ユーザーエージェント設定
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    return options


def load_cookies():
    """クッキーを読み込む"""
    # GitHub Actions環境の場合はBase64デコード
    if os.getenv("GITHUB_ACTIONS"):
        cookies_b64 = os.getenv("COOKIES_DATA")
        if not cookies_b64:
            raise ValueError("COOKIES_DATA環境変数が設定されていません")
        cookies_data = base64.b64decode(cookies_b64)
        return pickle.loads(cookies_data)
    else:
        # ローカル環境の場合はファイルから読み込み
        with open("cookies.pkl", "rb") as f:
            return pickle.load(f)


def get_market_data(browser):
    """野村證券から市場データを取得"""
    try:
        market_url = 'https://www.nomura.co.jp/market/conditions/'

        browser.get(market_url)

        # 要素が表示されるまで待機
        wait = WebDriverWait(browser, 20)

        nikkei_element = wait.until(EC.presence_of_element_located((By.ID, 'ni225')))
        nikkei = nikkei_element.text.replace('\n', '  ').replace('（', '(').replace('）', ')')

        dow_element = wait.until(EC.presence_of_element_located((By.ID, 'dji')))
        dow = dow_element.text.replace('\n', '  ').replace('（', '(').replace('）', ')')

        kawase_element = wait.until(EC.presence_of_element_located((By.ID, 'usd')))
        kawase = kawase_element.text.replace('\n', '  ').replace('（', '(').replace('）', ')')

        return nikkei, dow, kawase

    except TimeoutException as e:
        print(f"市場データ取得タイムアウト: {e}")
        raise
    except Exception as e:
        print(f"市場データ取得エラー: {e}")
        raise


def post_to_x(browser, message, cookies):
    """Xに投稿する"""
    try:
        X_url = 'https://x.com'

        browser.get(X_url)

        # クッキーを設定
        for cookie in cookies:
            try:
                browser.add_cookie(cookie)
            except Exception as e:
                print(f"クッキー設定エラー: {e}")
                continue

        # ページを再読み込みしてログイン状態を確認
        browser.get(X_url)

        # 投稿フォームが表示されるまで待機
        wait = WebDriverWait(browser, 20)

        # 複数のセレクタを試して投稿フォームを見つける
        post_selectors = [
            'public-DraftStyleDefault-block.public-DraftStyleDefault-ltr',
            '[data-testid="tweetTextarea_0"]',
            '[role="textbox"]',
            'textarea[aria-label*="投稿"]'
        ]

        post_element = None
        for selector in post_selectors:
            try:
                post_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                break
            except TimeoutException:
                continue

        if not post_element:
            raise ValueError("投稿フォームが見つかりませんでした")

        # メッセージを入力
        post_element.clear()
        post_element.send_keys(message)
        sleep(2)

        # 投稿ボタンを探してクリック
        post_button_selectors = [
            'button[data-testid="tweetButtonInline"]',
            'button[aria-label*="投稿"]',
            'button.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-1cwvpvk.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l',
            '[role="button"][data-testid="tweetButton"]'
        ]

        post_button = None
        for selector in post_button_selectors:
            try:
                post_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                break
            except TimeoutException:
                continue

        if not post_button:
            raise ValueError("投稿ボタンが見つかりませんでした")

        post_button.click()
        sleep(5)

        print("投稿完了")

    except Exception as e:
        print(f"X投稿エラー: {e}")
        raise


def main():
    """メイン処理"""
    try:
        print("処理開始")

        # Chromeオプション設定
        options = setup_chrome_options()

        # 野村證券から市場データ取得
        print("市場データを取得中...")
        market_browser = webdriver.Chrome(options=options)

        try:
            nikkei, dow, kawase = get_market_data(market_browser)
            print(f"日経平均: {nikkei}")
            print(f"NYダウ: {dow}")
            print(f"ドル/円: {kawase}")
        finally:
            market_browser.quit()

        # Xに投稿
        print("Xに投稿中...")
        x_browser = webdriver.Chrome(options=options)

        try:
            # クッキーを読み込み
            cookies = load_cookies()

            # 投稿メッセージ作成
            post_message = f'【お昼の経済指標速報】\n\n日経平均：{nikkei}\nNYダウ：{dow}\nドル/円：{kawase}\n\n#株価 #為替'

            # 投稿実行
            post_to_x(x_browser, post_message, cookies)

        finally:
            x_browser.quit()

        print("処理完了")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        raise


if __name__ == "__main__":
    main()