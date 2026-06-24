class SceneManager:
    def __init__(self, scene):
        self.current_scene = scene

    def handle_events(self, events):
        self.current_scene.handle_events(events)

    def update(self):
        self.current_scene.update()

        # scene switching system
        if hasattr(self.current_scene, "next_scene") and self.current_scene.next_scene is not None:
            self.current_scene = self.current_scene.next_scene

    def draw(self, screen):
        self.current_scene.draw(screen)