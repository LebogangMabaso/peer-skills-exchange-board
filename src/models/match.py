from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Match:

    user1_id: int
    user2_id: int
    compatibility_score: float
    matching_skills: List[str]
    created_at: datetime = None
    match_id: int = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert match to dictionary"""
        return {
            'match_id': self.match_id,
            'user1_id': self.user1_id,
            'user2_id': self.user2_id,
            'compatibility_score': self.compatibility_score,
            'matching_skills': self.matching_skills,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }