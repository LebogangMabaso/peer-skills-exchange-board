from typing import List, Tuple, Dict
from src.models.user import User
from src.models.match import Match
from src.database.db_handler import DatabaseHandler

class Matchmaker:
    
    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler
    
    def calculate_compatibility_score(self, user1: User, user2: User) -> Tuple[float, List[str]]:
        if user1.user_id == user2.user_id:
            return 0.0, []

        user1_can_learn = []
        for skill_user1_needs in user1.skills_needed:
            for skill_user2_offers in user2.skills_offered:
                if skill_user1_needs == skill_user2_offers:
                    user1_can_learn.append(skill_user1_needs)
                    break
        
        user2_can_learn = []
        for skill_user2_needs in user2.skills_needed:
            for skill_user1_offers in user1.skills_offered:
                if skill_user2_needs == skill_user1_offers:
                    user2_can_learn.append(skill_user2_needs)
                    break

        all_matches = []
        for skill in user1_can_learn:
            all_matches.append(skill)
        for skill in user2_can_learn:
            if skill not in all_matches:
                all_matches.append(skill)
 
        base_score = len(user1_can_learn) + len(user2_can_learn)
        
        mutual_bonus = 0.0
        if len(user1_can_learn) > 0 and len(user2_can_learn) > 0:
            mutual_bonus = 2.0
        
        max_possible = len(user1.skills_needed) + len(user2.skills_needed)
        
        if max_possible == 0:
            return 0.0, all_matches
        
        raw_score = base_score + mutual_bonus
        normalized_score = raw_score / max_possible
        if normalized_score > 1.0:
            normalized_score = 1.0
        
        return normalized_score, all_matches
    
    def find_matches(self, user_id: int, min_score: float = 0.1) -> List[Tuple[int, float]]:
        target_user = self.db_handler.get_user(user_id)
        if not target_user:
            return []
        
        all_users = self.db_handler.get_all_users()
        matches = []
        
        for user in all_users:
            if user.user_id == user_id:
                continue
            
            score, matching_skills = self.calculate_compatibility_score(target_user, user)
            
            if score >= min_score:
                matches.append((user.user_id, score))

                match = Match(
                    user1_id=user_id,
                    user2_id=user.user_id,
                    compatibility_score=score,
                    matching_skills=matching_skills
                )
                self.db_handler.save_match(match)
        
        for i in range(len(matches)):
            for j in range(len(matches) - 1 - i):
                if matches[j][1] < matches[j + 1][1]:
                    temp = matches[j]
                    matches[j] = matches[j + 1]
                    matches[j + 1] = temp
        
        return matches
    
    def get_match_details(self, user1_id: int, user2_id: int) -> Dict:
        user1 = self.db_handler.get_user(user1_id)
        user2 = self.db_handler.get_user(user2_id)
        
        if not user1 or not user2:
            return {}
        
        score, matching_skills = self.calculate_compatibility_score(user1, user2)
        
        user1_can_learn = []
        for skill_user1_needs in user1.skills_needed:
            for skill_user2_offers in user2.skills_offered:
                if skill_user1_needs == skill_user2_offers:
                    user1_can_learn.append(skill_user1_needs)
                    break
        
        user2_can_learn = []
        for skill_user2_needs in user2.skills_needed:
            for skill_user1_offers in user1.skills_offered:
                if skill_user2_needs == skill_user1_offers:
                    user2_can_learn.append(skill_user2_needs)
                    break
        
        is_mutual_exchange = False
        if len(user1_can_learn) > 0 and len(user2_can_learn) > 0:
            is_mutual_exchange = True
        
        return {
            'user1': user1.to_dict(),
            'user2': user2.to_dict(),
            'compatibility_score': score,
            'user1_can_learn': user1_can_learn,
            'user2_can_learn': user2_can_learn,
            'all_matching_skills': matching_skills,
            'is_mutual_exchange': is_mutual_exchange
        }