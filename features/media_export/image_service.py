import requests
from PIL import Image
from io import BytesIO
from urllib.parse import quote

class ImageService:
    def __init__(self):
        
        # Pollinations.ai URL (Image bytes data using image.pollinations.ai)
        self.base_url = "https://image.pollinations.ai/prompt/"

    def fetch_cover_image(self, prompt, genre_style=""):
        # Combine prompt with genre style
        if genre_style:
            full_prompt = f"{prompt}, in the style of {genre_style} album art"
        else:
            full_prompt = prompt
        
        print(f"\n--- [LOG] Pollinations Prompt ---\n{full_prompt}\n---------------------------------\n")
        
        # URL içinde boşluk ve özel karakterleri güvenli hale getiriyoruz
        encoded_prompt = quote(full_prompt)
        
        # Width and height settings (600x600 preferred for Spotify style)
        # Pollinations logo is removed with nologo=true parameter.
        image_url = f"{self.base_url}{encoded_prompt}?width=600&height=600&seed=42&nologo=true"

        try:
            print(f"Image is being generated: {image_url}")
            
            # REQ 9: Uzun süren işlemler için timeout ekliyoruz.
            # (Bu metodun kendisi threading.Thread içinde çağrılmalıdır)
            response = requests.get(image_url, timeout=90)
            response.raise_for_status()

            # Downloaded binary data into an image object (PIL Image)
            img_data = BytesIO(response.content)
            img = Image.open(img_data).convert("RGB") 
            return img 
            
        except Exception as e:
            print(f"Image download error: {e}")
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
