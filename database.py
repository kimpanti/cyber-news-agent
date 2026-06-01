import json
import os
from typing import List, Dict
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    user_id: str
    preferred_style: str = "Standard"
    core_interests: List[str] = Field(default_factory=list)
    category_weights: Dict[str, int] = Field(
        default_factory=lambda: {"Cybersecurity": 0, "Privacy": 0, "AI_Safety": 0, "Data_Governance": 0}
    )

class ProfileDB:
    def __init__(self, filename="/tmp/profiles.json"):
        # We use /tmp/ because cloud hosting has read-only filesystems but allows /tmp writes
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({}, f)

    def get_user(self, user_id: str) -> UserProfile:
        with open(self.filename, "r") as f:
            data = json.load(f)
        if user_id in data:
            return UserProfile(**data[user_id])
        return UserProfile(user_id=user_id)

    def save_user(self, profile: UserProfile):
        with open(self.filename, "r") as f:
            data = json.load(f)
        data[profile.user_id] = profile.model_dump()
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)
