from pathlib import Path
from scripts.osu_finder import (
    find_osu_directory, 
    find_songs_directory, 
    get_beatmap_count,
    get_beatmap_details,
    export_to_csv
)
from scripts.osu_downloader import download_from_csv
from scripts.path_manager import PathManager

def show_menu():    
    """顯示主選單"""
    print("\n=== osu! 圖譜備份工具 ===")
    print("1. 掃描本機圖譜")
    print("2. 下載已備份圖譜")
    print("3. 退出")
    return input("\n請選擇功能 (1-3): ")


def scan_local_beatmaps():
    """掃描本機圖譜"""
    print("\n開始掃描本機圖譜...")
    
    osu_dir = find_osu_directory()
    if not osu_dir:
        print("找不到 osu! 的安裝位置 (´;ω;｀)")
        return False
    
    songs_dir = find_songs_directory(osu_dir)
    if not songs_dir:
        print("找不到 Songs 資料夾 (´;ω;｀)")
        return False
        
    print(f"找到 Songs 資料夾：{songs_dir}")
    print(f"圖譜數量：{get_beatmap_count(songs_dir)}")
    
    print("正在收集圖譜資訊...")
    beatmap_details = get_beatmap_details(songs_dir)
    
    if export_to_csv(beatmap_details):
        print("已成功輸出到 beatmaps.csv ✨")
        print(f"共處理了 {len(beatmap_details)} 個圖譜")
        return True
    else:
        print("輸出CSV時發生錯誤 (´;ω;｀)")
        return False

def download_missing_beatmaps():
    """下載遺失的圖譜"""
    beatmaps_file = PathManager.get_beatmaps_file()
    if not beatmaps_file.exists():
        print("\n請先執行掃描功能產生 beatmaps.csv (´;ω;｀)")
        return
    
    print("\n開始下載遺失圖譜...")
    download_from_csv(beatmaps_file.name, PathManager.get_downloads_path())

def main():
    # 確保所有必要的目錄都存在
    PathManager.ensure_directories()
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            scan_local_beatmaps()
        elif choice == "2":
            download_missing_beatmaps()
        elif choice == "3":
            print("\n感謝使用！ヾ(•ω•`)o")
            break
        else:
            print("\n請輸入有效的選項！(◞‸◟)")
        
        input("\n按 Enter 繼續...")

if __name__ == "__main__":
    main()
