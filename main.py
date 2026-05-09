import os
from dotenv import load_dotenv
import tkinter as tk

# .env dosyasındaki anahtarları yükle
load_dotenv()
from views.main_page import MainPage
from viewmodels.album_view_model import AlbumViewModel


class AlbumCoverStudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Album Cover Studio")
        self.root.geometry("1200x800")
         
        # Initialize ViewModel
        self.view_model = AlbumViewModel()
        
        # Load main page and inject ViewModel
        self.main_page = MainPage(self.root, self.view_model)
        self.main_page.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlbumCoverStudioApp(root)
    root.mainloop()
