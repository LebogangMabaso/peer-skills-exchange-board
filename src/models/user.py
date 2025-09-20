from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class User:
    name: str
    email: str
    skills_offered: List[str] = field(default_factory=list)
    skills_needed: List[str] = field(default_factory=list)
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    
    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")
        
        if not self.email or "@" not in self.email:
            raise ValueError("Valid email is required")
            
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def add_skill_offered(self, skill: str) -> None:
        if skill and skill not in self.skills_offered:
            self.skills_offered.append(skill)
    
    def add_skill_needed(self, skill: str) -> None:
        if skill and skill not in self.skills_needed:
            self.skills_needed.append(skill)
    
    def remove_skill_offered(self, skill: str) -> None:
        if skill in self.skills_offered:
            self.skills_offered.remove(skill)
    
    def remove_skill_needed(self, skill: str) -> None:
        if skill in self.skills_needed:
            self.skills_needed.remove(skill)
    
    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'skills_offered': self.skills_offered,
            'skills_needed': self.skills_needed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'location': self.location,
            'bio': self.bio
        }