import PyInstaller.__main__
from pathlib import Path

def build():
    """打包程式"""
    # 建立必要目錄
    directories = ['cache', 'downloads', 'data']
    for dir_name in directories:
        Path(f'src/{dir_name}').mkdir(parents=True, exist_ok=True)
    
    # 設定打包選項
    options = [
        'src/main.py',
        '--name=osu_map_manager',
        '--onefile',  # 打包成單一執行檔
        '--clean',    # 清理暫存檔
        '--distpath=dist',  # 輸出目錄
        '--workpath=build',  # 暫存目錄
        '--add-data=src/scripts;scripts',  # 添加腳本目錄
        '--add-data=src/cache;cache',  # 添加緩存目錄
        '--add-data=src/data;data',  # 添加資料目錄
        '--add-data=src/downloads;downloads'  # 添加下載目錄
    ]
    
    # 執行打包
    print("開始打包程式...")
    PyInstaller.__main__.run(options)
    print("打包完成！檢查 dist 目錄")

if __name__ == '__main__':
    build()
