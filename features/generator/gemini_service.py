import os
import json
from google import genai
from dotenv import load_dotenv

# installing dotenv api keys
load_dotenv()


class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # REQ 4: Using google-genai SDK for 2026 models
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash"

    def generate_album_metadata(self, journal_text, genre, era, track_count):
        """
        REQ 4: Gemini creates the album metadata based on user inputs.
        Returns a dictionary containing album details and Last.fm tags.
        """
        prompt = f"""
Act as a creative Music Director and Concept Artist. Your goal is to transform a personal journal entry into a cohesive fictional album concept.

Current User Inputs:
- Journal Entry: "{journal_text}"
- Music Genre: {genre}
- Target Era: {era}
- Expected Track Count: {track_count}

Instructions for the JSON fields:
1. "album_name" & "artist_name": Must be fictional and creatively reflect the mood of the journal.
2. "mood_description": A short sentence explaining how the "{genre}" genre and "{era}" era evoke the emotions in the journal.
3. "cover_prompt": MUST BE IN ENGLISH. Provide a highly detailed, artistic description for an AI image generator (Pollinations.ai). Describe lighting, textures, and style (e.g., "{genre} album art style"). DO NOT include text or artist names.
4. "lastfm_tags": Provide 4-6 lowercase tags. To ensure Last.fm API returns real songs:
   - Always include the English version of the genre (e.g., if genre is "Türk Pop", use "turkish pop").
   - Do NOT use special Turkish characters (use 'o' instead of 'ö', 's' instead of 'ş').
   - Include the era (e.g., "{era}").
   - Add broad emotion tags (e.g., "happy", "love", "melancholic").

Return ONLY valid JSON with this schema:
{{
 "album_name": "string",
 "artist_name": "string",
 "year": "{era[:4]}",
 "label": "string",
 "mood_description": "string",
 "cover_prompt": "string",
 "lastfm_tags": ["tag1", "tag2", "tag3", "tag4"]
}}
"""

        print(f"\n--- [LOG] Gemini Prompt ---\n{prompt}\n---------------------------\n")

        try:
            # Generate content using the new SDK
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            
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
            print(f"Raw Text: {text}")
            return None
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return None



if __name__ == "__main__":
    service = GeminiService()
    print(f"Gemini ({service.model_id}) test ediliyor...")
    
    result = service.generate_album_metadata(
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