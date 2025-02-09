import spotipy, requests

class Spotistats(spotipy.Spotify):
    
    def __init__(self, env):
        scope = "user-library-read,user-top-read,playlist-modify-private,playlist-read-private"
        super().__init__(
            auth_manager=spotipy.oauth2.SpotifyOAuth(
                scope=scope,
                client_id=env["CLIENT_ID"],
                client_secret=env["CLIENT_SECRET"],
                redirect_uri=env["REDIRECT_URI"]
            )
        )
        
    def get_personal_playlists(self):
        all_playlists = []
        playlists = self.current_user_playlists()
        while playlists:
            all_playlists += playlists["items"]
            if playlists["next"]:
                playlists = self.next(playlists)
            else:
                break
        return all_playlists
    
    def get_playlist_track_ids(self, id):
        all_ids = []
        tracks = self.playlist_items(id, fields="next,items.track.id")
        while tracks:
            all_ids += [t["track"]["id"] for t in tracks["items"]]
            if tracks["next"]:
                tracks = self.next(tracks)
            else:
                break 
        return all_ids
    
    def get_tracks_audio_features(self, tracks):
        
        def make_request(ids):
            url = "https://api.stats.fm/api/v1/spotify/audio-features"
            params = {"ids": ",".join(ids)}
            headers = {"User-Agent": ""}

            response = requests.get(url, params=params, headers=headers)
            return response.json()["items"]
        
        all_tracks_features = []
        for i in range(0, len(tracks), 100):
            all_tracks_features += make_request(tracks[i:i+100])
        return all_tracks_features