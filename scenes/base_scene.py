class BaseScene:
    def __init__(self):
        self.next_scene = None

    def switch_to(self, scene):
        self.next_scene = scene
        
    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def get_next_scene(self):
        return self