import pytest
from datetime import datetime
from src.models.user import User

class TestUser:
    """Unit tests for User class"""
    
    def test_user_creation_valid(self):
        """Test creating a user with valid data"""
        user = User(
            name="Malachai Mckenzie",
            email="malachai@example.com",
            skills_offered=["Python", "JavaScript"],
            skills_needed=["Machine Learning", "Docker"]
        )
        
        assert user.name == "Malachai Mckenzie"
        assert user.email == "malachai@example.com"
        assert "Python" in user.skills_offered
        assert "Machine Learning" in user.skills_needed
        assert user.user_id is None  # Not set initially
        assert isinstance(user.created_at, datetime)
    
    def test_user_creation_empty_name(self):
        """Test that empty name raises ValueError"""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            User(name="", email="malachai@example.com")
    
    def test_user_creation_invalid_email(self):
        """Test that invalid email raises ValueError"""
        with pytest.raises(ValueError, match="Valid email is required"):
            User(name="Malachai Mckenzie", email="invalid-email")
    
    def test_add_skill_offered(self):
        """Test adding skills to offered list"""
        user = User(name="Malachai", email="malachai@example.com")
        
        user.add_skill_offered("Python")
        assert "Python" in user.skills_offered
        
        # Test duplicate skill (should not add twice)
        user.add_skill_offered("Python")
        assert user.skills_offered.count("Python") == 1
    
    def test_add_skill_needed(self):
        """Test adding skills to needed list"""
        user = User(name="Malachai", email="malachai@example.com")
        
        user.add_skill_needed("Docker")
        assert "Docker" in user.skills_needed
    
    def test_remove_skill_offered(self):
        """Test removing skills from offered list"""
        user = User(
            name="Malachai", 
            email="malachai@example.com",
            skills_offered=["Python", "JavaScript"]
        )
        
        user.remove_skill_offered("Python")
        assert "Python" not in user.skills_offered
        assert "JavaScript" in user.skills_offered
    
    def test_remove_skill_needed(self):
        """Test removing skills from needed list"""
        user = User(
            name="Malachai", 
            email="malachai@example.com",
            skills_needed=["Docker", "AWS"]
        )
        
        user.remove_skill_needed("Docker")
        assert "Docker" not in user.skills_needed
        assert "AWS" in user.skills_needed
    
    def test_to_dict(self):
        """Test converting user to dictionary"""
        user = User(
            name="Malachai",
            email="malachai@example.com",
            skills_offered=["Python"],
            skills_needed=["Docker"]
        )
        user.user_id = 1
        
        user_dict = user.to_dict()
        
        assert user_dict['name'] == "Malachai"
        assert user_dict['email'] == "malachai@example.com"
        assert user_dict['user_id'] == 1
        assert user_dict['skills_offered'] == ["Python"]
        assert user_dict['skills_needed'] == ["Docker"]
