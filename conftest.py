# conftest.py
import pytest
import tempfile
import os
from src.database.db_handler import DatabaseHandler
from src.models.user import User

@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    db_handler = DatabaseHandler(path)
    db_handler.initialize_database()

    yield db_handler

    os.unlink(path)

@pytest.fixture
def sample_user():
    """Single sample user"""
    return User(
        name="Malachai Mckenzie",
        email="malachai@example.com",
        skills_offered=["Python", "JavaScript"],
        skills_needed=["Machine Learning", "Docker"]
    )

@pytest.fixture
def sample_users():
    """Multiple sample users"""
    return [
        User(
            name="Akabongwe Madondo",
            email="akabongwe@example.com",
            skills_offered=["Python", "Data Science"],
            skills_needed=["JavaScript", "React"]
        ),
        User(
            name="Lebo Mabaso",
            email="lebo@example.com",
            skills_offered=["JavaScript", "React"],
            skills_needed=["Python", "Machine Learning"]
        ),
        User(
            name="Cayla Darries",
            email="cayla@example.com",
            skills_offered=["Machine Learning", "Docker"],
            skills_needed=["Web Design", "CSS"]
        )
    ]

@pytest.fixture
def perfect_match_users():
    """Users with perfect mutual skill exchange"""
    return [
        User(
            name="Alice Perfect",
            email="alice.perfect@example.com",
            skills_offered=["Python", "Django", "Flask"],
            skills_needed=["JavaScript", "React", "Vue"]
        ),
        User(
            name="Bob Perfect",
            email="bob.perfect@example.com",
            skills_offered=["JavaScript", "React", "Vue"],
            skills_needed=["Python", "Django", "Flask"]
        )
    ]

@pytest.fixture
def one_way_match_users():
    """Users with one-way learning match"""
    return [
        User(
            name="Expert Teacher",
            email="expert@example.com",
            skills_offered=["Machine Learning", "Deep Learning", "AI"],
            skills_needed=["Guitar", "Cooking", "Photography"]
        ),
        User(
            name="Eager Learner",
            email="learner@example.com",
            skills_offered=["Guitar", "Cooking", "Photography"],
            skills_needed=["Machine Learning", "Deep Learning", "AI"]
        )
    ]

@pytest.fixture
def no_match_users():
    """Users with no matching skills"""
    return [
        User(
            name="Tech Person",
            email="tech@example.com",
            skills_offered=["Python", "JavaScript", "React"],
            skills_needed=["Machine Learning", "Docker", "AWS"]
        ),
        User(
            name="Creative Person",
            email="creative@example.com",
            skills_offered=["Painting", "Music", "Writing"],
            skills_needed=["Photography", "Design", "Art"]
        )
    ]

@pytest.fixture
def complex_match_users():
    """Users with complex matching scenarios"""
    return [
        User(
            name="Full Stack Dev",
            email="fullstack@example.com",
            skills_offered=["Python", "JavaScript", "React", "Django"],
            skills_needed=["Machine Learning", "Docker", "AWS", "Kubernetes"]
        ),
        User(
            name="ML Engineer",
            email="ml@example.com",
            skills_offered=["Machine Learning", "Docker", "AWS", "Kubernetes"],
            skills_needed=["Python", "JavaScript", "Data Analysis"]
        ),
        User(
            name="DevOps Engineer",
            email="devops@example.com",
            skills_offered=["Docker", "AWS", "Kubernetes", "Terraform"],
            skills_needed=["Python", "JavaScript", "Monitoring"]
        )
    ]
