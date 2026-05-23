from dataclasses import dataclass
from enum import Enum

class Sex(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class Interests(str, Enum):
    SPORTS = "Sports"
    READING = "Reading"
    MUSIC = "Music"

@dataclass
class Paticipant:
    user_name: str #first_name
    surname: str #last_name
    email_address: str #email
    sex_choice: Sex #gender
    phone_number: str #mobile
    birth_year: str #year_of_birth
    birth_month: str #month_of_birth
    birth_day: str #day_of_birth
    favorite_subject: str #subjects
    free_time: Interests #hobbies
    avatar_path: str #picture
    living_address: str #address
    region: str #state
    settlement: str #city