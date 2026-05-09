import threading
from features.generator.gemini_service import GeminiService
from features.music_discovery.lastfm_service import LastFmService
from features.media_export.image_service import ImageService
from features.playback.playback_service import PlaybackService
from features.media_export.save_manager import SaveManager


class AlbumViewModel:
    def __init__(self):
        """
        REQ 9: Background Threading and Status Updates.
        The ViewModel orchestrates the generation pipeline.
        """
        self.gemini_service = GeminiService()
        self.lastfm_service = LastFmService()
        self.image_service = ImageService()
        self.playback_service = PlaybackService()
        self.save_manager = SaveManager()

        
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
                print("Generating album metadata...")
            
            album_metadata = self.gemini_service.generate_album_metadata(
                journal, genre, era, track_count
            )
            
            if not album_metadata:
                raise Exception("Gemini could not generate album metadata.")

            # 2. Last.fm Phase
            if self.on_status_update:
                self.on_status_update("Fetching tracks...")
                print("Fetching tracks...")
            
            tags = album_metadata.get("lastfm_tags", [])
            tracks = self.lastfm_service.fetch_tracks_by_tags(tags, track_count)
            
            if not tracks:
                raise Exception("Last.fm returned no tracks for the provided tags.")
            
            album_metadata["tracks"] = tracks

            # 3. Image Generation Phase (Pollinations)
            if self.on_status_update:
                self.on_status_update("Generating cover...")
                print("Generating cover...")
            
            cover_prompt = album_metadata.get("cover_prompt", "")
            cover_image = self.image_service.fetch_cover_image(cover_prompt, genre)
            
            if not cover_image:
                raise Exception("Could not generate album cover image.")
            
            album_metadata["cover_image"] = cover_image

            # Final Success Callback
            if self.on_generation_success:
                self.on_generation_success(album_metadata)
                print("Album generated successfully!")

        except Exception as e:
            if self.on_error:
                self.on_error(str(e))

    def play_track(self, url: str):
        """
        REQ 7: Route playback request to the PlaybackService.
        """
        return self.playback_service.open_track(url)

    def save_album(self, album_data: dict):
            """
            REQ 8: Routes the save request to SaveManager.
            Fixes 'Image is not JSON serializable' error by separating image from metadata.
            """
            if not album_data:
                return False, "No album data to save."

            folder = self.save_manager.select_directory()
            if not folder:
                return False, "Save cancelled by user."

            metadata_to_save = album_data.copy()
            cover_image = metadata_to_save.pop("cover_image", None) 
            tracks = metadata_to_save.get("tracks", [])
            success = self.save_manager.save_album_package(
                folder, 
                metadata_to_save, 
                tracks, 
                cover_image 
            )
            
            if success:
                return True, "Album saved successfully!"
            else:
                return False, "Failed to save the album."

