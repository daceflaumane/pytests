from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import json
import os
import snoop
import time


class RegistrationFlow:
    def __init__(self, browser):
        self.browser = browser
        # Texts
        self.reg_cont_a1 = os.path.join("flows", "reg_cont_a1.json")

        # Input data
        self.reg_inp_a1 = os.path.join("flows", "reg_inp_a1.json")


    def check_elements(self, elements):
        check_status = True
        for element in elements:
            el_class = element['class']
            el_contents = element['value']
            try:
                actual_element = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, el_class)))
                actual_element.is_displayed()
                actual_value_xpath = f"""
                    //*[contains(@class, "{el_class}")][contains(normalize-space(), "{el_contents}")]
                    | //img[contains(@class, "{el_class}")][contains(@src, "{el_contents}")]
                    | //*[contains(@class, "{el_class}")][contains(@required, "")][contains(@placeholder, "{el_contents}")]
                """
                actual_value = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, actual_value_xpath)))
                assert actual_value.is_displayed()
            except AssertionError:
                allure.attach(
                    self.browser.get_screenshot_as_png(),
                    name=f"{el_class}_{el_contents}_failed_check",
                    attachment_type=allure.attachment_type.PNG
                )
                with allure.step(f"Element check failed for element {el_class} with value {el_contents}"):
                    allure.attach(
                        self.browser.get_screenshot_as_png(),
                        name=f"{el_class}_{el_contents}_failed_check",
                        attachment_type=allure.attachment_type.PNG
                    )
                    allure.attach(actual_value_xpath, name="actual_value_xpath", attachment_type=allure.attachment_type.TEXT)
                    check_status = False
            finally:
                with allure.step(f"Element check status for element {el_class} with value {el_contents}"):
                    allure.attach(actual_value_xpath, name="actual_value_xpath", attachment_type=allure.attachment_type.TEXT)
                    if check_status:
                        allure.attach("Element check passed", name="check_status", attachment_type=allure.attachment_type.TEXT)
                    else:
                        allure.attach("Element check failed", name="check_status", attachment_type=allure.attachment_type.TEXT)
                check_status = True if check_status else False

        # Add a try-except block around the entire for loop to handle failures
        try:
            assert check_status, "Content check failed for one or more elements"
        except AssertionError:
            with allure.step("Element checks failed"):
                allure.attach(
                    self.browser.get_screenshot_as_png(),
                    name="element_checks_failed",
                    attachment_type=allure.attachment_type.PNG
                )
            pytest.fail("Content check failed for one or more elements")

        # Take a screenshot and attach it to the report
        allure.attach(
            self.browser.get_screenshot_as_png(),
            name="Screen",
            attachment_type=allure.attachment_type.PNG
        )


    def test_javascript_errors(self):
        # execute some JavaScript that throws an error
        self.browser.execute_script("var a = 10; console.log(a);")
        # get the browser console logs
        logs = self.browser.get_log('browser')
        # check if there are any error logs
        error_logs = [log for log in logs if log['level'] == 'SEVERE']
        assert not error_logs, f"JavaScript errors found: {error_logs}"



    def click_button_for_next_step(self, button):
        continue_button = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, button)))
        continue_button.click()



# Pages
    def start_page(self, flow, url):
        self.browser.get(url)
        with allure.step("Element Checks"):
            with open(flow, 'r') as f:
                elements = json.load(f)
            
            self.check_elements(elements['start'])

    
    def welcome_page(self, flow):
        with allure.step("Element Checks"):
            with open(flow, 'r') as f:
                elements = json.load(f)
            
            self.check_elements(elements['welcome'])

    @snoop
    def name_page(self, flow, inputs):
        with allure.step("Element Checks"):
            with open(flow, 'r') as f:
                elements = json.load(f)
            
            self.check_elements(elements['name'])

        with allure.step("Input name"):
            with open(inputs) as f:
                users = json.load(f)
            
            input_val = users['user_a1'][0]['name']

            name_field = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "name-input")))
            name_field.send_keys(input_val)
            time.sleep(1)
            