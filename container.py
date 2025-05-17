class Container:
    def __init__(self, container_id, zone, width, depth, height):
        self.container_id = container_id
        self.zone = zone
        self.width = width
        self.depth = depth
        self.height = height
        self.items = []  # Items placed in this container

    def to_dict(self):
        return {
            "containerId": self.container_id,
            "zone": self.zone,
            "width": self.width,
            "depth": self.depth,
            "height": self.height
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            container_id=data["containerId"],
            zone=data["zone"],
            width=data["width"],
            depth=data["depth"],
            height=data["height"]
        )
