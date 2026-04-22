import pygame
import os

class MusicPlayer:
    def __init__(self, music_dir):
        self.music_dir = music_dir
        # Получаем список всех mp3 и wav файлов в папке
        self.playlist = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
        self.current_index = 0
        self.is_playing = False
        
        pygame.mixer.init()

    def play(self):
        if not self.playlist:
            return
        
        # Загружаем текущий трек
        track_path = os.path.join(self.music_dir, self.playlist[self.current_index])
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        # Циклическое переключение вперед
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def prev_track(self):
        # Циклическое переключение назад
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def get_current_track_name(self):
        if not self.playlist:
            return "No music found"
        return self.playlist[self.current_index]