class GeminiService:
    """Gemini'a metin gönderme ve JSON alma (LLM Uzmanının Alanı)"""
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_prompt(self, music_data):
        """Müzik verisine göre görsel oluşturma promptu hazırlar"""
        # Gemini API çağrısı burada yapılacak
        return f"Görsel promptu: {music_data}"
