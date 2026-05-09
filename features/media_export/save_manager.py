import os
import json
import re
from tkinter import filedialog

class SaveManager:
    """
    Handles exporting album metadata and cover art to the local filesystem.
    Satisfies REQUIREMENT 8.
    """

    @staticmethod
    def select_directory():
        """
        Opens a directory selection dialog for the user.
        Returns the selected path or an empty string if cancelled.
        """
        folder_selected = filedialog.askdirectory(title="Select Folder to Save Album")
        return folder_selected

    @staticmethod
    def save_album_package(target_folder, album_data, tracklist, pil_image):
        """
        REQ 8: Exports the album as both a JSON file (metadata + tracklist) 
        and a PNG file (the cover image) into an album-specific subfolder.
        """
        if not target_folder:
            return False

        try:
            # 1. Create a clean folder name from the album name
            raw_name = album_data.get("album_name", "Untitled_Album")
            # Sanitize: remove non-alphanumeric (except underscores/hyphens) and replace spaces
            sanitized_name = re.sub(r'(?u)[^-\w.]', '_', raw_name.strip().replace(" ", "_"))
            save_path = os.path.join(target_folder, sanitized_name)
            
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            # 2. Prepare JSON Data (Metadata + Tracklist)
            # REQ 8: 'containing all metadata + tracklist'
            full_package = {
                "metadata": album_data,
                "tracklist": tracklist
            }

            json_path = os.path.join(save_path, "album_details.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(full_package, f, indent=4, ensure_ascii=False)

            # 3. Save Cover Image as PNG
            # REQ 8: 'a PNG file (the cover image)'
            image_path = os.path.join(save_path, "cover.png")
            pil_image.save(image_path, "PNG")

            print(f"Successfully saved album to: {save_path}")
            return True

        except Exception as e:
            print(f"Failed to save album package: {e}")
            return False


# Test etmek için Pillow kütüphanesinden Image modülünü ve tkinter'ı eklemelisin
from PIL import Image
import tkinter as tk

if __name__ == "__main__":
    # Bazı işletim sistemlerinde filedialog'un düzgün çalışması için 
    # görünmez bir ana pencere oluşturmamız gerekebilir.
    root = tk.Tk()
    root.withdraw() 

    print("--- SaveManager Testi Başlatılıyor ---")
    
    manager = SaveManager()
    
    # 1. Kullanıcıdan klasör seçmesini iste
    selected_path = manager.select_directory()
    
    if selected_path:
        # 2. Sahte (Mock) veriler oluştur
        test_album_data = {
            "album_name": "Kordon Whisper",
            "artist_name": "Azure Tides",
            "year": "2015",
            "label": "Saltwater Sounds"
        }
        
        test_tracklist = [
            {"title": "Space Song", "artist": "Beach House"},
            {"title": "Sofia", "artist": "Clairo"}
        ]
        
        # 3. Sahte bir resim objesi yarat (512x512 düz mavi bir resim)
        test_image = Image.new('RGB', (512, 512), color='blue')
        
        # 4. Kaydetme işlemini gerçekleştir
        success = manager.save_album_package(
            selected_path, 
            test_album_data, 
            test_tracklist, 
            test_image
        )
        
        if success:
            print(f"\n✅ BAŞARILI: Albüm '{selected_path}' içine kaydedildi.")
            print("Lütfen klasörü kontrol edin: 'album_details.json' ve 'cover.png' orada mı?")
        else:
            print("\n❌ HATA: Kayıt işlemi başarısız oldu.")
    else:
        print("\n⚠️ İPTAL: Herhangi bir klasör seçilmedi.")