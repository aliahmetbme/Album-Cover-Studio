import requests
from PIL import Image
from io import BytesIO
from urllib.parse import quote

class ImageService:
    def __init__(self):
        """
        Pollinations.ai için servis sınıfı.
        Herhangi bir API anahtarı gerektirmez, sadece URL üzerinden görsel oluşturur.
        """
        # Pollinations.ai için temel URL (Resim bytes verisi almak için image.pollinations.ai kullanılmalı)
        self.base_url = "https://image.pollinations.ai/prompt/"

    def fetch_cover_image(self, prompt, genre_style=""):
        """
        Gemini'dan gelen cover prompt'unu alır, seçilen türün görsel stiliyle birleştirir
        ve Pollinations.ai üzerinden albüm kapağını indirir.
        
        REQUIREMENT 6: The cover prompt returned by Gemini must be combined with 
        the chosen genre's visual style description and forwarded to an AI image generation service.
        """
        # REQ 6: Prompt ile tür stilini birleştiriyoruz
        if genre_style:
            full_prompt = f"{prompt}, in the style of {genre_style} album art"
        else:
            full_prompt = prompt
        
        # URL içinde boşluk ve özel karakterleri güvenli hale getiriyoruz
        encoded_prompt = quote(full_prompt)
        
        # Genişlik ve yükseklik ayarlarını yapıyoruz (Spotify stili için 600x600 tercih edildi)
        # nologo=true parametresi ile Pollinations logosunu kaldırıyoruz.
        image_url = f"{self.base_url}{encoded_prompt}?width=600&height=600&seed=42&nologo=true"

        try:
            print(f"Resim oluşturuluyor: {image_url}")
            
            # REQ 9: Uzun süren işlemler için timeout ekliyoruz.
            # (Bu metodun kendisi threading.Thread içinde çağrılmalıdır)
            response = requests.get(image_url, timeout=90)
            response.raise_for_status()

            # İndirilen binary veriyi bir resim nesnesine (PIL Image) dönüştür
            img_data = BytesIO(response.content)
            img = Image.open(img_data).convert("RGB")
            return img
            
        except Exception as e:
            print(f"Resim indirme hatası: {e}")
            return None

# --- GÖRSEL UZMANI İÇİN TEST BÖLÜMÜ ---
if __name__ == "__main__":
    service = ImageService()
    # Gemini'dan gelen örnek bir prompt
    test_prompt = "An artistic shot of the Izmir Kordon at late afternoon, cool blues and greys, indie aesthetic"
    
    # Test için görseli indir
    image = service.fetch_cover_image(test_prompt, "Indie Pop")
    
    if image:
        print("Resim başarıyla indirildi!")
        image.show() # Resmi bilgisayarda anlık olarak görüntüler
        # image.save("test_cover.png") # Kaydetmek istersen bu satırı açabilirsin
    else:
        print("Resim alınamadı.")
