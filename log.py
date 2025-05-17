class Log:
    def __init__(self, log_id, timestamp, user_id, action_type, item_id=None,
                 container_id=None, details=None):
        self.log_id = log_id
        self.timestamp = timestamp
        self.user_id = user_id
        self.action_type = action_type
        self.item_id = item_id
        self.container_id = container_id
        self.details = details or {}

    def to_dict(self):
        return {
            "logId": self.log_id,
            "timestamp": self.timestamp,
            "userId": self.user_id,
            "actionType": self.action_type,
            "itemId": self.item_id,
            "containerId": self.container_id,
            "details": self.details
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            log_id=data["logId"],
            timestamp=data["timestamp"],
            user_id=data["userId"],
            action_type=data["actionType"],
            item_id=data.get("itemId"),
            container_id=data.get("containerId"),
            details=data.get("details")
        )
