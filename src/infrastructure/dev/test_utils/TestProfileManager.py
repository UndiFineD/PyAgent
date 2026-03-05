class TestProfileManager:
    #    def __init__(self):
    #        self.profiles = {}

    def add(self, profile):
        self.profiles[profile.name] = profile


__all__ = ["TestProfileManager"]
