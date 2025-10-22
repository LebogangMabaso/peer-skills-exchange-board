# Peer Skills Exchange Board

A Python-based platform that connects people who want to learn and teach skills. Users can register their skills, find compatible learning partners, and discover mutual skill exchange opportunities.

## Features

- User registration and profile management
- Skill-based matching algorithm with compatibility scoring
- Interactive command-line interface
- SQLite database for data persistence
- Comprehensive test suite with 75+ tests
- Docker support for containerized deployment

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

## Installation

### Option 1: Using Virtual Environment (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd peer-skills-exchange-board
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Option 2: Using Makefile

1. Clone the repository and navigate to the project directory
2. Run the installation command:
```bash
make install
```

## Running the Application

### Method 1: Direct Python Execution

```bash
# Make sure you're in the project directory
cd peer-skills-exchange-board

# Activate virtual environment (if not already activated)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the interactive application
python -m src.main
```

### Method 2: Using Makefile

```bash
# Run the application
make run
```

### Method 3: Using Docker

```bash
# Build the Docker image
make docker-build

# Run the application in Docker (runs tests by default)
docker run -it --rm peer-skill-exchange python -m src.main
```

## Usage

Once the application starts, you'll see a welcome message and available commands:

```
Welcome to the Peer Skill Exchange Platform!

You can add users, find matches, or list all users.

Available commands:
  add            -> Add a new user
  find <user_id> -> Find matches for a user
  list           -> Show all users
  quit           -> Exit the program
```

### Adding a User

1. Type `add` and press Enter
2. Enter the user's name
3. Enter their email address
4. Enter skills they can offer (comma-separated)
5. Enter skills they want to learn (comma-separated)

Example:
```
> add
Name: John Doe
Email: john@example.com
Skills offered (comma-separated): Python, JavaScript
Skills needed (comma-separated): Machine Learning, React
John Doe added successfully with ID 1
```

### Finding Matches

1. Type `find <user_id>` and press Enter
2. The system will show compatible users ranked by compatibility score

Example:
```
> find 1
Finding matches for John Doe...
  Jane Smith - Compatibility: 1.00
    Can learn: Machine Learning
    Can teach: JavaScript, Python
    Mutual skill exchange possible!
  Bob Wilson - Compatibility: 0.25
    Can learn: React
```

### Listing All Users

Type `list` to see all registered users with their skills.

## Testing

### Run All Tests

```bash
# Using pytest directly
python -m pytest tests/ -v

# Using Makefile
make test
```

### Run Tests with Coverage

```bash
python -m pytest tests/ --cov=src --cov-report=term-missing
```

### Run Tests in Docker

```bash
docker run --rm peer-skill-exchange
```

## Project Structure

```
peer-skills-exchange-board/
├── src/
│   ├── database/
│   │   └── db_handler.py          # Database operations
│   ├── models/
│   │   ├── user.py               # User model
│   │   └── match.py              # Match model
│   ├── utils/
│   │   └── matchmaker.py         # Matching algorithm
│   └── main.py                   # Main application entry point
├── tests/
│   ├── acceptance/               # Acceptance tests
│   ├── unit/                     # Unit tests
│   └── integration/              # Integration tests
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── Makefile                      # Build automation
└── README.md                     # This file
```

## Database

The application uses SQLite for data persistence. The database file (`peer_exchange.db`) is created automatically when you first run the application.

### Database Schema

- **users**: User profiles and basic information
- **skills_offered**: Skills that users can teach
- **skills_needed**: Skills that users want to learn
- **matches**: Compatibility scores and matching data

## Matching Algorithm

The system uses a sophisticated compatibility scoring algorithm:

1. **Base Score**: Number of matching skills between users
2. **Mutual Bonus**: +2.0 points when both users can teach each other
3. **Normalization**: Score is normalized based on total possible matches
4. **Ranking**: Users are ranked by compatibility score (highest first)

## Development

### Code Quality

The project includes several code quality tools:

```bash
# Format code with Black
python -m black src/ tests/

# Check code style with flake8
python -m flake8 src/ tests/

# Type checking with mypy
python -m mypy src/
```

### Adding New Features

1. Create feature branch
2. Add tests for new functionality
3. Implement the feature
4. Run tests to ensure everything works
5. Submit pull request

## Troubleshooting

### Common Issues

1. **Module not found error**: Make sure you're in the project directory and virtual environment is activated
2. **Database errors**: Delete `peer_exchange.db` to reset the database
3. **Permission errors**: Ensure you have write permissions in the project directory

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed correctly
2. Verify Python version is 3.9 or higher
3. Run the test suite to identify any problems
4. Check the project structure matches the expected layout


## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request
