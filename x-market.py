# x-market.py

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle


market_url = 'https://www.nomura.co.jp/market/conditions/'
X_url = 'https://x.com'

options = Options()
options.add_argument("--headless")

# 野村證券からマーケット情報を取得
browser = webdriver.Chrome(options=options)
browser.get(market_url)
browser.implicitly_wait(10)

nikkei = browser.find_element(By.ID, 'ni225').text.replace('\n', '  ').replace('（', '(').replace('）', ')')
dow = browser.find_element(By.ID, 'dji').text.replace('\n', '  ').replace('（', '(').replace('）', ')')
kawase = browser.find_element(By.ID, 'usd').text.replace('\n', '  ').replace('（', '(').replace('）', ')')
browser.quit()

# Xにログイン
browser = webdriver.Chrome(options=options)
cookies = pickle.load(open("cookies.pkl", "rb"))
browser.get(X_url)
browser.implicitly_wait(10)
for cookie in cookies:
    browser.add_cookie(cookie)
browser.get(X_url)

# ポストの作成
post = f'【お昼の経済指標速報】\n\n日経平均：{nikkei}\nNYダウ：{dow}\nドル/円：{kawase}'

# ポストの入力
browser.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-block.public-DraftStyleDefault-ltr').send_keys(post)
sleep(10)

# ポストの投稿
browser.find_element(By.CSS_SELECTOR, 'button.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-1cwvpvk.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l').click()
sleep(5)

browser.quit()
