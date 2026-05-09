import os
import requests
from dotenv import load_dotenv

load_dotenv()

LASTFM_BASE_URL = "https://ws.audioscrobbler.com/2.0/"

class LastFmService:
    def __init__(self):
        self.api_key = os.getenv("LASTFM_API_KEY")
        if not self.api_key:
            raise ValueError("Last.fm API Key bulunamadı! .env dosyasını kontrol edin.")

    def fetch_tracks_by_tags(self, tags, target_count):
        
        all_tracks = []
        seen_track_ids = set() # To prevent duplicate tracks.

        for tag in tags:
            params = {
                "method": "tag.gettoptracks",
                "tag": tag,
                "api_key": self.api_key,
                "format": "json",
                "limit": target_count # to get enough samples for each tag
            }

            try:
                # REQUIREMENT: User-Agent and timeout settings applied.
                headers = {"User-Agent": "AlbumCoverStudio/1.0"}
                response = requests.get(LASTFM_BASE_URL, params=params, headers=headers, timeout=15)
                response.raise_for_status()
                data = response.json()
                
                # JSON içindeki şarkı listesine ulaşalım
                tracks = data.get("tracks", {}).get("track", [])

                for t in tracks:
                    # Şarkı adı + Sanatçı adını ID olarak kullanıp kopyaları engelliyoruz
                    track_id = f"{t['name']} - {t['artist']['name']}".lower()
                    
                    if track_id not in seen_track_ids:
                        seen_track_ids.add(track_id)
                        all_tracks.append({
                            "title": t['name'],
                            "artist": t['artist']['name'],
                            "url": t['url'] # REQ 7: "Listen" butonu için gereken link
                        })
                        
                    # İstenen sayıya ulaştıysak döngüden çıkabiliriz
                    if len(all_tracks) >= target_count:
                        break

            except Exception as e:
                print(f"Last.fm hata ({tag}): {e}")
            
            if len(all_tracks) >= target_count:
                break

        return all_tracks[:target_count]

# --- MÜZİK SORUMLUSU İÇİN TEST BÖLÜMÜ ---
if __name__ == "__main__":
    service = LastFmService()
    # Senin az önce Gemini'dan aldığın gerçek etiketleri buraya koyup test ediyoruz
    test_tags = ["indie pop", "dream pop", "atmospheric"]
    
    print(f"'{test_tags}' etiketleri için gerçek şarkılar aranıyor...")
    songs = service.fetch_tracks_by_tags(test_tags, 8)
    
    if songs:
        print(f"\n--- Toplam {len(songs)} Gerçek Şarkı Bulundu ---")
        for i, song in enumerate(songs, 1):
            print(f"{i}. {song['title']} - {song['artist']}")
    else:
        print("Şarkı bulunamadı. API Key'inizi kontrol edin.")