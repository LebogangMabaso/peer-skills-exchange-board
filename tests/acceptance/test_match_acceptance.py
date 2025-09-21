import pytest
from datetime import datetime
from src.models.match import Match
from src.models.user import User


class TestMatchAcceptance:

    def test_match_creation(self, temp_db):
        user1 = User(
            name="User One",
            email="user1@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript"]
        )
        user2 = User(
            name="User Two", 
            email="user2@example.com",
            skills_offered=["JavaScript"],
            skills_needed=["Python"]
        )
        
        user1_id = temp_db.add_user(user1)
        user2_id = temp_db.add_user(user2)
        
        match = Match(
            user1_id=user1_id,
            user2_id=user2_id,
            compatibility_score=0.85,
            matching_skills=["Python", "JavaScript"]
        )
        
        match_id = temp_db.save_match(match)
        assert match_id > 0
        
    
        matches = temp_db.get_matches_for_user(user1_id)
        assert len(matches) == 1
        assert matches[0].user1_id == user1_id
        assert matches[0].user2_id == user2_id
        assert matches[0].compatibility_score == 0.85
        assert "Python" in matches[0].matching_skills
        assert isinstance(matches[0].created_at, datetime)

    def test_match_to_dict(self, temp_db):
        user1 = User(
            name="User One",
            email="user1@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript"]
        )
        user2 = User(
            name="User Two", 
            email="user2@example.com",
            skills_offered=["JavaScript"],
            skills_needed=["Python"]
        )
        
        user1_id = temp_db.add_user(user1)
        user2_id = temp_db.add_user(user2)
        
        match = Match(
            user1_id=user1_id,
            user2_id=user2_id,
            compatibility_score=0.75,
            matching_skills=["Docker", "AWS"]
        )
        
        match_id = temp_db.save_match(match)
        matches = temp_db.get_matches_for_user(user1_id)
        match_obj = matches[0]
        
        match_dict = match_obj.to_dict()
        
        assert match_dict['user1_id'] == user1_id
        assert match_dict['user2_id'] == user2_id
        assert match_dict['compatibility_score'] == 0.75
        assert match_dict['matching_skills'] == ["Docker", "AWS"]
        assert match_dict['match_id'] == match_id

    def test_save_and_get_match(self, temp_db):
        user1 = User(
            name="Akabongwe Madondo",
            email="akabongwe@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript"]
        )
        user2 = User(
            name="Lebo Mabaso",
            email="lebo@example.com",
            skills_offered=["JavaScript"],
            skills_needed=["Python"]
        )
        
        user1_id = temp_db.add_user(user1)
        user2_id = temp_db.add_user(user2)

        match = Match(
            user1_id=user1_id,
            user2_id=user2_id,
            compatibility_score=0.92,
            matching_skills=["Python"]
        )

        match_id = temp_db.save_match(match)
        assert match_id > 0

        matches = temp_db.get_matches_for_user(user1_id)
        assert len(matches) == 1
        assert matches[0].compatibility_score == 0.92
        assert "Python" in matches[0].matching_skills

    def test_multiple_matches_for_user(self, temp_db):
        target_user = User(
            name="Target User",
            email="target@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript", "React"]
        )
        target_id = temp_db.add_user(target_user)
        
        users = [
            User(name="User A", email="a@example.com", skills_offered=["JavaScript"], skills_needed=["Python"]),
            User(name="User B", email="b@example.com", skills_offered=["React"], skills_needed=["Python"]),
            User(name="User C", email="c@example.com", skills_offered=["Docker"], skills_needed=["Python"])
        ]
        
        user_ids = [temp_db.add_user(user) for user in users]
        
        matches = [
            Match(user1_id=target_id, user2_id=user_ids[0], compatibility_score=0.9, matching_skills=["Python", "JavaScript"]),
            Match(user1_id=target_id, user2_id=user_ids[1], compatibility_score=0.8, matching_skills=["Python", "React"]),
            Match(user1_id=target_id, user2_id=user_ids[2], compatibility_score=0.7, matching_skills=["Python"])
        ]
        
        for match in matches:
            temp_db.save_match(match)
        
        target_matches = temp_db.get_matches_for_user(target_id)
        assert len(target_matches) == 3
        

        scores = [match.compatibility_score for match in target_matches]
        assert scores[0] >= scores[1] >= scores[2]

    def test_match_deletion_when_user_deleted(self, temp_db):
        user1 = User(
            name="User One",
            email="user1@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript"]
        )
        user2 = User(
            name="User Two", 
            email="user2@example.com",
            skills_offered=["JavaScript"],
            skills_needed=["Python"]
        )
        
        user1_id = temp_db.add_user(user1)
        user2_id = temp_db.add_user(user2)
        
        match = Match(
            user1_id=user1_id,
            user2_id=user2_id,
            compatibility_score=0.85,
            matching_skills=["Python", "JavaScript"]
        )
        
        temp_db.save_match(match)
        
        matches1 = temp_db.get_matches_for_user(user1_id)
        matches2 = temp_db.get_matches_for_user(user2_id)
        assert len(matches1) == 1
        assert len(matches2) == 1
        
        temp_db.delete_user(user1_id)
        
        matches1_after = temp_db.get_matches_for_user(user1_id)
        matches2_after = temp_db.get_matches_for_user(user2_id)
        assert len(matches1_after) == 0
        assert len(matches2_after) == 0

    def test_match_with_high_compatibility_score(self, temp_db):
        user1 = User(
            name="Expert Python",
            email="python@example.com",
            skills_offered=["Python", "Django", "Flask", "FastAPI"],
            skills_needed=["JavaScript", "React", "Vue", "Node.js"]
        )
        user2 = User(
            name="Expert JavaScript",
            email="js@example.com",
            skills_offered=["JavaScript", "React", "Vue", "Node.js"],
            skills_needed=["Python", "Django", "Flask", "FastAPI"]
        )
        
        user1_id = temp_db.add_user(user1)
        user2_id = temp_db.add_user(user2)
        
        match = Match(
            user1_id=user1_id,
            user2_id=user2_id,
            compatibility_score=0.95,
            matching_skills=["Python", "Django", "Flask", "FastAPI", "JavaScript", "React", "Vue", "Node.js"]
        )
        
        match_id = temp_db.save_match(match)
        assert match_id > 0
        
        matches = temp_db.get_matches_for_user(user1_id)
        assert len(matches) == 1
        assert matches[0].compatibility_score == 0.95
        assert len(matches[0].matching_skills) == 8

    def test_match_with_low_compatibility_score(self, temp_db):
        user1 = User(
            name="Python Developer",
            email="python@example.com",
            skills_offered=["Python"],
            skills_needed=["Machine Learning"]
        )
        user2 = User(
            name="Web Developer",
            email="web@example.com",
            skills_offered=["HTML", "CSS"],
            skills_needed=["JavaScript"]
        )
        
        user1_id = temp_db.add_user(user1)
        user2_id = temp_db.add_user(user2)
        
        match = Match(
            user1_id=user1_id,
            user2_id=user2_id,
            compatibility_score=0.1,
            matching_skills=[]
        )
        
        match_id = temp_db.save_match(match)
        assert match_id > 0
        
        matches = temp_db.get_matches_for_user(user1_id)
        assert len(matches) == 1
        assert matches[0].compatibility_score == 0.1
        assert len(matches[0].matching_skills) == 0
