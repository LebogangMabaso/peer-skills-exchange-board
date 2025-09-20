import pytest
from src.models.user import User
from src.models.match import Match

class TestDatabaseHandler:

    def test_initialize_database(self, temp_db):
        user = User(name="Test User", email="test@example.com")
        user_id = temp_db.add_user(user)
        assert user_id > 0

    def test_add_user(self, temp_db, sample_user):
        user_id = temp_db.add_user(sample_user)
        assert user_id > 0
        assert isinstance(user_id, int)

    def test_get_user(self, temp_db, sample_user):
        user_id = temp_db.add_user(sample_user)
        retrieved_user = temp_db.get_user(user_id)

        assert retrieved_user is not None
        assert retrieved_user.name == "Malachai Mckenzie"
        assert retrieved_user.email == "malachai@example.com"
        assert "Python" in retrieved_user.skills_offered
        assert "Docker" in retrieved_user.skills_needed
        assert retrieved_user.user_id == user_id

    def test_get_user_nonexistent(self, temp_db):
        user = temp_db.get_user(999)
        assert user is None

    def test_get_user_by_email(self, temp_db):
        user = User(name="Cayla Darries", email="unique@example.com")
        temp_db.add_user(user)

        retrieved = temp_db.get_user_by_email("unique@example.com")
        assert retrieved is not None
        assert retrieved.email == "unique@example.com"

        non_existent = temp_db.get_user_by_email("notfound@example.com")
        assert non_existent is None

    def test_get_all_users(self, temp_db, sample_users):
        for user in sample_users:
            temp_db.add_user(user)

        all_users = temp_db.get_all_users()

        assert len(all_users) == 3
        assert all(isinstance(user, User) for user in all_users)
        assert any(user.name == "Akabongwe Madondo" for user in all_users)
        assert any(user.name == "Lebo Mabaso" for user in all_users)
        assert any(user.name == "Cayla Darries" for user in all_users)

    def test_update_user(self, temp_db, sample_user):
        user_id = temp_db.add_user(sample_user)

        updated_user = temp_db.get_user(user_id)
        updated_user.name = "Updated Name"
        updated_user.skills_offered = ["Python", "JavaScript", "Go"]
        updated_user.skills_needed = ["Docker", "Kubernetes"]

        result = temp_db.update_user(updated_user)
        assert result is True

        retrieved = temp_db.get_user(user_id)
        assert retrieved.name == "Updated Name"
        assert "Go" in retrieved.skills_offered
        assert "Kubernetes" in retrieved.skills_needed

    def test_delete_user(self, temp_db, sample_user):
        user_id = temp_db.add_user(sample_user)
        assert temp_db.get_user(user_id) is not None

        result = temp_db.delete_user(user_id)
        assert result is True
        assert temp_db.get_user(user_id) is None

    def test_save_and_get_match(self, temp_db, sample_users):
        user1_id = temp_db.add_user(sample_users[0])
        user2_id = temp_db.add_user(sample_users[1])  

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
