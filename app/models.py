class Lead:
    def __init__(self, name=None, tags=None):
        self.name = name
        self.tags = tags or []

    def __repr__(self):
        return f"Lead(name={self.name}, tags={self.tags})"
