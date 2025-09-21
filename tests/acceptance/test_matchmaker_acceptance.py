import pytest
from src.utils.matchmaker import Matchmaker
from src.models.user import User


class TestMatchmakerAcceptance:
    """Acceptance tests for matchmaker functionality"""

    def test_calculate_compatibility_same_user(self, temp_db):
        """
        As a user
        I want to see what happens when I try to match with myself
        So that I understand the system won't let me match with myself
        """
        # Given that I have a profile
        matchmaker = Matchmaker(temp_db)
        my_profile = User(name="Thabo Mthembu", email="thabo.mthembu@example.com")
        my_profile.user_id = 1
        
        # When I try to match with myself
        match_score, matching_skills = matchmaker.calculate_compatibility_score(my_profile, my_profile)
        
        # Then I should get zero because I can't match with myself
        assert match_score == 0.0
        assert matching_skills == []

    def test_calculate_compatibility_perfect_match(self, temp_db):
        """
        As a user looking for skill exchanges
        I want to find someone who perfectly matches my needs
        So that we can both learn exactly what we want from each other
        """
        # Given that I know Python and Data Science but want to learn JavaScript and React
        matchmaker = Matchmaker(temp_db)
        
        my_profile = User(
            name="Fundi Mthembu",
            email="fundi.mthembu@example.com",
            skills_offered=["Python", "Data Science"],
            skills_needed=["JavaScript", "React"]
        )
        my_id = temp_db.add_user(my_profile)
        my_profile.user_id = my_id
        
        # And someone else knows JavaScript and React but wants to learn Python and Data Science
        their_profile = User(
            name="Akabongwe Dlamini",
            email="akabongwe.dlamini@example.com", 
            skills_offered=["JavaScript", "React"],
            skills_needed=["Python", "Data Science"]
        )
        their_id = temp_db.add_user(their_profile)
        their_profile.user_id = their_id
        
        # When I check how well we match
        match_score, skills_we_can_exchange = matchmaker.calculate_compatibility_score(my_profile, their_profile)

        # Then we should have a high match score because we perfectly complement each other
        assert match_score > 0.5
        assert "Python" in skills_we_can_exchange
        assert "JavaScript" in skills_we_can_exchange
        assert len(skills_we_can_exchange) == 4

    def test_calculate_compatibility_partial_match(self, temp_db):
        """
        As a user looking for skill exchanges
        I want to find someone who partially matches my needs
        So that we can still learn some things from each other
        """
        # Given that I know Python but want to learn JavaScript, Docker, and AWS
        matchmaker = Matchmaker(temp_db)
        
        my_profile = User(
            name="Fundi Mthembu",
            email="fundi.mthembu@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript", "Docker", "AWS"]
        )
        my_id = temp_db.add_user(my_profile)
        my_profile.user_id = my_id
        
        # And someone else knows JavaScript but wants to learn Python and Machine Learning
        their_profile = User(
            name="Akabongwe Dlamini",
            email="akabongwe.dlamini@example.com",
            skills_offered=["JavaScript"],
            skills_needed=["Python", "Machine Learning"]
        )
        their_id = temp_db.add_user(their_profile)
        their_profile.user_id = their_id
        
        # When I check how well we match
        match_score, skills_we_can_exchange = matchmaker.calculate_compatibility_score(my_profile, their_profile)
    
        # Then we should have a moderate match score because we can exchange some skills
        assert 0 < match_score < 1.0
        assert "Python" in skills_we_can_exchange
        assert "JavaScript" in skills_we_can_exchange

    def test_calculate_compatibility_no_match(self, temp_db):
        """
        As a user looking for skill exchanges
        I want to see what happens when someone has completely different skills
        So that I understand when there's no potential for learning
        """
        # Given that I know Python and want to learn JavaScript
        matchmaker = Matchmaker(temp_db)
        
        my_profile = User(
            name="Fundi Mthembu",
            email="fundi.mthembu@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript"]
        )
        my_id = temp_db.add_user(my_profile)
        my_profile.user_id = my_id
        
        # And someone else knows Docker and wants to learn AWS (completely different skills)
        their_profile = User(
            name="Akabongwe Dlamini",
            email="akabongwe.dlamini@example.com",
            skills_offered=["Docker"],
            skills_needed=["AWS"]
        )
        their_id = temp_db.add_user(their_profile)
        their_profile.user_id = their_id
        
        # When I check how well we match
        match_score, skills_we_can_exchange = matchmaker.calculate_compatibility_score(my_profile, their_profile)
        
        # Then we should have no match because we can't teach each other anything
        assert match_score == 0.0
        assert skills_we_can_exchange == []

    def test_find_matches(self, temp_db, sample_users):
        """
        As a user looking for skill exchanges
        I want to find people I can learn from
        So that I can see all my potential matches
        """
        # Given that there are several users on the platform
        matchmaker = Matchmaker(temp_db)
        
        user_ids = []
        for user in sample_users:
            user_id = temp_db.add_user(user)
            user.user_id = user_id
            user_ids.append(user_id)
        
        # When I search for matches
        my_matches = matchmaker.find_matches(user_ids[0])
        
        # Then I should find at least one person I can learn from
        assert len(my_matches) >= 1
        
        # And if there are multiple matches, they should be sorted by best match first
        if len(my_matches) > 1:
            assert my_matches[0][1] >= my_matches[1][1]
        
        # And each match should have a valid ID and score
        for match_id, match_score in my_matches:
            assert isinstance(match_id, int)
            assert isinstance(match_score, float)
            assert 0 <= match_score <= 1.0

    def test_get_match_details(self, temp_db):
        """
        As a user looking at a potential match
        I want to see detailed information about what we can learn from each other
        So that I can decide if this person is right for me
        """
        # Given that I know Python and want to learn JavaScript
        matchmaker = Matchmaker(temp_db)
    
        my_profile = User(
            name="Fundi Mthembu",
            email="fundi.mthembu@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript"]
        )
        their_profile = User(
            name="Akabongwe Dlamini", 
            email="akabongwe.dlamini@example.com",
            skills_offered=["JavaScript"],
            skills_needed=["Python"]
        )
        
        my_id = temp_db.add_user(my_profile)
        their_id = temp_db.add_user(their_profile)
        
        # When I look at the detailed information about our match
        match_details = matchmaker.get_match_details(my_id, their_id)
        
        # Then I should see all the important information
        assert 'user1' in match_details
        assert 'user2' in match_details
        assert 'compatibility_score' in match_details
        assert 'user1_can_learn' in match_details
        assert 'user2_can_learn' in match_details
        assert 'is_mutual_exchange' in match_details
        
        # And I should see that I can learn JavaScript from them
        assert match_details['user1_can_learn'] == ['JavaScript']
        # And they can learn Python from me
        assert match_details['user2_can_learn'] == ['Python']
        # And we can both learn from each other
        assert match_details['is_mutual_exchange'] is True

    def test_find_matches_with_ranking(self, temp_db):
        """Test that matches are properly ranked by compatibility score"""
        matchmaker = Matchmaker(temp_db)
        
        # Create a target user
        target_user = User(
            name="Target User",
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

    def test_mutual_exchange_detection(self, temp_db):
        """Test detection of mutual skill exchanges"""
        matchmaker = Matchmaker(temp_db)
        
        user1 = User(
            name="User One",
            email="user1@example.com",
            skills_offered=["Python", "Django"],
            skills_needed=["JavaScript", "React"]
        )
        user2 = User(
            name="User Two",
            email="user2@example.com",
            skills_offered=["JavaScript", "React"],
            skills_needed=["Python", "Django"]
        )
        
        user1_id = temp_db.add_user(user1)
        user2_id = temp_db.add_user(user2)
        
        details = matchmaker.get_match_details(user1_id, user2_id)
        
        assert details['is_mutual_exchange'] is True
        assert len(details['user1_can_learn']) == 2  # JavaScript, React
        assert len(details['user2_can_learn']) == 2  # Python, Django
        assert "JavaScript" in details['user1_can_learn']
        assert "Python" in details['user2_can_learn']

    def test_one_way_learning_detection(self, temp_db):
        """Test detection of one-way learning scenarios"""
        matchmaker = Matchmaker(temp_db)
        
        expert = User(
            name="Expert",
            email="expert@example.com",
            skills_offered=["Python", "Machine Learning"],
            skills_needed=["Guitar", "Cooking"]  # Completely different skills
        )
        
        learner = User(
            name="Learner",
            email="learner@example.com",
            skills_offered=["Guitar", "Cooking"],
            skills_needed=["Python", "Machine Learning"]
        )
        
        expert_id = temp_db.add_user(expert)
        learner_id = temp_db.add_user(learner)
        
        # Check from expert's perspective
        details = matchmaker.get_match_details(expert_id, learner_id)
        assert details['is_mutual_exchange'] is True  # Both can learn from each other
        assert len(details['user1_can_learn']) == 2  # Expert can learn Guitar, Cooking
        assert len(details['user2_can_learn']) == 2  # Learner can learn Python, ML

    def test_empty_skills_handling(self, temp_db):
        """Test matching behavior with users who have empty skill lists"""
        matchmaker = Matchmaker(temp_db)
        
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
        
        # Skilled user should not find matches
        matches_skilled = matchmaker.find_matches(skilled_id)
        assert len(matches_skilled) == 0
        
        # Unskilled user should not find matches
        matches_unskilled = matchmaker.find_matches(unskilled_id)
        assert len(matches_unskilled) == 0

    def test_duplicate_skills_handling(self, temp_db):
        """Test that duplicate skills are handled correctly in matching"""
        matchmaker = Matchmaker(temp_db)
        
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
