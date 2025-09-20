import pytest
from src.utils.matchmaker import Matchmaker
from src.models.user import User

class TestMatchmaker:
    
    def test_calculate_compatibility_same_user(self, temp_db):
        matchmaker = Matchmaker(temp_db)
        user = User(name="Same User", email="same@example.com")
        user.user_id = 1
        
        score, skills = matchmaker.calculate_compatibility_score(user, user)
        assert score == 0.0
        assert skills == []
    
    def test_calculate_compatibility_perfect_match(self, temp_db):
        matchmaker = Matchmaker(temp_db)
        
        user1 = User(
            name="Fundi",
            email="fundi@example.com",
            skills_offered=["Python", "Data Science"],
            skills_needed=["JavaScript", "React"]
        )
        user1.user_id = 1
        
        user2 = User(
            name="akabongwe",
            email="akabongwe@example.com", 
            skills_offered=["JavaScript", "React"],
            skills_needed=["Python", "Data Science"]
        )
        user2.user_id = 2
        
        score, matching_skills = matchmaker.calculate_compatibility_score(user1, user2)

        assert score > 0.5
        assert "Python" in matching_skills
        assert "JavaScript" in matching_skills
        assert len(matching_skills) == 4 
    
    def test_calculate_compatibility_partial_match(self, temp_db):
        matchmaker = Matchmaker(temp_db)
        
        user1 = User(
            name="fundi",
            email="fundi@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript", "Docker", "AWS"]
        )
        user1.user_id = 1
        
        user2 = User(
            name="akabongwe",
            email="akabongwe@example.com",
            skills_offered=["JavaScript"],
            skills_needed=["Python", "Machine Learning"]
        )
        user2.user_id = 2
        
        score, matching_skills = matchmaker.calculate_compatibility_score(user1, user2)
    
        assert 0 < score < 1.0
        assert "Python" in matching_skills
        assert "JavaScript" in matching_skills
    
    def test_calculate_compatibility_no_match(self, temp_db):
        matchmaker = Matchmaker(temp_db)
        
        user1 = User(
            name="fundi",
            email="fundi@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript"]
        )
        user1.user_id = 1
        
        user2 = User(
            name="akabongwe",
            email="akabongwe@example.com",
            skills_offered=["Docker"],
            skills_needed=["AWS"]
        )
        user2.user_id = 2
        
        score, matching_skills = matchmaker.calculate_compatibility_score(user1, user2)
        
        assert score == 0.0
        assert matching_skills == []
    
    def test_find_matches(self, temp_db, sample_users):
        matchmaker = Matchmaker(temp_db)
        
        user_ids = []
        for user in sample_users:
            user_id = temp_db.add_user(user)
            user.user_id = user_id
            user_ids.append(user_id)
        
        matches = matchmaker.find_matches(user_ids[0])
        
        assert len(matches) >= 1
        
        if len(matches) > 1:
            assert matches[0][1] >= matches[1][1]
        
        for match_id, score in matches:
            assert isinstance(match_id, int)
            assert isinstance(score, float)
            assert 0 <= score <= 1.0
    
    def test_get_match_details(self, temp_db):
        matchmaker = Matchmaker(temp_db)
    
        user1 = User(
            name="fundi",
            email="fundi@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript"]
        )
        user2 = User(
            name="Akabongwe", 
            email="akabongwe@example.com",
            skills_offered=["JavaScript"],
            skills_needed=["Python"]
        )
        
        user1_id = temp_db.add_user(user1)
        user2_id = temp_db.add_user(user2)
        
        details = matchmaker.get_match_details(user1_id, user2_id)
        
        assert 'user1' in details
        assert 'user2' in details
        assert 'compatibility_score' in details
        assert 'user1_can_learn' in details
        assert 'user2_can_learn' in details
        assert 'is_mutual_exchange' in details
        
        assert details['user1_can_learn'] == ['JavaScript']
        assert details['user2_can_learn'] == ['Python']
        assert details['is_mutual_exchange'] is True