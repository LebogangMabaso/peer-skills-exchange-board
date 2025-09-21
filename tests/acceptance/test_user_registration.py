import pytest
from datetime import datetime
from src.models.user import User
from src.database.db_handler import DatabaseHandler


class TestUserRegistration:
    """Acceptance tests for user registration functionality"""

    def test_user_creation_valid(self, temp_db):
        """
        As a new user
        I want to register my profile with my skills
        So that I can find people to exchange skills with
        """
        # Given that I want to create a new account
        user = User(
            name="Thabo Mthembu",
            email="thabo.mthembu@example.com",
            skills_offered=["Python", "JavaScript"],
            skills_needed=["Machine Learning", "Docker"]
        )
        
        # When I register my profile
        user_id = temp_db.add_user(user)
        
        # Then my account should be created successfully
        assert user_id > 0
        
        # And I should be able to retrieve my profile
        retrieved_user = temp_db.get_user(user_id)
        assert retrieved_user is not None
        assert retrieved_user.name == "Thabo Mthembu"
        assert retrieved_user.email == "thabo.mthembu@example.com"
        assert "Python" in retrieved_user.skills_offered
        assert "Machine Learning" in retrieved_user.skills_needed
        assert retrieved_user.user_id == user_id
        assert isinstance(retrieved_user.created_at, datetime)
    
    def test_user_creation_empty_name(self, temp_db):
        """
        As a new user
        I want to register with an empty name
        So that I can see what happens when I make a mistake
        """
        # Given that I try to register with an empty name
        # When I attempt to create an account
        # Then I should get an error message
        with pytest.raises(ValueError, match="Name cannot be empty"):
            User(name="", email="sipho.ndlovu@example.com")
    
    def test_user_creation_invalid_email(self, temp_db):
        """
        As a new user
        I want to register with a bad email address
        So that I can see what happens when I make a typo
        """
        # Given that I try to register with an invalid email
        # When I attempt to create an account
        # Then I should get an error message
        with pytest.raises(ValueError, match="Valid email is required"):
            User(name="Sipho Ndlovu", email="not-a-real-email")

    def test_user_registration_with_minimal_info(self, temp_db):
        """
        As a new user
        I want to register with just my name and email
        So that I can add my skills later
        """
        # Given that I only want to provide basic information
        user = User(
            name="Nomsa Dlamini",
            email="nomsa.dlamini@example.com"
        )
        
        # When I register my profile
        user_id = temp_db.add_user(user)
        
        # Then my account should be created successfully
        assert user_id > 0
        
        # And I should have empty skill lists that I can fill later
        retrieved_user = temp_db.get_user(user_id)
        assert retrieved_user.name == "Nomsa Dlamini"
        assert retrieved_user.email == "nomsa.dlamini@example.com"
        assert retrieved_user.skills_offered == []
        assert retrieved_user.skills_needed == []

    def test_user_registration_with_duplicate_email_fails(self, temp_db):
        """
        As a new user
        I want to register with an email that's already taken
        So that I can see what happens when I try to use someone else's email
        """
        # Given that someone else already registered with an email
        user1 = User(
            name="Lungile Khumalo",
            email="lungile.khumalo@example.com",
            skills_offered=["Python"]
        )
        
        # When the first person registers
        user1_id = temp_db.add_user(user1)
        assert user1_id > 0
        
        # And I try to register with the same email
        user2 = User(
            name="Mandla Zulu",
            email="lungile.khumalo@example.com",
            skills_offered=["JavaScript"]
        )
        
        # Then my registration should fail
        with pytest.raises(Exception):  # SQLite will raise an integrity error
            temp_db.add_user(user2)

    def test_user_registration_with_whitespace_name_fails(self, temp_db):
        """
        As a new user
        I want to register with just spaces as my name
        So that I can see what happens when I don't enter a real name
        """
        # Given that I try to register with only spaces
        # When I attempt to create an account
        # Then I should get an error message
        with pytest.raises(ValueError, match="Name cannot be empty"):
            User(
                name="   ",
                email="busi.mthembu@example.com"
            )

    def test_user_registration_with_many_skills(self, temp_db):
        """
        As a new user
        I want to register with lots of different skills
        So that I can show off how much I know
        """
        # Given that I have many skills to offer and need
        many_skills = [f"Skill{i}" for i in range(20)]
        user = User(
            name="Zanele Mkhize",
            email="zanele.mkhize@example.com",
            skills_offered=many_skills[:10],
            skills_needed=many_skills[10:]
        )
        
        # When I register my profile
        user_id = temp_db.add_user(user)
        
        # Then my account should be created successfully
        assert user_id > 0
        
        # And all my skills should be saved correctly
        retrieved_user = temp_db.get_user(user_id)
        assert len(retrieved_user.skills_offered) == 10
        assert len(retrieved_user.skills_needed) == 10
        assert "Skill0" in retrieved_user.skills_offered
        assert "Skill19" in retrieved_user.skills_needed

    def test_user_registration_with_special_characters(self, temp_db):
        """
        As a new user
        I want to register with my real name that has special characters
        So that my profile shows my actual name correctly
        """
        # Given that I have a name with special characters and technical skills
        user = User(
            name="José María O'Connor-Smith",
            email="jose.maria@example.com",
            skills_offered=["C++", "C#", "R", "Go", "Rust"],
            skills_needed=["Machine Learning", "Data Science", "AI/ML"]
        )
        
        # When I register my profile
        user_id = temp_db.add_user(user)
        
        # Then my account should be created successfully
        assert user_id > 0
        
        # And my name and skills should be stored exactly as I entered them
        retrieved_user = temp_db.get_user(user_id)
        assert retrieved_user.name == "José María O'Connor-Smith"
        assert "C++" in retrieved_user.skills_offered
        assert "AI/ML" in retrieved_user.skills_needed

    def test_user_registration_preserves_created_at_timestamp(self, temp_db):
        """
        As a new user
        I want my registration time to be recorded
        So that I can see when I joined the platform
        """
        # Given that I want to register
        import time
        before_registration = time.time()
        
        user = User(
            name="Jabulani Nkosi",
            email="jabulani.nkosi@example.com"
        )
        
        # When I register my profile
        user_id = temp_db.add_user(user)
        after_registration = time.time()
        
        # Then my registration time should be recorded
        retrieved_user = temp_db.get_user(user_id)
        assert retrieved_user.created_at is not None
        
        # And it should be within a reasonable time range
        created_timestamp = retrieved_user.created_at.timestamp()
        assert before_registration <= created_timestamp <= after_registration
