# Peer Skills Exchange Board

A platform that connects people who want to exchange skills with each other. Users can offer skills they're good at and request skills they want to learn, creating a peer-to-peer learning community.

## Problem Statement

Many people have valuable skills they can teach others, but lack a structured way to find people who want to learn those skills. Similarly, people who want to learn new skills often don't know where to find mentors or peers who can teach them. This creates a gap in knowledge sharing and skill development.

Traditional learning platforms often require payment, have limited personalization, or lack the peer-to-peer connection that makes learning more engaging and effective.

## Solution

The Peer Skills Exchange Board provides a platform where:
- Users can register and list skills they can offer to teach
- Users can specify skills they want to learn
- An intelligent matching algorithm finds complementary skill exchanges
- Users can connect with each other for skill sharing
- Learning becomes a mutual exchange rather than a one-way transaction

## Key Features

- **User Management**: Register, update profiles, manage skills
- **Skill Matching**: AI-powered algorithm to find compatible skill exchanges
- **Search & Discovery**: Find users by specific skills
- **Match Scoring**: Intelligent scoring system for optimal matches
- **Database Storage**: SQLite database for data persistence
- **Command Line Interface**: Easy-to-use CLI for interaction

## Technology Stack

- **Backend**: Python 3.9+
- **Database**: SQLite
- **Testing**: pytest (Unit Tests), behave (BDD Tests)
- **Architecture**: Object-Oriented Design with clean separation of concerns

## Project Structure

```
peer-skills-exchange-board/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Main application entry point
│   ├── models/                 # Data models
│   │   └── __init__.py
│   ├── database/              # Database layer
│   │   └── __init__.py
│   └── utils/                 # Utility modules
│       └── __init__.py
├── tests/
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   ├── features/              # BDD feature tests
│   │   └── steps/
│   └── acceptance/            # Acceptance tests
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Development Approach

This project follows **Test-Driven Development (TDD)** and **Behavior-Driven Development (BDD)**:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Feature Tests**: Test user scenarios using Gherkin syntax
- **Acceptance Tests**: Test complete user workflows

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd peer-skills-exchange-board
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python src/main.py
```

## Usage

### Adding a User
```
> add
Enter user name: John Doe
Enter skills offered (comma-separated): Python, JavaScript
Enter skills needed (comma-separated): React, Docker
User added successfully with ID: 1
```

### Finding Matches
```
> match 1
Found 2 matches for user 1:
1. Alice (Score: 8.5)
   Skills offered: React, TypeScript
   Skills needed: Python, Machine Learning
   Complementary skills: {'Python': ['user_1', 'user_2']}
```

### Listing Users
```
> list
Found 3 users:
ID: 1 - John Doe
  Skills offered: Python, JavaScript
  Skills needed: React, Docker
```

## Development Roadmap

### Week 1 Development Plan
- **Day 1 (Mon)**: Project setup, folder structure, README
- **Day 2 (Tue)**: Design OOP classes and code skeletons
- **Day 3 (Wed)**: Set up SQLite database and basic CRUD
- **Day 4 (Thu)**: Implement backend logic and unit tests
- **Day 5 (Fri)**: Implement matchmaking algorithm and tests
- **Day 6 (Sat)**: Write acceptance tests and sample data
- **Day 7 (Sun)**: Dockerize project and final testing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Implement the feature
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Future Enhancements

- [ ] Web interface
- [ ] User authentication
- [ ] Real-time notifications
- [ ] Skill categories and tags
- [ ] Rating and review system
- [ ] Mobile app
- [ ] Advanced matching algorithms
- [ ] Calendar integration for scheduling
- [ ] Video call integration