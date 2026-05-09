import webbrowser

class PlaybackService:
    def open_track(self, url: str):
        """
        REQ 7: Opens the provided Last.fm track URL in the default web browser.
        Returns True if successful, False if URL is empty or an error occurs.
        """
        if not url:
            return False
        
        try:
            webbrowser.open(url)
            return True
        except Exception:
            return False
