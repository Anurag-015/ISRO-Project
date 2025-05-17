from datetime import datetime


class Item:
    def __init__(self, item_id, name, width, depth, height, mass=0, priority=50,
                 expiry_date=None, usage_limit=1, preferred_zone="",
                 container_id=None, position=None, uses_remaining=None):
        self.item_id = item_id
        self.name = name
        self.width = width
        self.depth = depth
        self.height = height
        self.mass = mass
        self.priority = priority
        self.expiry_date = expiry_date
        self.usage_limit = usage_limit
        self.preferred_zone = preferred_zone
        self.container_id = container_id
        self.position = position
        self.uses_remaining = uses_remaining if uses_remaining is not None else usage_limit

    def to_dict(self):
        return {
            "itemId": self.item_id,
            "name": self.name,
            "width": self.width,
            "depth": self.depth,
            "height": self.height,
            "mass": self.mass,
            "priority": self.priority,
            "expiryDate": self.expiry_date,
            "usageLimit": self.usage_limit,
            "preferredZone": self.preferred_zone,
            "containerId": self.container_id,
            "position": self.position,
            "usesRemaining": self.uses_remaining
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            item_id=data["itemId"],
            name=data["name"],
            width=data["width"],
            depth=data["depth"],
            height=data["height"],
            mass=data.get("mass", 0),
            priority=data.get("priority", 50),
            expiry_date=data.get("expiryDate"),
            usage_limit=data.get("usageLimit", 1),
            preferred_zone=data.get("preferredZone", ""),
            container_id=data.get("containerId"),
            position=data.get("position"),
            uses_remaining=data.get("usesRemaining")
        )

    def is_waste(self, current_date):
        # Check if item is expired
        if self.expiry_date and current_date:
            try:
                if datetime.fromisoformat(current_date) > datetime.fromisoformat(self.expiry_date):
                    return True, "Expired"
            except ValueError:
                pass

        # Check if item is out of uses
        if self.uses_remaining <= 0:
            return True, "Out of Uses"

        return False, None
