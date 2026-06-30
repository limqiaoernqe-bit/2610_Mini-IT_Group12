class SceneManager:
    def __init__(self):
        self.current_scene = None

    def handle_events(self, events):
        if self.current_scene:
            self.current_scene.handle_events(events)

    def update(self):
        if self.current_scene:
            self.current_scene.update()

        if hasattr(self.current_scene, "next_scene") and self.current_scene.next_scene is not None:
            self.current_scene = self.current_scene.next_scene

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)