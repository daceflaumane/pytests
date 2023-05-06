from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pytest
import allure
import json
import os
import snoop
import time
import re


class RegistrationFlow:
    def __init__(self, browser):
        self.browser = browser
        # Texts
        self.reg_cont_a1 = os.path.join("flows", "reg_cont_a1.json")

        # Input data
        self.reg_inp_a1 = os.path.join("flows", "reg_inp_a1.json")


    def check_elements(self, elements):
        # Take a screenshot and attach it to the report
        allure.attach(
            self.browser.get_screenshot_as_png(),
            name="Screen",
            attachment_type=allure.attachment_type.PNG
        )
        
        errors = 0
        missing_txts = ""
        missing_cls = ""
        for element in elements:
            didn_find_cl = ""
            didn_find_txt = ""
            el_class = element['class']  # Get class name of element
            el_contents = element['value']  # Get expected value of element

            # input fields
            if re.match(".*-input", el_class): 
                actual_value_xpath = f"""
                    //input[contains(@class, "{el_class}")][contains(@placeholder, "{el_contents}")]
                """
                # //input[contains(@class, "{el_class}")][contains(@required, "")][contains(@placeholder, "{el_contents}")]

            # images
            elif re.match("img-*.", el_class):
                actual_value_xpath = f"""
                    //img[contains(@class, "{el_class}")][contains(@src, "{el_contents}")]
                """

            # texts and titles
            else:
                actual_value_xpath = f"""
                    //*[contains(@class, "{el_class}")][contains(normalize-space(), "{el_contents}")]
                """

            try:
                actual_value = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, actual_value_xpath)))
            except:
                if missing_txts == "":
                    missing_txts += f"{el_class}: {el_contents}"
                else:
                    missing_txts += f"; {el_class}: {el_contents}"
                errors += 1
                didn_find_txt += f"{el_class}: {el_contents}"
            

            if didn_find_txt == "":
                with allure.step(f"{el_class} contains: '{el_contents}'"):
                    assert True
            else:
                with allure.step(f"Couldnt locate: element {el_class}: {el_contents}'"):
                    allure.attach(actual_value_xpath, name="actual_value_xpath", attachment_type=allure.attachment_type.TEXT)
                    allure.attach(
                        self.browser.page_source, name="Page HTML", attachment_type=allure.attachment_type.HTML
                    )
                    assert False
            

        assert (errors == 0), f"""
            Couldnt locate: element - {el_class}: {el_contents}'
        """


    def test_javascript_errors(self):
        # execute some JavaScript that throws an error
        self.browser.execute_script("var a = 10; console.log(a);")
        # get the browser console logs
        logs = self.browser.get_log('browser')
        # check if there are any error logs
        error_logs = [log for log in logs if log['level'] == 'SEVERE']
        assert not error_logs, f"JavaScript errors found: {error_logs}"



    def click_button_for_next_step(self, button):
        btn_xpath = f'//*[contains(@class, "{button}")]'
        continue_button = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, btn_xpath)))
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


    def gender_page(self, flow, inputs):
        with allure.step("Element Checks"):
            with open(flow, 'r') as f:
                elements = json.load(f)
            
            self.check_elements(elements['gender'])

        with allure.step("Choose gender"):
            with open(inputs) as f:
                users = json.load(f)
            
            input_val = users['user_a1'][0]['gender']

            gender_path = f'//label[contains(normalize-space(), "{input_val}")]'
            test_user_gender = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, gender_path)))
            test_user_gender.click()

            ticked_path = f'//label[contains(normalize-space(), "{input_val}")]//span[@class="btn-icon show-check"]'
            chosen_gender = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, ticked_path)))

            if chosen_gender:
                with allure.step(f"Gender: '{input_val}'"):
                    assert True
            else:
                with allure.step(f"Couldnt select gender: {input_val}'"):
                    allure.attach(gender_path, name="gender_xpath_path", attachment_type=allure.attachment_type.TEXT)
                    allure.attach(
                        self.browser.page_source, name="Page HTML", attachment_type=allure.attachment_type.HTML
                    )
                    assert False

            # Take a screenshot and attach it to the report
            allure.attach(
                self.browser.get_screenshot_as_png(),
                name="Screen",
                attachment_type=allure.attachment_type.PNG
            )

            time.sleep(1)

    def age_page(self, flow, inputs):
        with allure.step("Element Checks"):
            with open(flow, 'r') as f:
                elements = json.load(f)
            
            self.check_elements(elements['age'])

        with allure.step("Input age"):
            with open(inputs) as f:
                users = json.load(f)
            
            input_val = users['user_a1'][0]['age']

            age_path = '//input[@id="age"]'
            test_user_age= WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, age_path)))
            test_user_age.send_keys(input_val)

            # Take a screenshot and attach it to the report
            allure.attach(
                self.browser.get_screenshot_as_png(),
                name="Screen",
                attachment_type=allure.attachment_type.PNG
            )

            time.sleep(1)

    def employment_page(self, flow, inputs):
        with allure.step("Element Checks"):
            with open(flow, 'r') as f:
                elements = json.load(f)
            
            self.check_elements(elements['employment'])

        with allure.step("Choose employment"):
            with open(inputs) as f:
                users = json.load(f)
            
            input_val = users['user_a1'][0]['employment']

            employment_path = f'//label[contains(normalize-space(), "{input_val}")]'
            test_user_employment = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, employment_path)))
            test_user_employment.click()

            ticked_path = f'//label[contains(normalize-space(), "{input_val}")]//span[@class="do-btn-icon"]'
            chosen_employment = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, ticked_path)))

            if chosen_employment:
                with allure.step(f"Employment: '{input_val}'"):
                    assert True
            else:
                with allure.step(f"Couldnt select employment: {input_val}'"):
                    allure.attach(employment_path, name="gender_xpath_path", attachment_type=allure.attachment_type.TEXT)
                    allure.attach(
                        self.browser.page_source, name="Page HTML", attachment_type=allure.attachment_type.HTML
                    )
                    assert False

            # Take a screenshot and attach it to the report
            allure.attach(
                self.browser.get_screenshot_as_png(),
                name="Screen",
                attachment_type=allure.attachment_type.PNG
            )

            time.sleep(1)


    def focus_page(self, flow, inputs):
        with allure.step("Element Checks"):
            with open(flow, 'r') as f:
                elements = json.load(f)
            
            self.check_elements(elements['focus'])

        with allure.step("Choose focus"):
            with open(inputs) as f:
                users = json.load(f)
            
            for focus_val in users['user_a1'][0]['focus']:
                focus_path = f'//*[contains(@class, "checkbox-wrapper")][contains(normalize-space(), "{focus_val}")]'

                focus_path = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, focus_path)))
                focus_path.click()

                ticked_path = f'//label[contains(normalize-space(), "{focus_val}")]//span[@class="do-btn-icon"]'
                chosen_focus = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, ticked_path)))

                if chosen_focus:
                    with allure.step(f"Focus: '{focus_val}'"):
                        assert True
                else:
                    with allure.step(f"Couldnt select focus: {focus_val}'"):
                        allure.attach(focus_path, name="focus_xpath_path", attachment_type=allure.attachment_type.TEXT)
                        allure.attach(
                            self.browser.page_source, name="Page HTML", attachment_type=allure.attachment_type.HTML
                        )
                        assert False

            # Take a screenshot and attach it to the report
            allure.attach(
                self.browser.get_screenshot_as_png(),
                name="Screen",
                attachment_type=allure.attachment_type.PNG
            )

            time.sleep(1)
            