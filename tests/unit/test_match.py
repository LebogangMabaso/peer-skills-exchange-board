import pytest
from datetime import datetime
from src.models.match import Match

class TestMatch:
    """Unit tests for Match class"""
    
    def test_match_creation(self):
        """Test creating a match with valid data"""
        match = Match(
            user1_id=1,
            user2_id=2,
            compatibility_score=0.85,
            matching_skills=["Python", "JavaScript"]
        )
        
        assert match.user1_id == 1
        assert match.user2_id == 2
        assert match.compatibility_score == 0.85
        assert "Python" in match.matching_skills
        assert isinstance(match.created_at, datetime)
    
    def test_match_to_dict(self):
        """Test converting match to dictionary"""
        match = Match(
            user1_id=1,
            user2_id=2,
            compatibility_score=0.75,
            matching_skills=["Docker", "AWS"]
        )
        match.match_id = 10
        
        match_dict = match.to_dict()
        
        assert match_dict['user1_id'] == 1
        assert match_dict['user2_id'] == 2
        assert match_dict['compatibility_score'] == 0.75
        assert match_dict['matching_skills'] == ["Docker", "AWS"]
        assert match_dict['match_id'] == 10
