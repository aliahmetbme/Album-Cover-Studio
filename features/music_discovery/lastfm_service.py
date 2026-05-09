LASTFM_BASE_URL = "http://ws.audioscrobbler.com/2.0/"

class LastFMService:
    """Last.fm API'den şarkıları çekme (Müzik Verisi Sorumlusunun Alanı)"""
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_track_info(self, artist, track):
        """Şarkı ve sanatçı bilgilerini Last.fm'den çeker"""
        # Last.fm API çağrısı burada yapılacak
        return {"artist": artist, "track": track, "genre": "Unknown"}
