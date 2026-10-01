# 程式繳交系統

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

## Features

* **支援語言**：支援任意副檔名程式碼(須修改程式碼中的filetypes)。
* **支援後端**：利用 Flask 套件架設內網的 API 繳交檔案至主機伺服器的資料夾中。

---

## Tech Stack

* **核心語言 (Languages)**：Python 3.x（系統核心與調度邏輯）、C++（測試標的與底層比對）
* **開發工具 (Dev Tools)**：VS Code, Git

---

## 細節架設步驟

> [!NOTE]
> 這個使用 Python Flask 讓電腦可以直接當作伺服器端處理 requests。

> [!NOTE]
> 請注意伺服器端以及用戶端預設架設在區域網。

### 伺服器端架設
1. 下載好後在 `\server` 中找到 `server.py` 檔案
2. 使用終端機，輸入 `python3 server.py` 或者使用打包後的伺服器檔案。
3. 如果顯示以下內容，代表伺服器設置成功：

   ![success](https://raw.githubusercontent.com/Haiaka-fr/submit-system/refs/heads/main/server%20success.png)
   
5. 找到 `* Running on http://… ` 的地方，複製IP的數字部分，如192.168.0.163。(不要選127.0.0.1那個)

### 用戶端設置
1. 打開繳交程式，一開始會詢問資料庫 IP，請告訴使用者輸入前面複製的 IP 數字部分(如圖)

   ![dbip](https://raw.githubusercontent.com/Haiaka-fr/submit-system/refs/heads/main/db_ip.png)
   
3. 可以試著繳交測試，成功繳交後，請到伺服器主機確認 `server\files` 資料夾中有沒有出現繳交的檔案。
