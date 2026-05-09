import threading
from features.generator.gemini_service import GeminiService
from features.music_discovery.lastfm_service import LastFmService
from features.media_export.image_service import ImageService

class AlbumViewModel:
    def __init__(self):
        """
        REQ 9: Background Threading and Status Updates.
        The ViewModel orchestrates the generation pipeline.
        """
        self.gemini_service = GeminiService()
        self.lastfm_service = LastFmService()
        self.image_service = ImageService()
        
        # Callback properties to communicate with the View
        self.on_status_update = None
        self.on_generation_success = None
        self.on_error = None

    def generate_album(self, journal, genre, era, track_count):
        """
        Starts the generation process in a separate thread to keep the UI responsive.
        """
        thread = threading.Thread(
            target=self._generation_task,
            args=(journal, genre, era, track_count),
            daemon=True
        )
        thread.start()

    def _generation_task(self, journal, genre, era, track_count):
        try:
            # 1. Gemini Phase
            if self.on_status_update:
                self.on_status_update("Gemini is thinking...")
            
            album_metadata = self.gemini_service.generate_album_metadata(
                journal, genre, era, track_count
            )
            
            if not album_metadata:
                raise Exception("Gemini could not generate album metadata.")

            # 2. Last.fm Phase
            if self.on_status_update:
                self.on_status_update("Fetching tracks...")
            
            tags = album_metadata.get("lastfm_tags", [])
            tracks = self.lastfm_service.fetch_tracks_by_tags(tags, track_count)
            
            if not tracks:
                raise Exception("Last.fm returned no tracks for the provided tags.")
            
            album_metadata["tracks"] = tracks

            # 3. Image Generation Phase (Pollinations)
            if self.on_status_update:
                self.on_status_update("Generating cover...")
            
            cover_prompt = album_metadata.get("cover_prompt", "")
            cover_image = self.image_service.fetch_cover_image(cover_prompt, genre)
            
            if not cover_image:
                raise Exception("Could not generate album cover image.")
            
            album_metadata["cover_image"] = cover_image

            # Final Success Callback
            if self.on_generation_success:
                self.on_generation_success(album_metadata)

        except Exception as e:
            if self.on_error:
                self.on_error(str(e))
