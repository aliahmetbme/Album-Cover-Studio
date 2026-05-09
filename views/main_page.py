import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk

class RoundedContainer(tk.Canvas):
    """A rounded container used to give border-radius to widgets like Entry or Text."""
    def __init__(self, parent, width, height, radius=15, bg="#181818", outline="#282828"):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0, bd=0)
        self.radius = radius
        self.bg_color = bg
        self.outline_color = outline
        self.draw()

    def draw(self):
        self.delete("all")
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        r = self.radius
        
        # 1. Fill with solid overlap
        self.create_arc((0, 0, r*2, r*2), start=90, extent=90, fill=self.bg_color, outline=self.bg_color, style="pieslice")
        self.create_arc((w-r*2, 0, w, r*2), start=0, extent=90, fill=self.bg_color, outline=self.bg_color, style="pieslice")
        self.create_arc((0, h-r*2, r*2, h), start=180, extent=90, fill=self.bg_color, outline=self.bg_color, style="pieslice")
        self.create_arc((w-r*2, h-r*2, w, h), start=270, extent=90, fill=self.bg_color, outline=self.bg_color, style="pieslice")
        self.create_rectangle((r, 0, w-r, h), fill=self.bg_color, outline=self.bg_color)
        self.create_rectangle((0, r, w, h-r), fill=self.bg_color, outline=self.bg_color)
        
        # 2. Precise Border (width=1)
        self.create_arc((0, 0, r*2, r*2), start=90, extent=90, outline=self.outline_color, style="arc", width=1)
        self.create_arc((w-r*2, 0, w, r*2), start=0, extent=90, outline=self.outline_color, style="arc", width=1)
        self.create_arc((0, h-r*2, r*2, h), start=180, extent=90, outline=self.outline_color, style="arc", width=1)
        self.create_arc((w-r*2, h-r*2, w, h), start=270, extent=90, outline=self.outline_color, style="arc", width=1)
        self.create_line((r, 0, w-r, 0), fill=self.outline_color, width=1)
        self.create_line((r, h-1, w-r, h-1), fill=self.outline_color, width=1)
        self.create_line((0, r, 0, h-r), fill=self.outline_color, width=1)
        self.create_line((w-1, r, w-1, h-r), fill=self.outline_color, width=1)

class RoundedButton(tk.Canvas):
    """Custom button with rounded corners and hover effects using Canvas."""
    def __init__(self, parent, text, command=None, width=120, height=40, radius=20, 
                 bg_color="#1DB954", fg_color="#000000", font=("Helvetica", 12, "bold"),
                 outline_mode=False):
        # bd=0 and highlightthickness=0 to remove extra borders
        super().__init__(parent, width=width, height=height, bg=parent["bg"], 
                         highlightthickness=0, bd=0, cursor="hand2")
        self.text = text
        self.command = command
        self.radius = radius
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.font = font
        self.outline_mode = outline_mode
        self.main_bg = parent["bg"]
        
        self.draw()
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def draw(self, hover=False):
        self.delete("all")
        # Offset and subtract small amount to prevent clipping at edges
        w, h = self.winfo_reqwidth() - 2, self.winfo_reqheight() - 2
        r = self.radius
        offset = 1
        
        if self.outline_mode:
            fill = self.bg_color if hover else self.main_bg
            outline = self.bg_color
            text_color = "#FFFFFF" if hover else self.bg_color
        else:
            fill = "#1ed760" if hover else self.bg_color
            outline = fill
            text_color = self.fg_color

        # 1. Draw fill shapes WITHOUT internal outlines (1px overlap to prevent "scratches")
        self.create_arc((offset, offset, offset+r*2, offset+r*2), start=90, extent=90, fill=fill, outline="", style="pieslice")
        self.create_arc((w-r*2+offset, offset, w+offset, offset+r*2), start=0, extent=90, fill=fill, outline="", style="pieslice")
        self.create_arc((offset, h-r*2+offset, offset+r*2, h+offset), start=180, extent=90, fill=fill, outline="", style="pieslice")
        self.create_arc((w-r*2+offset, h-r*2+offset, w+offset, h+offset), start=270, extent=90, fill=fill, outline="", style="pieslice")
        # Slightly overlap rectangles to ensure no gaps (cracks) appear
        self.create_rectangle((r+offset-1, offset, w-r+offset+1, h+offset), fill=fill, outline="")
        self.create_rectangle((offset, r+offset-1, w+offset, h-r+offset+1), fill=fill, outline="")

        # 2. Draw ONLY the outer boundary lines and arcs
        self.create_line((offset+r, offset, w-r+offset, offset), fill=outline)
        self.create_line((offset+r, h+offset, w-r+offset, h+offset), fill=outline)
        self.create_line((offset, offset+r, offset, h-r+offset), fill=outline)
        self.create_line((w+offset, offset+r, w+offset, h-r+offset), fill=outline)
        self.create_arc((offset, offset, offset+r*2, offset+r*2), start=90, extent=90, outline=outline, style="arc")
        self.create_arc((w-r*2+offset, offset, w+offset, offset+r*2), start=0, extent=90, outline=outline, style="arc")
        self.create_arc((offset, h-r*2+offset, offset+r*2, h+offset), start=180, extent=90, outline=outline, style="arc")
        self.create_arc((w-r*2+offset, h-r*2+offset, w+offset, h+offset), start=270, extent=90, outline=outline, style="arc")
        
        # Text centered with respect to the actual canvas center
        self.create_text((w+2)/2, (h+2)/2, text=self.text, fill=text_color, font=self.font)

    def on_enter(self, e): self.draw(hover=True)
    def on_leave(self, e): self.draw(hover=False)
    def on_click(self, e): 
        if self.command: self.command()

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
        self.style.configure("Left.TFrame", background="#0A0A0A")
        self.style.configure("Card.TFrame", background="#181818")
        
        self.style.configure("TLabel", background="#121212", foreground="#FFFFFF", font=("Helvetica", 10))
        # SOL PANEL ETİKETLERİ BÜYÜTÜLDÜ (10 -> 12)
        self.style.configure("Left.TLabel", background="#0A0A0A", foreground="#FFFFFF", font=("Helvetica", 12))
        
        # ANA BUTON BÜYÜTÜLDÜ (11 -> 14 ve padding artırıldı)
        self.style.configure("Green.TButton", background="#1DB954", foreground="#000000", font=("Helvetica", 14, "bold"), padding=14)
        self.style.map("Green.TButton", background=[('active', '#1ed760')])
        
        self.style.configure("Outline.TButton", background="#181818", foreground="#1DB954", font=("Helvetica", 9, "bold"))
        
        # --- DEFINITIVE FIX FOR COMBOBOX ---
        self.style.configure("TCombobox", 
                             fieldbackground="#181818", 
                             background="#181818", 
                             foreground="#FFFFFF", 
                             bordercolor="#181818", 
                             lightcolor="#181818",
                             darkcolor="#181818", 
                             arrowcolor="#FFFFFF",
                             borderwidth=0,
                             padding=10)
                             
        self.style.map("TCombobox", 
                       fieldbackground=[('readonly', '#181818'), ('focus', '#181818')],
                       selectbackground=[('readonly', '#1DB954'), ('focus', '#1DB954')],
                       lightcolor=[('focus', '#181818')],
                       darkcolor=[('focus', '#181818')],
                       bordercolor=[('focus', '#181818')])
                       
        self.option_add('*TCombobox*Listbox.background', '#181818')
        self.option_add('*TCombobox*Listbox.foreground', '#FFFFFF')
        self.option_add('*TCombobox*Listbox.selectBackground', '#1DB954')
        self.option_add('*TCombobox*Listbox.selectForeground', '#000000')
        self.option_add('*TCombobox*Listbox.font', 'Helvetica 13') # AÇILIR MENÜ YAZILARI BÜYÜTÜLDÜ

        # --- DEFINITIVE FIX FOR SPINBOX ---
        self.style.configure("TSpinbox", 
                             fieldbackground="#181818", 
                             background="#181818", 
                             foreground="#FFFFFF", 
                             bordercolor="#181818", 
                             lightcolor="#181818", 
                             darkcolor="#181818", 
                             arrowcolor="#FFFFFF",
                             borderwidth=0,
                             insertwidth=0,
                             padding=10)
                             
        self.style.map("TSpinbox", 
                       fieldbackground=[('readonly', '#181818'), ('focus', '#181818')],
                       selectbackground=[('readonly', '#1DB954'), ('focus', '#1DB954')],
                       lightcolor=[('focus', '#181818')],
                       darkcolor=[('focus', '#181818')],
                       bordercolor=[('focus', '#181818')])

    def create_layout(self):
        # Left Panel (Expanded to 400px with balancing left padding)
        self.left_panel = ttk.Frame(self, style="Left.TFrame", width=400)
        self.left_panel.pack(side="left", fill="y", padx=(4, 0))
        self.left_panel.pack_propagate(False)
        
        # Vertical separator line
        separator = tk.Frame(self, bg="#282828", width=4)
        separator.pack(side="left", fill="y")
        
        # Right Panel (Main Content with Invisible Scroll)
        self.right_panel = ttk.Frame(self, style="TFrame")
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        self.main_canvas = tk.Canvas(self.right_panel, bg="#121212", highlightthickness=0)
        self.main_canvas.pack(side="left", fill="both", expand=True)
        
        # Invisible Scrollbar (Created but not packed/visible)
        self.right_scroll = ttk.Scrollbar(self, orient="vertical", command=self.main_canvas.yview)
        self.main_canvas.configure(yscrollcommand=self.right_scroll.set)
        
        # All right panel content goes inside this frame
        self.main_content_container = tk.Frame(self.main_canvas, bg="#121212")
        self.main_canvas.create_window((0, 0), window=self.main_content_container, anchor="nw", width=800)
        
        self.main_content_container.bind("<Configure>", lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        
        # Mouse Wheel Support for smooth scrolling (Optimized for Mac)
        def _on_mousewheel(event):
            # Only scroll if results are currently visible
            if not self.result_state_frame.winfo_viewable():
                return
                
            if event.num == 5 or event.delta < 0:
                direction = 1
            else:
                direction = -1
            self.main_canvas.yview_scroll(direction * 2, "units")
        
        self.main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Right panel will have two states (Empty/Result)
        self.empty_state_frame = ttk.Frame(self.main_content_container, style="TFrame")
        self.result_state_frame = ttk.Frame(self.main_content_container, style="TFrame")
        
        self.build_left_panel()
        self.build_empty_state()
        self.build_result_state()
        
        # Show empty state by default
        self.show_empty_state()

    def build_left_panel(self):
        # Container for padding
        content = tk.Frame(self.left_panel, bg="#0A0A0A", padx=30, pady=40)
        content.pack(fill="both", expand=True)

        # Başlık ve Alt başlık büyütüldü
        tk.Label(content, text="Album Cover Studio", font=("Helvetica", 26, "bold"), bg="#0A0A0A", fg="#FFFFFF").pack(anchor="w", pady=(0, 5))
        tk.Label(content, text="Journal your mood, generate your sound.", font=("Helvetica", 13), bg="#0A0A0A", fg="#B3B3B3").pack(anchor="w", pady=(0, 25))
        
        # Disclaimer yazısı - Panel genişlediği için wraplength artırıldı
        tk.Label(content, text="Note: Generated data is fictional; tracks are real. AI limitations apply.", 
                 font=("Helvetica", 11, "bold italic"), bg="#0A0A0A", fg="#B3B3B3", 
                 wraplength=330, justify="left").pack(anchor="w", pady=(0, 15))

        ttk.Label(content, text="Your Mood / Journal Entry", style="Left.TLabel").pack(anchor="w", pady=(10, 5))
        
        # Rounded Mood Text Area
        mood_frame = RoundedContainer(content, width=340, height=140, radius=15)
        mood_frame.pack(pady=(0, 20))
        self.mood_text = tk.Text(mood_frame, bg="#181818", fg="#FFFFFF", font=("Helvetica", 13), 
                                 insertbackground="white", relief="flat", highlightthickness=0, bd=0)
        self.mood_text.place(x=12, y=12, width=316, height=116)
        self.mood_text.insert("1.0", "How was your day?")
        
        ttk.Label(content, text="Genre", style="Left.TLabel").pack(anchor="w", pady=(0, 5))
        genre_frame = RoundedContainer(content, width=340, height=45, radius=10)
        genre_frame.pack(pady=(0, 20))
        self.genre_combo = ttk.Combobox(genre_frame, values=["Pop", "Rock", "Hip-Hop / Rap", "Electronic", "Indie", "R&B / Soul", "Jazz", "Metal", "Türk Pop", "Klasik"], state="readonly", font=("Helvetica", 13))
        self.genre_combo.set("Pop")
        self.genre_combo.place(x=10, y=2, width=320, height=41)
        
        ttk.Label(content, text="Era", style="Left.TLabel").pack(anchor="w", pady=(0, 5))
        era_frame = RoundedContainer(content, width=340, height=45, radius=10)
        era_frame.pack(pady=(0, 20))
        self.era_combo = ttk.Combobox(era_frame, values=["2020s", "2010s", "2000s", "1990s", "1980s", "1970s"], state="readonly", font=("Helvetica", 13))
        self.era_combo.set("2020s")
        self.era_combo.place(x=10, y=2, width=320, height=41)
        
        ttk.Label(content, text="Track Count (6-14)", style="Left.TLabel").pack(anchor="w", pady=(0, 5))
        track_frame = RoundedContainer(content, width=340, height=45, radius=10)
        track_frame.pack(pady=(0, 35))
        # Custom Modern Counter (Large buttons with spacing)
        self.track_val = tk.IntVar(value=10)
        
        def update_track(delta):
            new_val = self.track_val.get() + delta
            if 6 <= new_val <= 14:
                self.track_val.set(new_val)

        # Value display (Center)
        val_label = tk.Label(track_frame, textvariable=self.track_val, font=("Helvetica", 16, "bold"), 
                             bg="#181818", fg="#FFFFFF")
        val_label.place(x=140, y=7, width=60)

        # Minus Button (Circular and cleaned background)
        self.btn_minus = RoundedButton(track_frame, text="−", command=lambda: update_track(-1), 
                                       width=40, height=35, radius=17, bg_color="#282828", fg_color="#FFFFFF")
        self.btn_minus.configure(bg="#181818") # Remove black corner artifacts
        self.btn_minus.place(x=10, y=5)

        # Plus Button (Circular and cleaned background)
        self.btn_plus = RoundedButton(track_frame, text="+", command=lambda: update_track(1), 
                                      width=40, height=35, radius=17, bg_color="#282828", fg_color="#FFFFFF")
        self.btn_plus.configure(bg="#181818") # Remove black corner artifacts
        self.btn_plus.place(x=290, y=5)
        
        # --- Custom Rounded Generate Button (Centered & Symmetrical) ---
        self.generate_btn = RoundedButton(content, text="GENERATE ALBUM", 
                                          command=self.on_generate_click,
                                          width=340, height=50, radius=25,
                                          font=("Helvetica", 14, "bold"))
        self.generate_btn.pack(pady=(0, 15))
        
        # Status Label büyütüldü (11 -> 12)
        self.status_label = tk.Label(content, text="Status: Ready", font=("Helvetica", 12, "bold italic"), bg="#0A0A0A", fg="#B3B3B3")
        self.status_label.pack(side="left", anchor="sw", pady=10)

    def build_empty_state(self):
        """Welcome screen shown when the app first opens with conceptual transparency warnings"""
        # Clear existing content if any
        for widget in self.empty_state_frame.winfo_children():
            widget.destroy()

        # Main vertical container
        container = tk.Frame(self.empty_state_frame, bg="#121212")
        container.pack(expand=True, fill="both", pady=80)
        
        # Big Icon
        tk.Label(container, text="🎵", font=("Helvetica", 85), bg="#121212", fg="#242424").pack(pady=(0, 10))
        
        # Main Titles
        tk.Label(container, text="Your Generated Album Will Appear Here", 
                 font=("Helvetica", 24, "bold"), bg="#121212", fg="#FFFFFF").pack()
        tk.Label(container, text="Describe your mood on the left and start the journey.", 
                 font=("Helvetica", 15), bg="#121212", fg="#B3B3B3").pack(pady=(5, 50))

        # --- DUALITY WARNING (Enlarged for readability) ---
        warning_box = RoundedContainer(container, width=720, height=300, radius=20, bg="#181818", outline="#282828")
        warning_box.pack()
        
        # Content inside the rounded box
        tk.Label(warning_box, text="⚠️ PROJECT CONCEPT & TRANSPARENCY", 
                 font=("Helvetica", 14, "bold"), bg="#181818", fg="#1DB954").place(x=40, y=30)
        
        notes = [
            ("Fictional Components:", "Album name, artist, and cover art generated by AI are entirely FICTIONAL."),
            ("Real Components:", "The tracklist consists of REAL songs fetched via Last.fm API based on your mood."),
            ("Interface Transparency:", "This project merges fictional concepts with real-world music data (Duality)."),
            ("AI Limitations:", "Generated covers may look abstract. Song matches are based on automated discovery.")
        ]
        
        y_offset = 75
        for title, text in notes:
            tk.Label(warning_box, text=title, font=("Helvetica", 13, "bold"), bg="#181818", fg="#FFFFFF").place(x=40, y=y_offset)
            tk.Label(warning_box, text=text, font=("Helvetica", 12), bg="#181818", fg="#B3B3B3").place(x=40, y=y_offset + 25)
            y_offset += 55


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
        self.list_card = tk.Frame(content, bg="#181818", padx=20, pady=20, highlightthickness=1, highlightbackground="#282828", highlightcolor="#282828")
        self.list_card.pack(fill="both", expand=True)
        
        self.list_header = tk.Label(self.list_card, text="#      Title                                                          Artist", font=("Helvetica", 11, "bold"), bg="#181818", fg="#B3B3B3")
        self.list_header.pack(anchor="w", pady=(0, 10))
        
        # Container for song rows
        # Container for song rows (Simplified since main panel now scrolls)
        self.songs_container = tk.Frame(self.list_card, bg="#181818")
        self.songs_container.pack(fill="both", expand=True)
            
        # --- Custom Rounded Save Button ---
        self.save_btn = RoundedButton(content, text="SAVE ALBUM (JSON + PNG)", 
                                      command=self.on_save_click,
                                      width=450, height=50, radius=25,
                                      font=("Helvetica", 14, "bold"))
        self.save_btn.pack(side="bottom", pady=(20,0))

    # --- SCREEN TRANSITION FUNCTIONS ---
    def show_empty_state(self):
        self.result_state_frame.pack_forget()
        self.empty_state_frame.pack(fill="both", expand=True)
        # Disable scroll for empty state
        self.main_canvas.configure(scrollregion=(0, 0, 0, 0))
        self.main_canvas.yview_moveto(0)

    def show_result_state(self):
        self.empty_state_frame.pack_forget()
        self.result_state_frame.pack(fill="both", expand=True)
        # Enable scroll for result state
        self.main_canvas.update_idletasks()
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    def on_generate_click(self):
        """Reads UI inputs and triggers the ViewModel generation task."""
        journal = self.mood_text.get("1.0", "end-1c")
        genre = self.genre_combo.get()
        era = self.era_combo.get()
        track_count = self.track_val.get()
        
        if self.view_model:
            self.view_model.generate_album(journal, genre, era, track_count)
        else:
            self.status_label.config(text="Status: No ViewModel connected")

    def update_status(self, message):
        """Thread-safe status label update."""
        self.status_label.config(text=f"Status: {message}")

    def handle_success(self, data):
        """Handles successful generation by updating UI components."""
        self.current_album_data = data
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

        for i, track in enumerate(data.get('tracks', []), 1):
            row = tk.Frame(self.songs_container, bg="#181818", padx=15, pady=10)
            row.pack(fill="x")
            
            # Row hover effects removed - Focus only on LISTEN button hover

            tk.Label(row, text=str(i), width=3, anchor="w", bg="#181818", fg="#B3B3B3", font=("Helvetica", 12)).pack(side="left")
            tk.Label(row, text=track['title'], width=40, anchor="w", bg="#181818", fg="#FFFFFF", font=("Helvetica", 14, "bold")).pack(side="left")
            tk.Label(row, text=track['artist'], anchor="w", bg="#181818", fg="#B3B3B3", font=("Helvetica", 12)).pack(side="left")

            # REQ 7: Custom Bordered "LISTEN" Button (Ensures visible border on all platforms)
            # REQ 7: Custom Rounded LISTEN Button (Outline -> Solid)
            listen_btn = RoundedButton(
                row, 
                text="LISTEN", 
                command=lambda u=track.get('url', ''): self.view_model.play_track(u) if self.view_model else None,
                width=100, height=34, radius=17, # radius=height/2 makes it a pill
                outline_mode=True,
                font=("Helvetica", 9, "bold")
            )
            listen_btn.pack(side="right", padx=10)

            # UX Improvement: 1px bottom border for the row
            separator = tk.Frame(self.songs_container, bg="#282828", height=1)
            separator.pack(fill="x", pady=(5, 5))

    def on_save_click(self):
        """Triggers the ViewModel to save the current album data."""
        if not hasattr(self, 'current_album_data') or not self.current_album_data:
            messagebox.showwarning("Warning", "No album to save yet!")
            return
            
        if self.view_model:
            success, msg = self.view_model.save_album(self.current_album_data)
            if success:
                messagebox.showinfo("Success", msg)
            else:
                if "cancelled" not in msg.lower():
                    messagebox.showerror("Error", msg)

if __name__ == "__main__":
    # Support for standalone execution
    root = tk.Tk()
    app = MainPage(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
