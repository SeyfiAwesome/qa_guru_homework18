import allure
from selene import have, command
from selene.support.shared import browser

import utils
from data.users import Paticipant


class PracticeFormPage:

    @allure.step("Запустить форму тестирования")
    def launch_form(self):
        browser.open('/automation-practice-form')
        ad_blocks = browser.all('[id^=google_ads][id$=container__]')
        ad_blocks.with_(timeout=10).wait_until(have.size_greater_than_or_equal(3))
        ad_blocks.perform(command.js.remove)

    @allure.step("Ввести имя")
    def input_firstname(self, value):
        browser.element('#firstName').type(value)

    @allure.step("Ввести фамилию")
    def input_lastname(self, value):
        browser.element('#lastName').type(value)

    @allure.step("Ввести почту")
    def input_email_field(self, value):
        browser.element('#userEmail').type(value)

    @allure.step("Указать пол")
    def set_sex_option(self, chosen_sex):
        mapping = {
            "Male": '[for="gender-radio-1"]',
            "Female": '[for="gender-radio-2"]',
            "Other": '[for="gender-radio-3"]'
        }
        browser.element(mapping[chosen_sex]).click()

    @allure.step("Ввести номер телефона")
    def set_phone(self, number):
        browser.element('#userNumber').type(number)

    @allure.step("Указать дату рождения")
    def set_birthdate(self, y, m, d):
        browser.element('#dateOfBirthInput').click()
        browser.element('.react-datepicker__month-select').type(m)
        browser.element('.react-datepicker__year-select').type(y)
        day_selector = f'.react-datepicker__day--0{d}:not(.react-datepicker__day--outside-month)'
        browser.element(day_selector).click()

    @allure.step("Выбрать академический предмет")
    def pick_subject(self, subject_name):
        browser.element('#subjectsInput').type(subject_name).press_enter()

    @allure.step("Выбрать хобби")
    def choose_hobby(self, hobby):
        hobby_map = {
            "Sports": "hobbies-checkbox-1",
            "Reading": "hobbies-checkbox-2",
            "Music": "hobbies-checkbox-3"
        }
        element_id = hobby_map.get(hobby)
        if element_id:
            # Прокручиваем к элементу
            browser.element(f'#{element_id}').perform(command.js.scroll_into_view)
            # Ждем небольшую паузу
            import time
            time.sleep(0.5)
            # Кликаем по связанному лейблу (более надежно)
            browser.element(f'[for="{element_id}"]').click()

    @allure.step("Загрузить изображение")
    def attach_picture(self, filename):
        browser.element('#uploadPicture').set_value(utils.get_file_path(filename))

    @allure.step("Ввести адресс проживания")
    def type_current_address(self, text):
        browser.element("#currentAddress").type(text)

    @allure.step("Выбрать регион (штат)")
    def select_region(self, region_name):
        browser.element('#state').perform(command.js.scroll_into_view)
        browser.element('#state').click()
        browser.all('[id^=react-select][id*=option]').element_by(
            have.exact_text(region_name)
        ).click()

    @allure.step("Выбрать населенный пункт")
    def select_city(self, city_name):
        browser.element('#city').click()
        browser.all('[id^=react-select][id*=option]').element_by(
            have.exact_text(city_name)
        ).click()

    @allure.step("Отправить анкету")
    def press_submit_btn(self):
        browser.element("#submit").click()

    @allure.step("Комплексное заполнение анкеты")
    def fill_application(self, participant: Paticipant):
        self.input_firstname(participant.user_name)
        self.input_lastname(participant.surname)
        self.input_email_field(participant.email_address)
        self.set_sex_option(participant.sex_choice.value)
        self.set_phone(participant.phone_number)
        self.set_birthdate(participant.birth_year, participant.birth_month, participant.birth_day)
        self.pick_subject(participant.favorite_subject)

        # Обработка хобби с паузой
        import time
        time.sleep(0.5)
        self.choose_hobby(participant.free_time.value)

        self.attach_picture(participant.avatar_path)
        self.type_current_address(participant.living_address)
        self.select_region(participant.region)
        self.select_city(participant.settlement)
        self.press_submit_btn()

    @allure.step("Валидация заполненных данных")
    def check_registration_result(self, participant: Paticipant):
        excpected_data = [
            participant.user_name + " " + participant.surname,
            participant.email_address,
            participant.sex_choice.value,
            participant.phone_number,
            utils.modify_date_format(participant.birth_year, participant.birth_month, participant.birth_day),
            participant.favorite_subject,
            participant.free_time.value,
            participant.avatar_path,
            participant.living_address,
            participant.region + " " + participant.settlement
        ]
        browser.element('.table').all('td').even.should(have.exact_texts(excpected_data))
