import csv
import time
import requests
import sys
import urllib3
import certifi
from pathlib import Path
from tqdm import tqdm
from .path_manager import PathManager

# 禁用不安全請求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OsuDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # 使用 certifi 的證書
        self.session.verify = certifi.where()
    
    def download_beatmap(self, beatmap_id, output_dir, retry_count=0):
        """下載指定的圖譜，支援重試"""
        
        # 鏡像站列表
        mirrors = [
            f"https://dl.sayobot.cn/beatmaps/download/{beatmap_id}",
        ]
        
        output_path = Path(output_dir) / f"{beatmap_id}.osz"
        
        if output_path.exists():
            print(f"圖譜 {beatmap_id} 已存在，跳過下載")
            return True
        
        for mirror in mirrors:
            try:
                mirror_name = mirror.split('/')[2]
                print(f"正在從 {mirror_name} 下載圖譜 {beatmap_id}...")
                
                response = self.session.get(
                    mirror, 
                    stream=True, 
                    timeout=10
                )
                response.raise_for_status()
                
                total = int(response.headers.get('content-length', 0))
                if total == 0:  # 檢查檔案大小
                    continue
                
                with open(output_path, 'wb') as f, tqdm(
                    desc="下載進度",
                    total=total,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as pbar:
                    for data in response.iter_content(chunk_size=8192):
                        size = f.write(data)
                        pbar.update(size)
                
                # 驗證檔案大小
                if output_path.stat().st_size == total:
                    print(f"圖譜 {beatmap_id} 下載完成！")
                    return True
                else:
                    print("檔案大小不符，重試其他鏡像站...")
                    output_path.unlink(missing_ok=True)
                    continue
                
            except Exception as e:
                print(f"從 {mirror_name} 下載失敗：{e}")
                output_path.unlink(missing_ok=True)
                continue
        
        # 所有鏡像站都失敗，重試整個過程
        if retry_count < 3:
            wait_time = (retry_count + 1) * 5
            print(f"等待 {wait_time} 秒後重試...")
            time.sleep(wait_time)
            return self.download_beatmap(beatmap_id, output_dir, retry_count + 1)
        
        print(f"無法下載圖譜 {beatmap_id}，已跳過")
        return False

def download_from_csv(csv_file, output_dir, start_from=None):
    """從 CSV 檔案讀取並下載圖譜"""
    downloader = OsuDownloader()
    
    csv_path = PathManager.get_data_path() / csv_file
    output_dir = PathManager.get_downloads_path()
    progress_file = PathManager.get_progress_file()
    
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = list(csv.DictReader(f))
            total_maps = len(reader)
            
            # 如果指定了起始位置，從該位置開始下載
            if start_from:
                for i, row in enumerate(reader):
                    if row['id'] == start_from:
                        reader = reader[i:]
                        break
            
            print(f"找到 {len(reader)} 個待下載圖譜")
            
            for i, row in enumerate(reader, 1):
                beatmap_id = row['id']
                print(f"\n[{i}/{len(reader)}] ", end="")
                
                try:
                    if not downloader.download_beatmap(beatmap_id, output_dir):
                        with open("failed_downloads.txt", "a") as f:
                            f.write(f"{beatmap_id}\n")
                    
                    # 每下載3個圖譜存檔一次進度
                    if i % 3 == 0:
                        with open(progress_file, "w") as f:
                            f.write(beatmap_id)
                    
                    time.sleep(0.5)
                    
                except KeyboardInterrupt:
                    print("\n\n下載已暫停！最後下載的圖譜ID：", beatmap_id)
                    print("重新執行程式時加入參數 --continue 可從此處繼續")
                    with open(progress_file, "w") as f:
                        f.write(beatmap_id)
                    sys.exit(0)
                
    except FileNotFoundError:
        print(f"找不到 CSV 檔案：{csv_path}")
    except Exception as e:
        print(f"處理 CSV 時發生錯誤：{e}")

if __name__ == "__main__":
    csv_file = "beatmaps.csv"
    output_dir = "downloads"
    
    # 確保所有必要的目錄都存在
    PathManager.ensure_directories()
    
    # 檢查是否需要繼續上次的下載
    start_from = None
    if "--continue" in sys.argv:
        try:
            with open(PathManager.get_progress_file(), "r") as f:
                start_from = f.read().strip()
            print(f"從圖譜 {start_from} 繼續下載")
        except FileNotFoundError:
            pass
    
    download_from_csv(csv_file, output_dir, start_from) 