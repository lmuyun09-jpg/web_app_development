# 路由與頁面設計文件 (ROUTES)

本文件依據 PRD、ARCHITECTURE 與 DB_DESIGN 設計本專案的 URL 路由規劃與 Jinja2 模板對應關係。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 | GET | `/` | `index.html` | 網站介紹與系統入口 |
| 註冊頁面 | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| 提交註冊 | POST | `/auth/register` | — | 接收表單並建立 User，完成後重導向登入頁 |
| 登入頁面 | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| 提交登入 | POST | `/auth/login` | — | 驗證密碼，寫入 Session 並重導向首頁 |
| 登出 | GET | `/auth/logout` | — | 清除 Session 並重導向首頁 |
| 進入抽籤頁 | GET | `/fortune/` | `fortune/index.html` | 顯示抽籤與擲筊互動介面 |
| 執行抽籤 | POST | `/fortune/draw` | — | 隨機抽取籤詩，若是會員則寫入紀錄，重導向結果頁 |
| 顯示籤詩結果 | GET | `/fortune/<int:id>` | `fortune/result.html` | 顯示指定歷史紀錄/籤詩的結果與詳解 |
| 個人歷史紀錄 | GET | `/profile/` | `profile/index.html` | 顯示使用者過去所有的抽籤與捐款紀錄 |
| 捐獻頁面 | GET | `/donate/` | `donate/index.html` | 顯示香油錢捐獻說明與選擇金額表單 |
| 提交捐款 | POST | `/donate/pay` | — | 建立捐款紀錄並模擬付款，重導向感謝頁 |
| 捐款感謝頁 | GET | `/donate/<int:id>/success` | `donate/success.html`| 顯示付款成功與感謝訊息 |

---

## 2. 每個路由的詳細說明

### 首頁 (`main.py`)
- **GET `/`**
  - **處理邏輯**: 簡單的回傳首頁模板，如果已經登入，可以取得 session 中的 user_id 在前端顯示個人化歡迎詞。
  - **輸出**: 渲染 `index.html`。

### 認證授權 (`auth.py`)
- **GET `/auth/register`**
  - **輸出**: 渲染 `auth/register.html` 供使用者填寫資料。
- **POST `/auth/register`**
  - **輸入**: Form data (`username`, `email`, `password`)。
  - **處理邏輯**: 驗證必填並透過 User Model 寫入。若 email 重複需回傳錯誤訊息 (flash)。
  - **輸出**: 成功後重導向 `/auth/login`。
- **GET `/auth/login`**
  - **輸出**: 渲染 `auth/login.html`。
- **POST `/auth/login`**
  - **輸入**: Form data (`email`, `password`)。
  - **處理邏輯**: 驗證密碼，若成功則設定 `session['user_id']`。
  - **輸出**: 成功後重導向 `/`，失敗則重新渲染並跳出錯誤。
- **GET `/auth/logout`**
  - **處理邏輯**: 將 `session` 內的 user 資訊清除。
  - **輸出**: 重導向 `/`。

### 籤詩與占卜 (`fortune.py`)
- **GET `/fortune/`**
  - **處理邏輯**: 如果有預設的參數或防重複抽狀態可以放這，主要是回傳開始求籤畫面。
  - **輸出**: 渲染 `fortune/index.html`。
- **POST `/fortune/draw`**
  - **處理邏輯**: 呼叫 `Fortune.get_random()`。若使用者為登入狀態，則產生該使用者的 `History.create()` 紀錄。若為訪客，則不寫紀錄。
  - **輸出**: 重導向至 `/fortune/<id>` (若是實獲取抽籤紀錄 id，或是籤詩本身的 id以利顯示)。
- **GET `/fortune/<int:id>`**
  - **處理邏輯**: 根據得到的 history id (獲fortune id) 使用 Model 取得籤詩詳細資料。若找不到回應 404。
  - **輸出**: 渲染 `fortune/result.html`。

### 個人檔案 (`profile.py`)
- **GET `/profile/`**
  - **處理邏輯**: 檢查使用者 Session 是否存在，若無則重導向 login。若有，則使用 API 向 History/Donation Model 撈取該使用者的資料。
  - **輸出**: 渲染 `profile/index.html` 並傳遞 `histories` 與 `donations` 參數。

### 捐款機制 (`donate.py`)
- **GET `/donate/`**
  - **輸出**: 渲染 `donate/index.html` 顯示金額選單。
- **POST `/donate/pay`**
  - **輸入**: Form data (`amount`)。
  - **處理邏輯**: 驗證金額。若是已登入會員則設定 `user_id`，若是訪客則可將其設為 NULL (或強制導向登入)。使用 `Donation.create()` 產生狀態為 SUCCESS 的單。
  - **輸出**: 重導向至 `/donate/<id>/success`。
- **GET `/donate/<int:id>/success`**
  - **處理邏輯**: 找出對應 id 的捐款紀錄。
  - **輸出**: 渲染 `donate/success.html` 顯示成功訊息。

---

## 3. Jinja2 模板清單

所有模板皆應該放置於 `app/templates/` 且繼承自共用的 `base.html`，以保持視覺風格一致：

- `base.html` （全站共用 Layout：主要包含 `<header>`、`<nav>`、`<footer>` 與基礎 CSS / JS 引入）
- `index.html` （首頁內容）
- **auth/**
  - `auth/login.html` （登入頁面）
  - `auth/register.html` （註冊頁面）
- **fortune/**
  - `fortune/index.html` （抽籤與擲筊互動頁面）
  - `fortune/result.html` （抽中籤詩之結果與解籤）
- **profile/**
  - `profile/index.html` （個人歷史紀錄列表區塊）
- **donate/**
  - `donate/index.html` （捐香油錢表單頁面）
  - `donate/success.html` （捐獻完成後之感謝畫面）

---

## 4. 路由骨架程式碼
各模組路由皆已建立於 `app/routes/` 內並以 Blueprint 的方式劃分，包含：
- `main.py`
- `auth.py`
- `fortune.py`
- `profile.py`
- `donate.py`
以及總路由註冊的 `__init__.py`。
