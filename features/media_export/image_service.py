class ImageService:
    """Pollinations.ai'den kapak resmi indirme (Sistem Asistanının Alanı)"""
    def generate_image_url(self, prompt):
        """Prompt'a göre Pollinations.ai URL'si oluşturur"""
        encoded_prompt = prompt.replace(" ", "%20")
        return f"https://pollinations.ai/p/{encoded_prompt}"
