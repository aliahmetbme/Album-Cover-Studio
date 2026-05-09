import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk

class MainPage(tk.Frame):
    """
    Updated and Dynamic Version:
    - "Duality" (Fictional x Real) warning added.
    - "Empty State" welcome screen implemented.
    - UX/UI improvements (margins, card view) applied.
    """
    def __init__(self, parent, view_model):
        super().__init__(parent)
        self.view_model = view_model
        
        # Main Window Settings (via parent)
        if isinstance(parent, tk.Tk) or isinstance(parent, tk.Toplevel):
            parent.title("Album Cover Studio")
            parent.geometry("1200x800")
            parent.configure(bg="#121212")
        
        self.configure(bg="#121212")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.create_layout()
        
        # REQ 9: Thread-safe callback binding
        if self.view_model:
            self.view_model.on_status_update = lambda s: self.after(0, self.update_status, s)
            self.view_model.on_generation_success = lambda d: self.after(0, self.handle_success, d)
            self.view_model.on_error = lambda e: self.after(0, self.handle_error, e)

    def configure_styles(self):
        self.style.configure("TFrame", background="#121212")
        self.style.configure("Left.TFrame", background="#0A0A0A") # Darker side panel
        self.style.configure("Card.TFrame", background="#181818") # For card-style containers
        
        self.style.configure("TLabel", background="#121212", foreground="#FFFFFF", font=("Helvetica", 12))
        self.style.configure("Left.TLabel", background="#0A0A0A", foreground="#FFFFFF", font=("Helvetica", 12))
        
        # Button Style (Spotify Green)
        self.style.configure("Green.TButton", background="#1DB954", foreground="#000000", font=("Helvetica", 13, "bold"), padding=12)
        self.style.map("Green.TButton", background=[('active', '#1ed760')])
        
        # Secondary Button (Listen / Save)
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
        # Left Panel
        self.left_panel = ttk.Frame(self, style="Left.TFrame", width=350)
        self.left_panel.pack(side="left", fill="y")
        self.left_panel.pack_propagate(False)
        
        # Vertical separator line
        separator = tk.Frame(self, bg="#282828", width=4)
        separator.pack(side="left", fill="y")
        
        # Right Panel (Main Content)
        self.right_panel = ttk.Frame(self, style="TFrame")
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        # Right panel will have two states (Empty/Result)
        self.empty_state_frame = ttk.Frame(self.right_panel, style="TFrame")
        self.result_state_frame = ttk.Frame(self.right_panel, style="TFrame")
        
        self.build_left_panel()
        self.build_empty_state()
        self.build_result_state()
        
        # Show empty state by default
        self.show_empty_state()

    def build_left_panel(self):
        # Container for padding
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
        
        self.generate_btn = ttk.Button(content, text="GENERATE ALBUM", style="Green.TButton", command=self.on_generate_click)
        self.generate_btn.pack(fill="x", pady=(0, 10))
        
        self.status_label = tk.Label(content, text="Status: Ready", font=("Helvetica", 11, "italic"), bg="#0A0A0A", fg="#B3B3B3")
        self.status_label.pack(side="left", anchor="sw", pady=10)

        # AI Disclaimer Note at the bottom of left panel
        tk.Label(content, text="⚠️ Note: Generated data is fictional; tracks are real. AI limitations apply.", 
                 font=("Helvetica", 10), bg="#0A0A0A", fg="#666666", wraplength=280, justify="left").pack(side="bottom", anchor="w", pady=(20, 0))

    def build_empty_state(self):
        """Welcome screen shown when the app first opens"""
        self.empty_state_frame.pack_propagate(False)
        
        # Center content
        tk.Label(self.empty_state_frame, text="🎵", font=("Helvetica", 70), bg="#121212", fg="#282828").pack(pady=(200, 10))
        tk.Label(self.empty_state_frame, text="Generated tracklist will be shown here.", font=("Helvetica", 20, "bold"), bg="#121212", fg="#FFFFFF").pack()
        tk.Label(self.empty_state_frame, text="Describe your mood on the left and hit generate.", font=("Helvetica", 14), bg="#121212", fg="#B3B3B3").pack(pady=(5, 30))

        # DUALITY WARNING (Requirement for Concept Transparency)
        duality_frame = tk.Frame(self.empty_state_frame, bg="#181818", padx=25, pady=20, highlightthickness=1, highlightbackground="#3E3E3E")
        duality_frame.pack(padx=50, fill="x", pady=20)
        
        tk.Label(duality_frame, text="⚠️ PROJECT CONCEPT & TRANSPARENCY", font=("Helvetica", 11, "bold"), bg="#181818", fg="#1DB954").pack(anchor="w")
        
        notes = [
            ("Fictional Components:", "Album name, artist, year, and cover art generated by AI are entirely FICTIONAL. These do not exist in reality."),
            ("Real Components:", "The tracklist consists of REAL songs fetched from the Last.fm API based on your mood."),
            ("Interface Transparency:", "The project is built on this 'duality' (fictional concept + real music). The UI reflects this synergy."),
            ("AI Limitations:", "Generated covers may look abstract/unusual, and song matches might not be perfect. This is inherent to AI automation.")
        ]
        
        for title, text in notes:
            tk.Label(duality_frame, text=title, font=("Helvetica", 11, "bold"), bg="#181818", fg="#FFFFFF").pack(anchor="w", pady=(8, 0))
            tk.Label(duality_frame, text=text, font=("Helvetica", 11), bg="#181818", fg="#B3B3B3", justify="left", wraplength=600).pack(anchor="w")

    def build_result_state(self):
        """The main result screen populated once data is fetched"""
        content = tk.Frame(self.result_state_frame, bg="#121212", padx=40, pady=40)
        content.pack(fill="both", expand=True)

        # Top Section: Cover and Metadata
        header_frame = tk.Frame(content, bg="#121212")
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Cover image label
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
        
        # Bottom Section: Tracklist (Inside a card)
        self.list_card = tk.Frame(content, bg="#181818", padx=20, pady=20, highlightthickness=1, highlightbackground="#3E3E3E")
        self.list_card.pack(fill="both", expand=True)
        
        self.list_header = tk.Label(self.list_card, text="#      Title                                                          Artist", font=("Helvetica", 11, "bold"), bg="#181818", fg="#B3B3B3")
        self.list_header.pack(anchor="w", pady=(0, 10))
        
        # Container for song rows
        self.songs_container = tk.Frame(self.list_card, bg="#181818")
        self.songs_container.pack(fill="both", expand=True)
            
        self.save_btn = ttk.Button(content, text="SAVE ALBUM (JSON + PNG)", style="Green.TButton")
        self.save_btn.pack(side="bottom", fill="x", pady=(20,0))

    # --- SCREEN TRANSITION FUNCTIONS ---
    def show_empty_state(self):
        self.result_state_frame.pack_forget()
        self.empty_state_frame.pack(fill="both", expand=True)

    def show_result_state(self):
        self.empty_state_frame.pack_forget()
        self.result_state_frame.pack(fill="both", expand=True)

    def on_generate_click(self):
        """Reads UI inputs and triggers the ViewModel generation task."""
        journal = self.mood_text.get("1.0", "end-1c")
        genre = self.genre_combo.get()
        era = self.era_combo.get()
        track_count = int(self.track_spin.get())
        
        if self.view_model:
            self.view_model.generate_album(journal, genre, era, track_count)
        else:
            self.status_label.config(text="Status: No ViewModel connected")

    def update_status(self, message):
        """Thread-safe status label update."""
        self.status_label.config(text=f"Status: {message}")

    def handle_success(self, data):
        """Handles successful generation by updating UI components."""
        self.populate_results(data)
        self.show_result_state()
        self.status_label.config(text="Status: Ready")

    def handle_error(self, error_message):
        """Handles generation errors with a popup."""
        self.status_label.config(text="Status: Error")
        messagebox.showerror("Generation Error", error_message)

    def populate_results(self, data):
        """Populates the result state UI with real data from the ViewModel."""
        # Update Metadata Labels
        self.album_title_label.config(text=data.get("album_name", "Unknown Album"))
        info_text = f"{data.get('artist_name', 'Unknown Artist')} • {data.get('year', '2026')} • {len(data.get('tracks', []))} tracks"
        self.album_info_label.config(text=info_text)
        self.tags_label.config(text=" • ".join(data.get("lastfm_tags", [])))

        # Update Cover Image
        img = data.get("cover_image")
        if img:
            photo = ImageTk.PhotoImage(img)
            self.cover_label.config(image=photo, width=300, height=300) # Adjusted size for UI
            self.cover_label.image = photo  # Keep reference

        # Clear and Populate Tracklist
        for widget in self.songs_container.winfo_children():
            widget.destroy()

        for i, track in enumerate(data.get("tracks", []), 1):
            row = tk.Frame(self.songs_container, bg="#181818")
            row.pack(fill="x", pady=2)
            
            tk.Label(row, text=str(i), width=4, anchor="w", bg="#181818", fg="#B3B3B3", font=("Helvetica", 12)).pack(side="left")
            tk.Label(row, text=track['title'], width=40, anchor="w", bg="#181818", fg="#FFFFFF", font=("Helvetica", 14, "bold")).pack(side="left")
            tk.Label(row, text=track['artist'], anchor="w", bg="#181818", fg="#B3B3B3", font=("Helvetica", 12)).pack(side="left")

if __name__ == "__main__":
    # Support for standalone execution
    root = tk.Tk()
    app = MainPage(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
