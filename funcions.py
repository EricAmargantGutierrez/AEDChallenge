from typing import List, Dict
from uuid import UUID
from collections import defaultdict
from typing import List, Tuple

#functions to make sure the data given is correctly organized

# three functions to handle data validation for your Participant class:

# This function checks whether all attributes of a Participant object are correctly set (not None or
# empty). It also ensures the data types are correct for each attribute.

def validate_participant_data(participant: Participant) -> bool:
    """
    Validates that all attributes of a Participant object are properly set and have the correct type.
    """
    try:
        # Validate basic fields
        assert isinstance(participant.id, uuid.UUID), "Invalid ID"
        assert isinstance(participant.name, str) and participant.name.strip(), "Name must be a non-empty string"
        assert isinstance(participant.email, str) and "@" in participant.email, "Invalid email address"
        assert isinstance(participant.age, int) and participant.age > 0, "Age must be a positive integer"
        assert participant.year_of_study in {"1st year", "2nd year", "3rd year", "4th year", "Masters", "PhD"}, \
            "Invalid year of study"
        assert participant.shirt_size in {"S", "M", "L", "XL"}, "Invalid shirt size"
        assert isinstance(participant.university, str) and participant.university.strip(), "University must be a string"
        assert participant.dietary_restrictions in {"None", "Vegetarian", "Vegan", "Gluten-free", "Other"}, \
            "Invalid dietary restriction"

        # Validate experience and skills
        assert isinstance(participant.programming_skills, dict), "Programming skills must be a dictionary"
        for skill, level in participant.programming_skills.items():
            assert isinstance(skill, str) and isinstance(level, int), "Each skill must be a string and level an integer"
        assert participant.experience_level in {"Beginner", "Intermediate", "Advanced"}, "Invalid experience level"
        assert isinstance(participant.hackathons_done, int) and participant.hackathons_done >= 0, \
            "Hackathons done must be a non-negative integer"

        # Validate interests and preferences
        assert isinstance(participant.interests, list) and all(isinstance(i, str) for i in participant.interests), \
            "Interests must be a list of strings"
        assert participant.preferred_role in {"Analysis", "Visualization", "Development", "Design", 
                                              "Don't know", "Don't care"}, "Invalid preferred role"
        assert isinstance(participant.objective, str) and participant.objective.strip(), "Objective must be a string"
        assert isinstance(participant.interest_in_challenges, list) and \
            all(isinstance(c, str) for c in participant.interest_in_challenges), "Challenges must be a list of strings"
        assert isinstance(participant.preferred_languages, list) and \
            all(isinstance(l, str) for l in participant.preferred_languages), "Languages must be a list of strings"
        assert isinstance(participant.friend_registration, list) and \
            all(isinstance(f, uuid.UUID) for f in participant.friend_registration), \
            "Friend registrations must be a list of UUIDs"
        assert isinstance(participant.preferred_team_size, int) and participant.preferred_team_size > 0, \
            "Team size must be a positive integer"
        assert isinstance(participant.availability, dict) and \
            all(isinstance(slot, str) and isinstance(available, bool) for slot, available in participant.availability.items()), \
            "Availability must be a dictionary with string keys and boolean values"

        # Validate description fields
        assert isinstance(participant.introduction, str), "Introduction must be a string"
        assert isinstance(participant.technical_project, str), "Technical project must be a string"
        assert isinstance(participant.future_excitement, str), "Future excitement must be a string"
        assert isinstance(participant.fun_fact, str), "Fun fact must be a string"

        return True  # If all assertions pass, the data is valid
    except AssertionError as e:
        print(f"Validation error for participant {participant.name}: {e}")
        return False

# This function ensures there are no duplicate participants in the list, based on their email or id.

def check_duplicate_participants(participants: List[Participant]) -> bool:
    """
    Checks if any participants have duplicate entries based on their email or ID.
    Returns True if no duplicates are found.
    """
    seen_emails = set()
    seen_ids = set()
    
    for participant in participants:
        if participant.email in seen_emails or participant.id in seen_ids:
            print(f"Duplicate participant found: {participant.name} ({participant.email})")
            return False
        seen_emails.add(participant.email)
        seen_ids.add(participant.id)
    
    return True

# his function ensures all participants' data is valid and there are no duplicates.

def validate_all_participants(participants: List[Participant]) -> bool:
    """
    Validates that all participants' data is correctly set and ensures no duplicates exist.
    """
    # Validate each participant's data
    for participant in participants:
        if not validate_participant_data(participant):
            print(f"Participant {participant.name} failed validation.")
            return False

    # Check for duplicates
    if not check_duplicate_participants(participants):
        print("Duplicate participants found.")
        return False

    return True  # All validations passed

def get_participants_without_group(participants: List[Participant]) -> List[Participant]:
    """
    Filters and returns a list of participants who do not belong to any group.

    Args:
        participants (List[Participant]): The list of all participants.

    Returns:
        List[Participant]: A list of participants without a group.
    """
    return [participant for participant in participants if participant.group is None]

# The function split_by_availability filters out participants who already belong to a group and
# focuses only on ungrouped participants. It evaluates their availability to determine if they 
# are free on Saturday, Sunday, or both days. Based on this, the function organizes them
# into three separate lists corresponding to their availability.
# Finally, it returns these lists, ensuring that ungrouped participants are categorized
#  by their availability for better team organization.

def split_by_availability(participants: List[Participant]) -> Tuple[List[Participant], List[Participant], List[Participant]]:
    """
    Filters participants without a group and splits them into three groups based on their availability:
    - Available only on Saturday
    - Available only on Sunday
    - Available on both Saturday and Sunday

    Returns:
        Tuple containing three lists: (saturday_only, sunday_only, both_days)
    """
    # Initialize lists for the three groups
    saturday_only = []
    sunday_only = []
    both_days = []

    for participant in participants:
        # Skip participants who already have a group
        if participant.assigned_group:  # Assuming `assigned_group` is a property indicating group status
            continue
        
        # Check availability
        available_saturday = participant.availability.get("Saturday", False)
        available_sunday = participant.availability.get("Sunday", False)
        
        if available_saturday and available_sunday:
            both_days.append(participant)
        elif available_saturday:
            saturday_only.append(participant)
        elif available_sunday:
            sunday_only.append(participant)

    return saturday_only, sunday_only, both_days

# Helper functions to compare attributes (useful to find shared patterns among 2 participants)
# The larger the integer is returned, the more similitudes both participants have

def check_role_and_objective_match(p1: Participant, p2: Participant) -> int:
    """
    Compares the role and objective between two participants.
    Instead of checking for an exact objective match, it finds the shared words between objectives.
    """
    score = 0
    
    # Compare objectives based on shared words
    p1_objective_words = set(p1.objective.lower().split())  # Convert to lowercase and split into words
    p2_objective_words = set(p2.objective.lower().split())  # Convert to lowercase and split into words
    shared_objective_words = p1_objective_words.intersection(p2_objective_words)  # Find shared words
    
    score += 10*len(shared_objective_words)  # Add the count of shared words to the score

    # Compare preferred roles
    if p1.preferred_role == p2.preferred_role:
        score += 10  # Role match
    
    return score

def compare_programming_skills(p1: Participant, p2: Participant) -> int:
    """
    Compares programming skills between two participants.
    Returns the number of skills they share.
    """
    return 3*(len(set(p1.programming_skills).intersection(p2.programming_skills)))

def compare_hackathon_experience(p1: Participant, p2: Participant) -> int:
    """
    Compares the number of hackathons two participants have done.
    Returns a score inversely proportional to the difference in experience.
    """
    hackathon_diff = abs(p1.hackathons_done - p2.hackathons_done)
    
    # Score decreases with larger differences
    if hackathon_diff == 0:
        return 3  # Perfect match
    elif hackathon_diff == 1:
        return 2  # Close match
    elif hackathon_diff == 2:
        return 1   # Somewhat close
    else:
        return 0   # No significant similarity

def is_available_in_same_slot(p1: Participant, p2: Participant) -> bool:
    """
    Checks if two participants are available in the same timeslot.
    """
    return any(p1.availability.get(slot, False) and p2.availability.get(slot, False) for slot in p1.availability)


#score_participant function considering all attributes
def score_participant(p1: Participant, p2: Participant) -> int:
    """
    Computes a compatibility score between two participants based on various factors.
    Now includes all attributes in the Participant class for a more comprehensive match.
    """
    score = 0
    
    # Matching Role and Objective
    score += check_role_and_objective_match(p1, p2)
    
    # Matching Interests and Challenges
    score += 3*(len(set(p1.interests).intersection(p2.interests)))  # Interest overlap
    score += 5*(len(set(p1.interest_in_challenges).intersection(p2.interest_in_challenges)))  # Interest in challenges overlap
    
    # Programming skills and Languages
    score += compare_programming_skills(p1, p2)  # Programming skill match
    score += 2+(len(set(p1.preferred_languages).intersection(p2.preferred_languages))) # Language overlap
    
    # Age and Year of Study
    age_diff = abs(p1.age - p2.age)
    if age_diff <= 2:  # Small age difference
        score += 2
    if p1.year_of_study == p2.year_of_study:
        score += 3  # Year of study match
    
    # Hackathon experience
    score += compare_hackathon_experience(p1, p2)  # Hackathon experience match
    
    # Team preferences
    if p1.preferred_team_size == p2.preferred_team_size:
        score += 1  # Preferred team size match

    # Availability match (timeslot overlap)
    score += sum(1 for slot in p1.availability if is_available_in_same_slot(p1, p2))  # Availability match
    
    # Additional personal attributes match
    if p1.university == p2.university:
        score += 2  # Same university match
    
    # Friend registration match (if they have friends in common)
    if any(friend in p2.friend_registration for friend in p1.friend_registration):
        score += 4  # Common friends
    
    # Experience level match
    if p1.experience_level == p2.experience_level:
        score += 3  # Experience level match
        
    return score

from collections import Counter

def most_frequent_topic(text):
    # Define keyword groups for each topic
    topics = {
        "prize-hunting": ["prize", "winning", "competition", "award", "victory", "reward", "contest"],
        "portfolio-building": ["portfolio", "project", "resume", "career", "work", "showcase", "development"],
        "learning new skills": ["learning", "skills", "knowledge", "training", "workshop", "growth", "improve"],
        "meeting new people": ["meeting", "networking", "people", "friends", "connections", "socializing", "community"]
    }
    
    # Normalize text (convert to lowercase)
    text = text.lower()
    
    # Count occurrences of keywords in the text
    keyword_counts = {topic: sum(text.count(word) for word in words) for topic, words in topics.items()}
    
    # Find the topic with the highest frequency
    most_frequent = max(keyword_counts, key=keyword_counts.get)
    
    return most_frequent, keyword_counts  # Return the most frequent topic and counts for reference
