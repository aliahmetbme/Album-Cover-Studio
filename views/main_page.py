import tkinter as tk
from tkinter import ttk

class MainPage(tk.Frame):
    """Tüm Tkinter kodları, butonlar ve yerleşim burada (Arayüz Geliştiricisinin Alanı)"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Album Cover Studio - Ana Sayfa", font=("Helvetica", 16))
        label.pack(pady=20, padx=20)
        
        self.status_label = ttk.Label(self, text="Hazır")
        self.status_label.pack(pady=10)

        # Örnek butonlar
        self.generate_btn = ttk.Button(self, text="Kapak Oluştur", command=self.on_generate)
        self.generate_btn.pack(pady=5)

    def on_generate(self):
        self.status_label.config(text="Oluşturuluyor...")
        # Burada controller üzerinden feature'lar çağrılacak
        pass
