from pathlib import Path

class PathManager:
    @staticmethod
    def get_base_path():
        """取得基礎路徑"""
        # 檢查是否在開發環境（src 資料夾存在）
        if Path("src").is_dir():
            return Path("src")
        return Path(".")
    
    @staticmethod
    def get_data_path():
        """取得資料目錄路徑"""
        base_path = PathManager.get_base_path()
        data_path = base_path / "data"
        data_path.mkdir(parents=True, exist_ok=True)
        return data_path
    
    @staticmethod
    def get_downloads_path():
        """取得下載目錄路徑"""
        base_path = PathManager.get_base_path()
        downloads_path = base_path / "downloads"
        downloads_path.mkdir(parents=True, exist_ok=True)
        return downloads_path
    
    @staticmethod
    def get_cache_path():
        """取得緩存目錄路徑"""
        base_path = PathManager.get_base_path()
        cache_path = base_path / "cache"
        cache_path.mkdir(parents=True, exist_ok=True)
        return cache_path
    
    @staticmethod
    def get_progress_file():
        """取得下載進度檔案路徑"""
        return PathManager.get_cache_path() / "download_progress.txt"
    
    @staticmethod
    def get_beatmaps_file():
        """取得圖譜清單檔案路徑"""
        return PathManager.get_data_path() / "beatmaps.csv"
    
    @staticmethod
    def ensure_directories():
        """確保所有必要的目錄都存在"""
        PathManager.get_data_path()
        PathManager.get_downloads_path()
        PathManager.get_cache_path() 