import os
import winreg
import csv
from pathlib import Path
from datetime import datetime

def verify_osu_directory(path):
    """驗證資料夾是否為 osu! 安裝目錄"""
    if not path:
        return False
    
    # 檢查是否存在 osu!.exe
    osu_exe = Path(path) / "osu!.exe"
    return osu_exe.is_file()

def find_osu_directory():
    """尋找 osu! 的安裝位置"""
    possible_locations = []
    
    # 1. 先檢查預設安裝位置
    default_path = os.path.join(os.getenv('LOCALAPPDATA'), 'osu!')
    if os.path.exists(default_path):
        possible_locations.append(default_path)
    
    # 2. 嘗試從註冊表尋找安裝位置
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"osu\DefaultIcon")
        value, _ = winreg.QueryValueEx(key, "")
        osu_path = value.replace('"', '').replace(',0', '')
        osu_directory = os.path.dirname(osu_path)
        
        if os.path.exists(osu_directory):
            possible_locations.append(osu_directory)
    except WindowsError:
        pass
    
    # 3. 驗證找到的位置
    for location in possible_locations:
        if verify_osu_directory(location):
            return location
    
    return None

def find_songs_directory(osu_dir):
    """找到 osu! 的 Songs 資料夾位置"""
    if not osu_dir:
        return None
    
    # 1. 先檢查預設的 Songs 資料夾
    default_songs = Path(osu_dir) / "Songs"
    if default_songs.is_dir():
        return default_songs
    
    # 2. 嘗試從設定檔讀取自訂的 Songs 位置
    try:
        config_files = list(Path(osu_dir).glob("osu!.*.cfg"))
        if config_files:
            config_path = config_files[0]
            
            with open(config_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("BeatmapDirectory"):
                        songs_path = line.split("=")[1].strip()
                        songs_dir = Path(songs_path)
                        if songs_dir.is_dir():
                            return songs_dir
    except Exception as e:
        print(f"讀取設定檔時發生錯誤：{e}")
    
    return None

def get_beatmap_count(songs_dir):
    """計算 Songs 資料夾中的圖譜數量"""
    if not songs_dir:
        return 0
    return len([d for d in songs_dir.iterdir() if d.is_dir()])

def get_beatmap_ids(songs_dir):
    """取得所有圖譜的 ID"""
    if not songs_dir:
        return []
    
    beatmap_ids = []
    for folder in songs_dir.iterdir():
        if folder.is_dir():
            # 資料夾名稱通常格式為: "123456 Artist - Song Name"
            folder_name = folder.name
            # 取得空格前的數字
            try:
                beatmap_id = folder_name.split(' ')[0]
                if beatmap_id.isdigit():
                    beatmap_ids.append(beatmap_id)
            except:
                continue
    
    return beatmap_ids

def get_beatmap_url(beatmap_id):
    """產生 beatmap 的網址"""
    return f"https://osu.ppy.sh/beatmapsets/{beatmap_id}"

def get_beatmap_details(songs_dir):
    """取得所有圖譜的詳細資訊"""
    if not songs_dir:
        return []
    
    beatmap_details = []
    for folder in songs_dir.iterdir():
        if folder.is_dir():
            try:
                # 資料夾名稱通常格式為: "123456 Artist - Song Name"
                folder_name = folder.name
                beatmap_id = folder_name.split(' ')[0]
                
                if not beatmap_id.isdigit():
                    continue
                    
                # 取得資料夾資訊
                folder_stat = folder.stat()
                created_time = datetime.fromtimestamp(folder_stat.st_ctime)
                modified_time = datetime.fromtimestamp(folder_stat.st_mtime)
                
                # 計算資料夾大小
                folder_size = sum(f.stat().st_size for f in folder.rglob('*') if f.is_file())
                folder_size_mb = folder_size / (1024 * 1024)
                
                beatmap_details.append({
                    'id': beatmap_id,
                    'name': folder_name[len(beatmap_id)+1:],  # 移除ID和空格
                    'url': get_beatmap_url(beatmap_id),
                    'size_mb': round(folder_size_mb, 2),
                    'created_time': created_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'modified_time': modified_time.strftime('%Y-%m-%d %H:%M:%S')
                })
            except:
                continue
    
    return beatmap_details

def export_to_csv(beatmap_details, output_file='beatmaps.csv'):
    """將圖譜資訊輸出成CSV檔案"""
    if not beatmap_details:
        return False
        
    # 修改輸出路徑
    output_path = Path("src/data") / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    fieldnames = ['id', 'name', 'url', 'size_mb', 'created_time', 'modified_time']
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(beatmap_details)
        return True
    except Exception as e:
        print(f"輸出CSV時發生錯誤：{e}")
        return False 