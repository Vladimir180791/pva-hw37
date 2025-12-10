import requests
import zipfile
import os
import sys

def update_chromedriver():
    # Получаем последнюю версию
    latest_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    response = requests.get(latest_url)
    version = response.text.strip()
    
    print(f"Latest ChromeDriver version: {version}")
    
    # Определяем ОС
    if sys.platform.startswith('win'):
        driver_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
        driver_name = "chromedriver.exe"
    elif sys.platform.startswith('linux'):
        driver_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_linux64.zip"
        driver_name = "chromedriver"
    elif sys.platform.startswith('darwin'):
        driver_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_mac64.zip"
        driver_name = "chromedriver"
    
    # Скачиваем и распаковываем
    print(f"Downloading from: {driver_url}")
    zip_path = "chromedriver.zip"
    
    with requests.get(driver_url, stream=True) as r:
        r.raise_for_status()
        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    # Распаковываем
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall()
    
    # Даем права на выполнение (для Linux/Mac)
    if not sys.platform.startswith('win'):
        os.chmod(driver_name, 0o755)
    
    # Удаляем архив
    os.remove(zip_path)
    
    print(f"ChromeDriver {version} updated successfully!")

if __name__ == "__main__":
    update_chromedriver()