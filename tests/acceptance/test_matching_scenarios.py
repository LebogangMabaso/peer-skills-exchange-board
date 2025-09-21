import pytest
from src.models.user import User
from src.utils.matchmaker import Matchmaker


class TestMatchingScenarios:
    """Acceptance tests for various matching scenarios"""

    def test_perfect_mutual_match(self, temp_db):
        """
        As a user looking for skill exchanges
        I want to find someone who can teach me what I need while I teach them what they need
        So that we can both learn from each other
        """
        # Given that I know Python and Django but want to learn JavaScript and React
        user_a = User(
            name="Thandeka Mthembu",
            email="thandeka.mthembu@example.com",
            skills_offered=["Python", "Django"],
            skills_needed=["JavaScript", "React"]
        )
        
        # And someone else knows JavaScript and React but wants to learn Python and Django
        user_b = User(
            name="Sipho Dlamini",
            email="sipho.dlamini@example.com",
            skills_offered=["JavaScript", "React"],
            skills_needed=["Python", "Django"]
        )
        
        # When we both register on the platform
        user_a_id = temp_db.add_user(user_a)
        user_b_id = temp_db.add_user(user_b)
        
        matchmaker = Matchmaker(temp_db)
        
        # Then I should find them as a perfect match
        matches_a = matchmaker.find_matches(user_a_id)
        matches_b = matchmaker.find_matches(user_b_id)
        
        assert len(matches_a) == 1
        assert len(matches_b) == 1
        assert matches_a[0][0] == user_b_id
        assert matches_b[0][0] == user_a_id
        
        # And we should both be able to learn from each other
        details_a = matchmaker.get_match_details(user_a_id, user_b_id)
        details_b = matchmaker.get_match_details(user_b_id, user_a_id)
        
        assert details_a["is_mutual_exchange"] is True
        assert details_b["is_mutual_exchange"] is True
        assert details_a["compatibility_score"] > 0.8  # Should be high for perfect match

    def test_one_way_learning_match(self, temp_db):
        """Test one-way learning scenario (A can teach B, but B can't teach A)"""
        user_a = User(
            name="Expert",
            email="expert@example.com",
            skills_offered=["Python", "Machine Learning"],
            skills_needed=["Guitar", "Cooking"]  # Completely different skills
        )
        
        user_b = User(
            name="Learner",
            email="learner@example.com",
            skills_offered=["Guitar", "Cooking"],
            skills_needed=["Python", "Machine Learning"]
        )
        
        user_a_id = temp_db.add_user(user_a)
        user_b_id = temp_db.add_user(user_b)
        
        matchmaker = Matchmaker(temp_db)
        
        # A should find B as a match (A can teach B)
        matches_a = matchmaker.find_matches(user_a_id)
        assert len(matches_a) == 1
        assert matches_a[0][0] == user_b_id
        
        # B should find A as a match (B can learn from A)
        matches_b = matchmaker.find_matches(user_b_id)
        assert len(matches_b) == 1
        assert matches_b[0][0] == user_a_id
        
        # Check that it's actually a mutual exchange (both can learn from each other)
        details = matchmaker.get_match_details(user_a_id, user_b_id)
        assert details["is_mutual_exchange"] is True
        assert len(details["user1_can_learn"]) == 2  # A can learn Guitar, Cooking from B
        assert len(details["user2_can_learn"]) == 2  # B can learn Python, ML from A

    def test_no_match_scenario(self, temp_db):
        """Test scenario where no matches are found"""
        user_a = User(
            name="Tech Person",
            email="tech@example.com",
            skills_offered=["Python", "JavaScript"],
            skills_needed=["Machine Learning", "AI"]
        )
        
        user_b = User(
            name="Creative Person",
            email="creative@example.com",
            skills_offered=["Painting", "Music"],
            skills_needed=["Photography", "Writing"]
        )
        
        user_a_id = temp_db.add_user(user_a)
        user_b_id = temp_db.add_user(user_b)
        
        matchmaker = Matchmaker(temp_db)
        
        # Neither should find matches
        matches_a = matchmaker.find_matches(user_a_id)
        matches_b = matchmaker.find_matches(user_b_id)
        
        assert len(matches_a) == 0
        assert len(matches_b) == 0

    def test_partial_match_scenario(self, temp_db):
        """Test partial match where only some skills align"""
        user_a = User(
            name="Full Stack Dev",
            email="fullstack@example.com",
            skills_offered=["Python", "JavaScript", "React", "Django"],
            skills_needed=["Machine Learning", "Docker", "AWS"]
        )
        
        user_b = User(
            name="ML Engineer",
            email="ml@example.com",
            skills_offered=["Machine Learning", "Docker", "AWS", "Kubernetes"],
            skills_needed=["Python", "JavaScript", "Data Analysis"]
        )
        
        user_a_id = temp_db.add_user(user_a)
        user_b_id = temp_db.add_user(user_b)
        
        matchmaker = Matchmaker(temp_db)
        
        matches_a = matchmaker.find_matches(user_a_id)
        matches_b = matchmaker.find_matches(user_b_id)
        
        assert len(matches_a) == 1
        assert len(matches_b) == 1
        
        # Check partial match details
        details = matchmaker.get_match_details(user_a_id, user_b_id)
        assert details["is_mutual_exchange"] is True
        assert len(details["user1_can_learn"]) == 3  # A can learn ML, Docker, AWS
        assert len(details["user2_can_learn"]) == 2  # B can learn Python, JavaScript

    def test_multiple_users_ranking(self, temp_db):
        """Test that matches are properly ranked by compatibility score"""
        # Create a target user
        target_user = User(
            name="Target",
            email="target@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript", "React", "Docker"]
        )
        target_id = temp_db.add_user(target_user)
        
        # Create multiple potential matches with different compatibility levels
        perfect_match = User(
            name="Perfect Match",
            email="perfect@example.com",
            skills_offered=["JavaScript", "React", "Docker"],
            skills_needed=["Python"]
        )
        
        good_match = User(
            name="Good Match",
            email="good@example.com",
            skills_offered=["JavaScript", "React"],
            skills_needed=["Python", "Docker"]
        )
        
        okay_match = User(
            name="Okay Match",
            email="okay@example.com",
            skills_offered=["JavaScript"],
            skills_needed=["Python", "React", "Docker"]
        )
        
        perfect_id = temp_db.add_user(perfect_match)
        good_id = temp_db.add_user(good_match)
        okay_id = temp_db.add_user(okay_match)
        
        matchmaker = Matchmaker(temp_db)
        matches = matchmaker.find_matches(target_id)
        
        # Should have 3 matches
        assert len(matches) == 3
        
        # Matches should be ranked by compatibility score (highest first)
        match_ids = [match[0] for match in matches]
        match_scores = [match[1] for match in matches]
        
        # Scores should be in descending order
        assert match_scores[0] >= match_scores[1] >= match_scores[2]
        
        # Perfect match should be first
        assert match_ids[0] == perfect_id

    def test_self_matching_excluded(self, temp_db):
        """Test that users don't match with themselves"""
        user = User(
            name="Self User",
            email="self@example.com",
            skills_offered=["Python", "JavaScript"],
            skills_needed=["Machine Learning", "Docker"]
        )
        
        user_id = temp_db.add_user(user)
        matchmaker = Matchmaker(temp_db)
        
        matches = matchmaker.find_matches(user_id)
        
        # Should not find any matches (including self)
        assert len(matches) == 0

    def test_empty_skills_handling(self, temp_db):
        """Test matching behavior with users who have empty skill lists"""
        user_with_skills = User(
            name="Skilled User",
            email="skilled@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript"]
        )
        
        user_without_skills = User(
            name="Unskilled User",
            email="unskilled@example.com",
            skills_offered=[],
            skills_needed=[]
        )
        
        skilled_id = temp_db.add_user(user_with_skills)
        unskilled_id = temp_db.add_user(user_without_skills)
        
        matchmaker = Matchmaker(temp_db)
        
        # Skilled user should not find matches
        matches_skilled = matchmaker.find_matches(skilled_id)
        assert len(matches_skilled) == 0
        
        # Unskilled user should not find matches
        matches_unskilled = matchmaker.find_matches(unskilled_id)
        assert len(matches_unskilled) == 0

    def test_duplicate_skills_handling(self, temp_db):
        """Test that duplicate skills are handled correctly"""
        user_a = User(
            name="User A",
            email="a@example.com",
            skills_offered=["Python", "Python", "JavaScript"],  # Duplicate Python
            skills_needed=["Machine Learning", "ML", "Machine Learning"]  # Duplicate ML
        )
        
        user_b = User(
            name="User B",
            email="b@example.com",
            skills_offered=["Machine Learning", "ML"],  # Duplicate ML
            skills_needed=["Python", "Python", "JavaScript"]  # Duplicate Python
        )
        
        user_a_id = temp_db.add_user(user_a)
        user_b_id = temp_db.add_user(user_b)
        
        matchmaker = Matchmaker(temp_db)
        
        matches_a = matchmaker.find_matches(user_a_id)
        matches_b = matchmaker.find_matches(user_b_id)
        
        # Should still find matches despite duplicates
        assert len(matches_a) == 1
        assert len(matches_b) == 1
        
        # Check that duplicates don't affect scoring
        details = matchmaker.get_match_details(user_a_id, user_b_id)
        assert details["is_mutual_exchange"] is True
        # Should only count unique skills (ML and Machine Learning are different skills)
        assert len(details["user1_can_learn"]) == 2  # "Machine Learning" and "ML"
        assert len(details["user2_can_learn"]) == 2  # "Python" and "JavaScript"
