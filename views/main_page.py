import tkinter as tk
from tkinter import ttk

class MainPage(tk.Frame):
    """
    Güncellenmiş ve Dinamik Versiyon:
    - "Duality" (Hayali x Gerçek) uyarısı eklendi.
    - "Empty State" (Boş Durum) karşılama ekranı eklendi.
    - UX/UI iyileştirmeleri (kenar boşlukları, kart görünümü) yapıldı.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Ana Pencere Ayarları (Ebeveyn üzerinden)
        if isinstance(parent, tk.Tk) or isinstance(parent, tk.Toplevel):
            parent.title("Album Cover Studio")
            parent.geometry("1200x800")
            parent.configure(bg="#121212")
        
        self.configure(bg="#121212")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.create_layout()

    def configure_styles(self):
        self.style.configure("TFrame", background="#121212")
        self.style.configure("Left.TFrame", background="#0A0A0A") # Sol paneli biraz daha koyu yapıp ayırdık
        self.style.configure("Card.TFrame", background="#181818") # Kart görünümü için
        
        self.style.configure("TLabel", background="#121212", foreground="#FFFFFF", font=("Helvetica", 12))
        self.style.configure("Left.TLabel", background="#0A0A0A", foreground="#FFFFFF", font=("Helvetica", 12))
        
        # Buton Stili (Spotify Yeşili)
        self.style.configure("Green.TButton", background="#1DB954", foreground="#000000", font=("Helvetica", 13, "bold"), padding=12)
        self.style.map("Green.TButton", background=[('active', '#1ed760')])
        
        # İkincil Buton (Listen / Save)
        self.style.configure("Outline.TButton", background="#181818", foreground="#1DB954", font=("Helvetica", 11, "bold"))

        # Combobox & Spinbox Styling (Modern Dark Border)
        self.style.configure("TCombobox", 
                             fieldbackground="#181818", 
                             background="#282828", 
                             foreground="#FFFFFF",
                             darkcolor="#282828",
                             lightcolor="#282828",
                             bordercolor="#3E3E3E",
                             insertcolor="#FFFFFF",
                             arrowcolor="#FFFFFF",
                             padding=5)
        
        self.style.configure("TSpinbox", 
                             fieldbackground="#181818", 
                             background="#282828", 
                             foreground="#FFFFFF",
                             darkcolor="#282828",
                             lightcolor="#282828",
                             bordercolor="#3E3E3E",
                             insertcolor="#FFFFFF",
                             arrowcolor="#FFFFFF",
                             padding=5)

    def create_layout(self):
        # Sol Panel
        self.left_panel = ttk.Frame(self, style="Left.TFrame", width=350)
        self.left_panel.pack(side="left", fill="y")
        self.left_panel.pack_propagate(False)
        
        # Araya ince bir sınır (border) çizgisi ekliyoruz
        separator = tk.Frame(self, bg="#282828", width=4)
        separator.pack(side="left", fill="y")
        
        # Sağ Panel (Ana İçerik)
        self.right_panel = ttk.Frame(self, style="TFrame")
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        # Sağ panelin iki farklı durumu (State) olacak
        self.empty_state_frame = ttk.Frame(self.right_panel, style="TFrame")
        self.result_state_frame = ttk.Frame(self.right_panel, style="TFrame")
        
        self.build_left_panel()
        self.build_empty_state()
        self.build_result_state()
        
        # Başlangıçta boş ekranı göster
        self.show_empty_state()

    def build_left_panel(self):
        # İç boşluklar (padding) için bir kapsayıcı
        content = tk.Frame(self.left_panel, bg="#0A0A0A", padx=25, pady=30)
        content.pack(fill="both", expand=True)

        tk.Label(content, text="Album Cover Studio", font=("Helvetica", 22, "bold"), bg="#0A0A0A", fg="#FFFFFF").pack(anchor="w", pady=(0, 5))
        tk.Label(content, text="Journal your mood, generate your sound.", font=("Helvetica", 11), bg="#0A0A0A", fg="#B3B3B3").pack(anchor="w", pady=(0, 20))
        
        ttk.Label(content, text="Your Mood / Journal Entry", style="Left.TLabel").pack(anchor="w", pady=(10, 5))
        self.mood_text = tk.Text(content, height=6, bg="#181818", fg="#FFFFFF", font=("Helvetica", 11), insertbackground="white", relief="flat", highlightthickness=2, highlightbackground="#3E3E3E", highlightcolor="#1DB954", padx=10, pady=10)
        self.mood_text.pack(fill="x", pady=(0, 15))
        self.mood_text.insert("1.0", "How was your day?")
        
        ttk.Label(content, text="Genre", style="Left.TLabel").pack(anchor="w")
        self.genre_combo = ttk.Combobox(content, values=["Electronic", "Synthwave", "Indie", "Pop", "Rock"])
        self.genre_combo.set("Electronic")
        self.genre_combo.pack(fill="x", pady=(0, 15))
        
        ttk.Label(content, text="Era", style="Left.TLabel").pack(anchor="w")
        self.era_combo = ttk.Combobox(content, values=["Modern", "2010s", "2000s", "90s", "80s"])
        self.era_combo.set("Modern")
        self.era_combo.pack(fill="x", pady=(0, 15))
        
        ttk.Label(content, text="Track Count (6-14)", style="Left.TLabel").pack(anchor="w")
        self.track_spin = ttk.Spinbox(content, from_=6, to=14)
        self.track_spin.set(10)
        self.track_spin.pack(fill="x", pady=(0, 30))
        
        # Generat butonunu controller'a veya boş bir fonksiyona bağlayacağız
        self.generate_btn = ttk.Button(content, text="GENERATE ALBUM", style="Green.TButton", command=self.on_generate_click)
        self.generate_btn.pack(fill="x", pady=(0, 10))
        
        self.status_label = tk.Label(content, text="Status: Ready", font=("Helvetica", 9, "italic"), bg="#0A0A0A", fg="#B3B3B3")
        self.status_label.pack(side="left", anchor="sw", pady=10)

    def build_empty_state(self):
        """Uygulama ilk açıldığında görünen boş karşılama ekranı"""
        self.empty_state_frame.pack_propagate(False)
        
        # Ortalamak için boşluk
        tk.Label(self.empty_state_frame, text="🎵", font=("Helvetica", 70), bg="#121212", fg="#282828").pack(pady=(200, 10))
        tk.Label(self.empty_state_frame, text="Generated tracklist will be shown here.", font=("Helvetica", 18, "bold"), bg="#121212", fg="#FFFFFF").pack()
        tk.Label(self.empty_state_frame, text="Describe your mood on the left and hit generate.", font=("Helvetica", 13), bg="#121212", fg="#B3B3B3").pack(pady=(5, 30))

        # DUALITY UYARISI (Proje dökümanındaki zorunluluk)
        duality_frame = tk.Frame(self.empty_state_frame, bg="#181818", padx=25, pady=20, highlightthickness=1, highlightbackground="#3E3E3E")
        duality_frame.pack(padx=50)
        tk.Label(duality_frame, text="⚠️ CONCEPT TRANSPARENCY", font=("Helvetica", 11, "bold"), bg="#181818", fg="#1DB954").pack(anchor="w")
        tk.Label(duality_frame, text="The album metadata (title, artist, cover) generated by AI is entirely FICTIONAL.\nHowever, the recommended tracklist contains REAL songs fetched from Last.fm.", font=("Helvetica", 11), bg="#181818", fg="#B3B3B3", justify="left").pack(anchor="w", pady=(5,0))

    def build_result_state(self):
        """Veri geldiğinde dolacak olan asıl Spotify ekranı"""
        content = tk.Frame(self.result_state_frame, bg="#121212", padx=40, pady=40)
        content.pack(fill="both", expand=True)

        # Üst Kısım: Kapak ve Metadata
        header_frame = tk.Frame(content, bg="#121212")
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Kapak görseli için label (Daha sonra ImageService ile güncellenecek)
        self.cover_label = tk.Label(header_frame, bg="#282828", width=35, height=15)
        self.cover_label.pack(side="left", padx=(0, 30))
        
        meta_frame = tk.Frame(header_frame, bg="#121212")
        meta_frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(meta_frame, text="ALBUM • FICTIONAL RELEASE", font=("Helvetica", 11, "bold"), bg="#121212", fg="#B3B3B3").pack(anchor="w")
        
        self.album_title_label = tk.Label(meta_frame, text="", font=("Helvetica", 40, "bold"), bg="#121212", fg="#FFFFFF")
        self.album_title_label.pack(anchor="w", pady=(5, 10))
        
        self.album_info_label = tk.Label(meta_frame, text="", font=("Helvetica", 13), bg="#121212", fg="#FFFFFF")
        self.album_info_label.pack(anchor="w", pady=(0, 10))
        
        self.tags_label = tk.Label(meta_frame, text="", font=("Helvetica", 11), bg="#121212", fg="#1DB954")
        self.tags_label.pack(anchor="w")
        
        # Alt Kısım: Şarkı Listesi (Kart içinde)
        self.list_card = tk.Frame(content, bg="#181818", padx=20, pady=20, highlightthickness=1, highlightbackground="#3E3E3E")
        self.list_card.pack(fill="both", expand=True)
        
        self.list_header = tk.Label(self.list_card, text="#      Title                                                          Artist", font=("Helvetica", 11, "bold"), bg="#181818", fg="#B3B3B3")
        self.list_header.pack(anchor="w", pady=(0, 10))
        
        # Şarkı satırları için container
        self.songs_container = tk.Frame(self.list_card, bg="#181818")
        self.songs_container.pack(fill="both", expand=True)
            
        self.save_btn = ttk.Button(content, text="SAVE ALBUM (JSON + PNG)", style="Green.TButton")
        self.save_btn.pack(side="bottom", fill="x", pady=(20,0))

    # --- EKRAN GEÇİŞ FONKSİYONLARI ---
    def show_empty_state(self):
        self.result_state_frame.pack_forget()
        self.empty_state_frame.pack(fill="both", expand=True)

    def show_result_state(self):
        self.empty_state_frame.pack_forget()
        self.result_state_frame.pack(fill="both", expand=True)

    def on_generate_click(self):
        """Butona basıldığında çalışacak fonksiyon (Controller tarafından ezilecek veya bağlanacak)"""
        if self.controller and hasattr(self.controller, 'handle_generate'):
            self.controller.handle_generate()
        else:
            self.status_label.config(text="Status: Generating...")
            # Entegrasyon tamamlanana kadar sadece ekranı değiştiriyoruz (veri basmadan)
            self.after(500, self.show_result_state)
            self.after(500, lambda: self.status_label.config(text="Status: Ready"))

if __name__ == "__main__":
    # Standalone çalıştırma desteği
    root = tk.Tk()
    app = MainPage(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
