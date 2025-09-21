import pytest
from src.models.user import User
from src.utils.matchmaker import Matchmaker

class TestComplexMatchingScenarios:
    """Acceptance tests for complex matching scenarios and user interactions"""

    def test_new_user_finds_matches_after_registration(self, temp_db, sample_users):
        """Test that a newly registered user can find matches with existing users"""
        matchmaker = Matchmaker(temp_db)
        for user in sample_users:
            temp_db.add_user(user)

        new_user = User(
            name="New Developer",
            email="new@dev.com",
            skills_offered=["Python", "Django"],
            skills_needed=["React", "Frontend Development"]
        )
        new_user_id = temp_db.add_user(new_user)

        matches = matchmaker.find_matches(new_user_id)
        assert len(matches) >= 1

        mutual_matches = [
            (mid, score)
            for mid, score in matches
            if matchmaker.get_match_details(new_user_id, mid)["is_mutual_exchange"]
        ]
        assert len(mutual_matches) >= 1

        top_match_id = matches[0][0]
        details = matchmaker.get_match_details(new_user_id, top_match_id)
        assert isinstance(details["user1_can_learn"], list)
        assert isinstance(details["user2_can_learn"], list)

    def test_skill_updates_affect_matching_results(self, temp_db, sample_users):
        """Test that updating user skills affects their matching results"""
        matchmaker = Matchmaker(temp_db)

        user1 = sample_users[0]
        user2 = sample_users[1]
        user1_id = temp_db.add_user(user1)
        user2_id = temp_db.add_user(user2)

        updated_user1 = temp_db.get_user(user1_id)
        updated_user1.skills_needed = list(set(updated_user1.skills_needed + user2.skills_offered))
        updated_user1.skills_offered = list(set(updated_user1.skills_offered + user2.skills_needed))
        temp_db.update_user(updated_user1)

        matches = matchmaker.find_matches(user1_id)

        found = False
        for mid, _ in matches:
            if mid == user2_id:
                details = matchmaker.get_match_details(user1_id, mid)
                assert details["is_mutual_exchange"] is True
                found = True
                break
        assert found is True

    def test_multiple_users_complex_matching_scenarios(self, temp_db, sample_users):
        """Test complex matching scenarios with multiple users"""
        matchmaker = Matchmaker(temp_db)
        user_ids = [temp_db.add_user(u) for u in sample_users]
        all_matches = {uid: matchmaker.find_matches(uid) for uid in user_ids}

        for uid, matches in all_matches.items():
            assert len(matches) >= 1

        mutual_exchanges = 0
        for i, uid in enumerate(user_ids):
            for j, other_uid in enumerate(user_ids):
                if i != j:
                    details = matchmaker.get_match_details(uid, other_uid)
                    if details["is_mutual_exchange"]:
                        mutual_exchanges += 1

        assert mutual_exchanges >= 1
