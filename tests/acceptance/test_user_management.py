import pytest
from datetime import datetime
from src.models.user import User
from src.models.match import Match


class TestUserManagement:
    """Acceptance tests for user management functionality"""

    def test_add_user(self, temp_db):
        """Test adding a user to the database"""
        user = User(
            name="Bongani Mthembu",
            email="bongani.mthembu@example.com",
            skills_offered=["Python", "Docker"],
            skills_needed=["Machine Learning", "AWS"]
        )
        
        user_id = temp_db.add_user(user)
        assert user_id > 0
        assert isinstance(user_id, int)

    def test_get_user(self, temp_db):
        """Test retrieving a user from the database"""
        user = User(
            name="Malachai Mckenzie",
            email="malachai@example.com",
            skills_offered=["Python", "Docker"],
            skills_needed=["Machine Learning", "AWS"]
        )
        
        user_id = temp_db.add_user(user)
        retrieved_user = temp_db.get_user(user_id)

        assert retrieved_user is not None
        assert retrieved_user.name == "Malachai Mckenzie"
        assert retrieved_user.email == "malachai@example.com"
        assert "Python" in retrieved_user.skills_offered
        assert "Docker" in retrieved_user.skills_offered
        assert "Machine Learning" in retrieved_user.skills_needed
        assert retrieved_user.user_id == user_id

    def test_get_user_nonexistent(self, temp_db):
        """Test retrieving a non-existent user returns None"""
        user = temp_db.get_user(999)
        assert user is None

    def test_get_user_by_email(self, temp_db):
        """Test retrieving user by email address"""
        user = User(name="Cayla Darries", email="unique@example.com")
        user_id = temp_db.add_user(user)

        retrieved = temp_db.get_user_by_email("unique@example.com")
        assert retrieved is not None
        assert retrieved.email == "unique@example.com"
        assert retrieved.user_id == user_id

        non_existent = temp_db.get_user_by_email("notfound@example.com")
        assert non_existent is None

    def test_get_all_users(self, temp_db):
        """Test retrieving all users from database"""
        users = [
            User(name="Akabongwe Madondo", email="akabongwe@example.com", skills_offered=["Python"]),
            User(name="Lebo Mabaso", email="lebo@example.com", skills_offered=["JavaScript"]),
            User(name="Cayla Darries", email="cayla@example.com", skills_offered=["Docker"])
        ]
        
        for user in users:
            temp_db.add_user(user)

        all_users = temp_db.get_all_users()
        assert len(all_users) == 3
        assert all(isinstance(user, User) for user in all_users)
        assert any(user.name == "Akabongwe Madondo" for user in all_users)
        assert any(user.name == "Lebo Mabaso" for user in all_users)
        assert any(user.name == "Cayla Darries" for user in all_users)

    def test_update_user(self, temp_db):
        """Test updating user information in database"""
        user = User(
            name="Malachai Mckenzie",
            email="malachai@example.com",
            skills_offered=["Python", "Docker"],
            skills_needed=["Machine Learning", "AWS"]
        )
        
        user_id = temp_db.add_user(user)
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

    def test_delete_user(self, temp_db):
        """Test deleting a user from database"""
        user = User(
            name="Malachai Mckenzie",
            email="malachai@example.com",
            skills_offered=["Python", "Docker"],
            skills_needed=["Machine Learning", "AWS"]
        )
        
        user_id = temp_db.add_user(user)
        assert temp_db.get_user(user_id) is not None

        result = temp_db.delete_user(user_id)
        assert result is True
        assert temp_db.get_user(user_id) is None

    def test_user_skill_addition(self, temp_db):
        """Test adding skills to user profile through database operations"""
        user = User(
            name="Skill Learner",
            email="learner@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript"]
        )
        user_id = temp_db.add_user(user)
        
        # Add new skills
        user = temp_db.get_user(user_id)
        user.add_skill_offered("Django")
        user.add_skill_offered("Flask")
        user.add_skill_needed("React")
        user.add_skill_needed("Vue")
        
        temp_db.update_user(user)
        
        # Verify skills were added
        updated_user = temp_db.get_user(user_id)
        assert "Django" in updated_user.skills_offered
        assert "Flask" in updated_user.skills_offered
        assert "React" in updated_user.skills_needed
        assert "Vue" in updated_user.skills_needed

    def test_user_skill_removal(self, temp_db):
        """Test removing skills from user profile through database operations"""
        user = User(
            name="Skill Remover",
            email="remover@example.com",
            skills_offered=["Python", "Django", "Flask"],
            skills_needed=["JavaScript", "React", "Vue"]
        )
        user_id = temp_db.add_user(user)
        
        # Remove some skills
        user = temp_db.get_user(user_id)
        user.remove_skill_offered("Django")
        user.remove_skill_needed("React")
        
        temp_db.update_user(user)
        
        # Verify skills were removed
        updated_user = temp_db.get_user(user_id)
        assert "Django" not in updated_user.skills_offered
        assert "React" not in updated_user.skills_needed
        assert "Python" in updated_user.skills_offered  # Should still be there
        assert "JavaScript" in updated_user.skills_needed  # Should still be there

    def test_user_deletion_with_matches(self, temp_db):
        """Test deleting a user who has matches"""
        user_a = User(
            name="User A",
            email="a@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript"]
        )
        
        user_b = User(
            name="User B",
            email="b@example.com",
            skills_offered=["JavaScript"],
            skills_needed=["Python"]
        )
        
        user_a_id = temp_db.add_user(user_a)
        user_b_id = temp_db.add_user(user_b)
        
        # Create a match
        match = Match(
            user1_id=user_a_id,
            user2_id=user_b_id,
            compatibility_score=0.9,
            matching_skills=["Python", "JavaScript"]
        )
        match_id = temp_db.save_match(match)
        
        # Verify match exists
        matches = temp_db.get_matches_for_user(user_a_id)
        assert len(matches) == 1
        
        # Delete user A
        success = temp_db.delete_user(user_a_id)
        assert success is True
        
        # Verify user A is deleted
        assert temp_db.get_user(user_a_id) is None
        
        # Verify user B still exists
        assert temp_db.get_user(user_b_id) is not None
        
        # Verify match is also deleted
        matches_after = temp_db.get_matches_for_user(user_b_id)
        assert len(matches_after) == 0

    def test_duplicate_skill_handling(self, temp_db):
        """Test that duplicate skills are handled correctly in updates"""
        user = User(
            name="Duplicate Tester",
            email="duplicate@example.com",
            skills_offered=["Python"],
            skills_needed=["JavaScript"]
        )
        user_id = temp_db.add_user(user)
        
        # Update with duplicate skills (remove duplicates before updating)
        user = temp_db.get_user(user_id)
        user.skills_offered = list(set(["Python", "Python", "Django", "Django"]))  # Remove duplicates
        user.skills_needed = list(set(["JavaScript", "JavaScript", "React", "React"]))  # Remove duplicates
        
        success = temp_db.update_user(user)
        assert success is True
        
        # Verify duplicates are handled (should be unique)
        updated_user = temp_db.get_user(user_id)
        assert len(updated_user.skills_offered) == 2  # Python, Django
        assert len(updated_user.skills_needed) == 2   # JavaScript, React
        assert updated_user.skills_offered.count("Python") == 1
        assert updated_user.skills_needed.count("JavaScript") == 1

    def test_user_profile_completeness(self, temp_db):
        """Test user profile with all optional fields"""
        user = User(
            name="Complete Profile",
            email="complete@example.com",
            skills_offered=["Python", "Django", "Flask"],
            skills_needed=["JavaScript", "React", "Vue"],
            location="New York, NY",
            bio="Full-stack developer with 5 years experience"
        )
        user_id = temp_db.add_user(user)
        
        retrieved_user = temp_db.get_user(user_id)
        assert retrieved_user.name == "Complete Profile"
        assert retrieved_user.email == "complete@example.com"
        assert retrieved_user.location == "New York, NY"
        assert retrieved_user.bio == "Full-stack developer with 5 years experience"
        assert len(retrieved_user.skills_offered) == 3
        assert len(retrieved_user.skills_needed) == 3
        assert retrieved_user.created_at is not None
