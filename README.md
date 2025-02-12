# OSU Map Manager

一個簡單易用的 OSU! 譜面管理工具，幫助你掃描、備份和下載譜面。

## 功能特色 ✨

- 自動掃描本機已安裝的 OSU! 譜面

- 匯出譜面資訊到 CSV 檔案
- 支援批量下載譜面
- 自動記錄下載進度，支援斷點續傳
- 可打包成獨立執行檔 (.exe)

## 下載與安裝 📥

### 方法一：直接使用（推薦）

1. [下載最新版本](https://github.com/Ynoob87/osu_map_manager/releases)
2. 解壓縮到任意資料夾
3. 執行 `osu_map_manager.exe`

### 方法二：從原始碼安裝

1. 克隆此專案：

   ```bash
   git clone https://github.com/Ynoob87/osu_map_manager.git
   cd osu_map_manager
   ```

2. 安裝相依套件：

   ```bash
   pip install -r requirements.txt
   ```

3. 執行程式：
   ```bash
   python src/main.py
   ```

## 系統需求 🔧

- Windows 10 或更新版本（使用打包版本）
- 或 Python 3.6+ （使用原始碼版本）
- 網路連線
- OSU! 遊戲本體

## 使用方法 🎮

### 掃描本機譜面

1. 執行程式後，會自動：
   - 尋找 OSU! 安裝位置
   - 掃描 Songs 資料夾
   - 匯出譜面資訊到 data/beatmaps.csv

### 下載譜面

- 在主視窗中選擇要下載的譜面
- 程式會自動記錄下載進度，支援中斷後續傳
- 下載的譜面會儲存在 downloads 目錄

### 打包成執行檔

1. 確保已安裝 PyInstaller：

   ```bash
   pip install pyinstaller
   ```

2. 執行打包程式：

   ```bash
   python src/build.py
   ```

3. 打包完成後：
   - 執行檔位於 `dist/osu_map_downloader.exe`
   - 包含所有必要的資料目錄和檔案
   - 可以直接複製到其他電腦使用

## 目錄結構 📁

```
src/
├── main.py           # 主程式
├── build.py          # 打包工具
├── scripts/          # 功能模組
│   ├── osu_finder.py     # 譜面掃描
│   └── osu_downloader.py # 譜面下載
├── data/             # 資料目錄
│   └── beatmaps.csv      # 譜面資訊
├── downloads/        # 下載目錄
└── cache/            # 緩存目錄
    └── download_progress.txt  # 下載進度
```

## 注意事項 ⚠️

- 請確保有足夠的硬碟空間
- 下載譜面時請遵守 OSU! 的使用條款
- 建議定期備份 beatmaps.csv
- 如果使用打包版本，可能會被防毒軟體誤判，這是正常現象

## 貢獻指南 🤝

歡迎提交 Pull Request 或開 Issue 來改善這個專案！

## 授權條款 📜

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 作者 💻

Small R
