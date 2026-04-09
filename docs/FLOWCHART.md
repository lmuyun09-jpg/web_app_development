# 系統流程圖文件 (FLOWCHART)

這份文件基於 PRD 與系統架構設計，描繪出使用者的操作路徑（User Flow），以及系統內部的資料流動順序（Sequence Diagram），並列出了全站預計的路由對照表。

---

## 1. 使用者流程圖 (User Flow)

此流程圖展示了使用者進入網站後，主要的幾條操作動線，包含註冊登入、抽籤解籤、查看歷史與捐獻香油錢。

```mermaid
flowchart LR
    Start([使用者到達平台首頁]) --> AuthCheck{已登入？}
    
    AuthCheck -->|否| ViewGuest[訪客瀏覽首頁]
    AuthCheck -->|是| ViewMember[會員瀏覽首頁]
    
    ViewGuest --> ClickLogin[點擊登入/註冊]
    ClickLogin --> Login[登入頁面]
    Login --> SubmitLogin{驗證帳密}
    SubmitLogin -->|失敗| Login
    SubmitLogin -->|成功| ViewMember
    
    ViewMember --> ActionType{選擇操作}
    ViewGuest --> ActionType
    
    ActionType -->|1. 求指引| GoFortune[進入抽籤頁面]
    GoFortune --> DoDraw[點擊抽籤 / 擲筊]
    DoDraw --> DrawResult[顯示籤詩與解說]
    DrawResult --> ShareOptions[社群分享籤詩]
    
    ActionType -->|2. 感謝神明| GoDonate[進入捐香油錢頁面]
    GoDonate --> SelectAmount[選擇捐獻金額]
    SelectAmount --> PayFlow[模擬付款流程]
    PayFlow --> PaySuccess[感謝捐款畫面]
    
    ActionType -->|3. 回顧運勢| CheckAuthRecord{是否登入？}
    CheckAuthRecord -->|否| ClickLogin
    CheckAuthRecord -->|是| GoProfile[進入個人歷史頁面]
    GoProfile --> ViewRecord[檢視過去抽籤/捐獻紀錄]
```

---

## 2. 系統序列圖 (Sequence Diagram)

此圖描述最核心的功能：**單次抽籤並紀錄結果** 的系統底層運作流程。涵蓋前端瀏覽器、Flask Controller、Model 到資料庫的操作。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (Frontend)
    participant Flask as Flask Route (Controller)
    participant Model as Fortune/History Model
    participant DB as SQLite (Database)
    
    User->>Browser: 點擊「開始抽籤」按鈕
    Browser->>Flask: POST /fortune/draw
    
    Flask->>Model: 請求取得隨機籤詩
    Model->>DB: SELECT * FROM fortunes ORDER BY RANDOM() LIMIT 1
    DB-->>Model: 回傳籤詩資料 (編號, 吉凶, 詳解)
    
    alt 使用者有登入 (紀錄歷史)
        Model->>Model: 擷取 user_id
        Model->>DB: INSERT INTO history (user_id, fortune_id, create_time)
        DB-->>Model: 儲存成功
    end
    
    Model-->>Flask: 回傳籤詩物件
    Flask->>Browser: 回傳 Jinja2 渲染畫面 (fortune/result.html)
    Browser-->>User: 顯示籤詩結果與詳解文字
```

---

## 3. 功能清單對照表

此表列出目前預計需要開發的 URL 路由、對應的 HTTP 請求方法，以及其負責的功能對應到 MVC 內的結構。

| 功能描述 | URL 路徑 | HTTP 方法 | 對應 Route 模組 | 對應 Template |
| :--- | :--- | :--- | :--- | :--- |
| **首頁** (網站介紹、入口) | `/` | GET | `main.py` | `index.html` |
| **註冊頁面/提交註冊** | `/auth/register` | GET, POST | `auth.py` | `auth/register.html` |
| **登入頁面/提交登入** | `/auth/login` | GET, POST | `auth.py` | `auth/login.html` |
| **登出** | `/auth/logout` | GET | `auth.py` | (無，重定向) |
| **進入抽籤頁面** | `/fortune/` | GET | `fortune.py` | `fortune/index.html` |
| **執行抽籤與結果顯示** | `/fortune/draw` | GET, POST | `fortune.py` | `fortune/result.html` |
| **個人歷史紀錄列表** | `/profile/` | GET | `main.py` 或 `history.py` | `profile/index.html` |
| **進入捐香油錢頁面** | `/donate/` | GET | `donate.py` | `donate/index.html` |
| **提交捐款表單** | `/donate/pay` | POST | `donate.py` | `donate/success.html` |
