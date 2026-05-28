class Door:
    def __init__(self, name, required_key, locked=True):
        self.name = name
        self.required_key = required_key
        self.locked = locked

    def unlock(self):
        self.locked = False
        print(f"{self.name} has been unlocked.")

    def lock(self):
        self.locked = True
        print(f"{self.name} has been locked.")

    def is_locked(self):
        return self.locked

    def show_status(self):
        if self.locked:
            print(f"{self.name} is LOCKED.")
        else:
            print(f"{self.name} is UNLOCKED.")