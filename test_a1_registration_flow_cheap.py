import allure
from functions import RegistrationFlow

class TestRegistration:
    @allure.title("Registration flow A1 - Cheap")
    @allure.severity(allure.severity_level.NORMAL)
    def test_successful_registration(self, browser):
        registration_page = RegistrationFlow(browser)
        with allure.step("Open registration flow landing page"):
            registration_page.start_page(
                registration_page.reg_cont_a1, 
                "https://staging.adhdplanner.app/flow/a1"
            )
            with allure.step("Check for JavaScript errors"):
                registration_page.test_javascript_errors()

            with allure.step("Move to next page"):
                registration_page.click_button_for_next_step("plan-btn")

        
        with allure.step("Welcome page"):
            registration_page.welcome_page(
                registration_page.reg_cont_a1
            )
            with allure.step("Check for JavaScript errors"):
                registration_page.test_javascript_errors()

            with allure.step("Move to next page"):
                registration_page.click_button_for_next_step("hello-btn")
        
        with allure.step("Name page"):
            registration_page.name_page(
                registration_page.reg_cont_a1,
                registration_page.reg_inp_a1
            )
            
            with allure.step("Check for JavaScript errors"):
                registration_page.test_javascript_errors()

            with allure.step("Move to next page"):
                registration_page.click_button_for_next_step("name-btn")
