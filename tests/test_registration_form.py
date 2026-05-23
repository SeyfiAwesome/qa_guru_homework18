import pytest
from selene.support.shared import browser
from pages.registration_page import PracticeFormPage
from data.users import Paticipant, Sex, Interests

class TestRegistrationSuite:
    @pytest.mark.parametrize("test_person", [
        {
            "firstname": "Иван",
            "lastname": "Петров",
            "email_addr": "ivan.petrov@test.ru",
            "gender_choice": Sex.MALE,
            "mobile_phone": "9998887766",
            "year": "1985",
            "month": "May",
            "day": "15",
            "subject_name": "Computer Science",
            "hobby_selection": Interests.MUSIC,
            "picture_file": "file.pdf",
            "home_address": "г. Москва, ул. Ленина, д. 10",
            "state_name": "Rajasthan",
            "city_name": "Jaipur"
        }
    ])
    def test_successful_form_submission(self, test_person):
        participant = Paticipant(
            user_name=test_person['firstname'],
            surname=test_person['lastname'],
            email_address=test_person["email_addr"],
            sex_choice=test_person["gender_choice"],
            phone_number=test_person["mobile_phone"],
            birth_year=test_person["year"],
            birth_month=test_person["month"],
            birth_day=test_person["day"],
            favorite_subject=test_person["subject_name"],
            free_time=test_person["hobby_selection"],
            avatar_path=test_person["picture_file"],
            living_address=test_person["home_address"],
            region=test_person["state_name"],
            settlement=test_person["city_name"]
        )
        registration_page = PracticeFormPage()
        registration_page.launch_form()
        registration_page.fill_application(participant)
        registration_page.check_registration_result(participant)


    def test_minimal_form_submissions(self):
        minimal_user = Paticipant(
            user_name="Анна",
            surname="Сидорова",
            email_address="anna@test.com",
            sex_choice=Sex.FEMALE,
            phone_number="1112223334",
            birth_year="1995",
            birth_month="December",
            birth_day="25",
            favorite_subject="English",
            free_time=Interests.READING,
            avatar_path="test_file.pdf",
            living_address="г. Санкт-Петербург, Невский пр., 25",
            region="Uttar Pradesh",
            settlement="Agra"
        )
        page = PracticeFormPage()
        page.launch_form()
        page.fill_application(minimal_user)
        page.check_registration_result(minimal_user)

