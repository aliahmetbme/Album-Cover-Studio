import os
from dotenv import load_dotenv
import tkinter as tk

# .env dosyasındaki anahtarları yükle
load_dotenv()
from views.main_page import MainPage
from viewmodels.album_view_model import AlbumViewModel
# Feature importları örnek olarak eklendi
# from features.generator.gemini_service import GeminiService
# from features.music_discovery.lastfm_service import LastFMService
# from features.media_export.image_service import ImageService
# from features.media_export.save_manager import SaveManager

class AlbumCoverStudioApp:
    """Proje Yöneticisi (Senin) alanın: View ve Feature'ları birleştirme"""
    def __init__(self, root):
        self.root = root
        self.root.title("Album Cover Studio")
        self.root.geometry("1200x800")
        
        # ViewModel'ı başlat
        self.view_model = AlbumViewModel()
        
        # Ana sayfayı yükle ve ViewModel'ı enjekte et
        self.main_page = MainPage(self.root, self.view_model)
        self.main_page.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlbumCoverStudioApp(root)
    root.mainloop()
