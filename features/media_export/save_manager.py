import json
import requests

class SaveManager:
    """JSON ve PNG olarak bilgisayara kaydetme (Sistem Asistanının Alanı)"""
    def save_metadata(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def save_image(self, url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
