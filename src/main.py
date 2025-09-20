import os
from src.database.db_handler import DatabaseHandler
from src.utils.matchmaker import Matchmaker
from src.models.user import User

def main():
    print("Welcome to the Peer Skill Exchange Platform!\n")
    
    db_path = os.environ.get('DATABASE_PATH', 'peer_exchange.db')
    db_handler = DatabaseHandler(db_path)
    db_handler.initialize_database()
    
    matchmaker = Matchmaker(db_handler)
    
    print("You can add users, find matches, or list all users.\n")
    interactive_mode(db_handler, matchmaker)

def interactive_mode(db_handler: DatabaseHandler, matchmaker: Matchmaker):
    print("Available commands:")
    print("  add            -> Add a new user")
    print("  find <user_id> -> Find matches for a user")
    print("  list           -> Show all users")
    print("  quit           -> Exit the program")
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == 'quit':
                print("Goodbye! See you next time.")
                break
            
            elif command == 'list':
                users = db_handler.get_all_users()
                print(f"\nAll Users ({len(users)} total):")
                
                for user in users:
                    print(f"  {user.user_id}: {user.name} ({user.email})")
                    
                    if len(user.skills_offered) > 0:
                        skills_offered_text = ""
                        for i, skill in enumerate(user.skills_offered):
                            if i == 0:
                                skills_offered_text = skill
                            else:
                                skills_offered_text = skills_offered_text + ", " + skill
                        print(f"    Offers: {skills_offered_text}")
                    else:
                        print(f"    Offers: None")
                    
                    if len(user.skills_needed) > 0:
                        skills_needed_text = ""
                        for i, skill in enumerate(user.skills_needed):
                            if i == 0:
                                skills_needed_text = skill
                            else:
                                skills_needed_text = skills_needed_text + ", " + skill
                        print(f"    Needs: {skills_needed_text}")
                    else:
                        print(f"    Needs: None")
            
            elif command == 'add':
                name = input("Name: ").strip()
                email = input("Email: ").strip()
                offered = input("Skills offered (comma-separated): ").strip()
                
                skills_offered = []
                if offered:
                    offered_list = offered.split(',')
                    for skill in offered_list:
                        cleaned_skill = skill.strip()
                        if cleaned_skill:
                            skills_offered.append(cleaned_skill)
                
                needed = input("Skills needed (comma-separated): ").strip()
                
                skills_needed = []
                if needed:
                    needed_list = needed.split(',')
                    for skill in needed_list:
                        cleaned_skill = skill.strip()
                        if cleaned_skill:
                            skills_needed.append(cleaned_skill)
                
                try:
                    user = User(
                        name=name,
                        email=email,
                        skills_offered=skills_offered,
                        skills_needed=skills_needed
                    )
                    user_id = db_handler.add_user(user)
                    print(f"{name} added successfully with ID {user_id}")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif command.startswith('find '):
                try:
                    user_id = int(command.split()[1])
                    user = db_handler.get_user(user_id)
                    if not user:
                        print(f"User {user_id} not found.")
                        continue
                    
                    print(f"\nFinding matches for {user.name}...")
                    matches = matchmaker.find_matches(user_id)
                    if not matches:
                        print("  No matches found.")
                        continue
                    
                    for match_id, score in matches:
                        matched_user = db_handler.get_user(match_id)
                        print(f"  {matched_user.name} - Compatibility: {score:.2f}")
                        
                        details = matchmaker.get_match_details(user.user_id, match_id)
                        
                        if len(details['user1_can_learn']) > 0:
                            can_learn_text = ""
                            for i, skill in enumerate(details['user1_can_learn']):
                                if i == 0:
                                    can_learn_text = skill
                                else:
                                    can_learn_text = can_learn_text + ", " + skill
                            print(f"    Can learn: {can_learn_text}")
                        
                        if len(details['user2_can_learn']) > 0:
                            can_teach_text = ""
                            for i, skill in enumerate(details['user2_can_learn']):
                                if i == 0:
                                    can_teach_text = skill
                                else:
                                    can_teach_text = can_teach_text + ", " + skill
                            print(f"    Can teach: {can_teach_text}")
                        
                        if details['is_mutual_exchange']:
                            print("    Mutual skill exchange possible!")
                
                except (ValueError, IndexError):
                    print("Usage: find <user_id>")
            
            else:
                print("Unknown command. Try 'add', 'find <id>', 'list', or 'quit'.")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()