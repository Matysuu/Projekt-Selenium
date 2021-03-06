from faker import Faker
from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

LOCALE = 'pl_PL'
PASSWORDS = "asdkhjf1/"
ERRORE = "Wprowadzono niepoprawny adres e-mail"
class EObuwie(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get("https://www.eobuwie.com.pl/")
        self.fake = Faker(LOCALE)

    def tearDown(self):
        self.driver.quit()

    def testinvalidEmail(self):
        driver = self.driver
        fake = self.fake
        wait = WebDriverWait(driver, 15)
        # 1. Akceptacja plików cookie
        close_cookie_modal = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//button[@data-testid="permission-popup-accept"]')))
        close_cookie_modal.click()
        # 2. Kliknij ZAREJESTRUJ
        driver.find_element_by_xpath('//a[@data-testid="header-register-link"]').click()
        # 3. Wpisz imię
        name_field = driver.find_element_by_id('firstname')
        name_field.send_keys(fake.first_name())
        # 4. Wpisz nazwisko
        last_name = driver.find_element_by_id('lastname')
        last_name.send_keys(fake.last_name())
        # 5. Wpisz adres email
        invalid_email = driver.find_element_by_id('email_address')
        invalid_email.send_keys(fake.email().replace("@", ""))
        # 6. Wpisz hasło
        password = driver.find_element_by_id('password')
        password.send_keys(PASSWORDS)
        # 7. Potwierdź hasło
        password = driver.find_element_by_id('confirmation')
        password.send_keys(PASSWORDS)
        # 8. Zaznacz oświadczenie
        state = driver.find_element_by_xpath('//label[@class="checkbox-wrapper__label"]')
        state.click()
        # 9. Kliknij załóż nowe konto
        new_account = driver.find_element_by_id('create-account')
        new_account.click()
        # 10. Test rzeczywisty
        error = driver.find_element_by_xpath('//span[@class="help-block form-error"]')
        error_ver = error.text
        self.assertEqual(error_ver, ERRORE)

