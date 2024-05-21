import pygame

class SoundsService:
    def __init__(self) -> None:
        self._sounds = {}

    def play(self, path: str, loops: int = 0):
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(path)
        if "game_loop" in path:
            self._sounds[path].play(loops=loops).set_volume(0.2)
        else:
            self._sounds[path].play(loops=loops).set_volume(0.6)

    def stop_sound(self, path: str):
        if path in self._sounds:
            self._sounds[path].stop()

    def stop_all(self):
        for sound in self._sounds.values():
            sound.stop()
