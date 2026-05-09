import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# installing dotenv api keys
load_dotenv()


class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(model_name="gemini-2.5-flash")

    def generate_album_cover(self, journal_text, genre, era, track_count):
        prompt = f"""Based on this journal entry and parameters, return ONLY valid JSON
with this schema:
{{
 "album_name": "string",
 "artist_name": "string",
 "year": "string",
 "label": "string",
 "mood_description": "string",
 "cover_prompt": "string",
 "lastfm_tags": ["array of 4-6 lowercase Last.fm tag strings"]
}}

Input Parameters:
- Journal: "{journal_text}"
- Genre: {genre}
- Era: {era}
- Track Count: {track_count}
"""

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            # Strip markdown fences if Gemini added them
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.strip().rstrip("`").strip()
            
            album_data = json.loads(text)
            return album_data

        except json.JSONDecodeError as e:
            print(f"Parsing Error: Gemini'ın gönderdiği veri JSON formatına uygun değil. {e}")
            return None
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return None



if __name__ == "__main__":
    service = GeminiService()
    print("Gemini test ediliyor...")
    
    result = service.generate_album_cover(
        journal_text="İzmir'de kordon boyunda yürüyorum, rüzgar sert ama huzurluyum.",
        genre="Indie",
        era="2010s",
        track_count=10
    )
    
    if result:
        print("\n--- Başarıyla Oluşturulan Albüm Verisi ---")
        print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
        print("\nAlbüm verisi oluşturulamadı.")