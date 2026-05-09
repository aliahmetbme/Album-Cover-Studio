import os
from dotenv import load_dotenv
import tkinter as tk

# .env dosyasındaki anahtarları yükle
load_dotenv()
from views.main_page import MainPage
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
        self.root.geometry("800x600")
        
        # Ana sayfayı yükle
        self.main_page = MainPage(self.root, self)
        self.main_page.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlbumCoverStudioApp(root)
    root.mainloop()
