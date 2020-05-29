
import time
from random import randint

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import Select

import pickle


class driver:
    scrape_attempts = 0
    errror_message = ""
    payload = []
    instance = None
    session_id = None

    def __init__(self, remote_url=None,headless=False, options = webdriver.ChromeOptions(), debug_mode=False):
       self.remote_url = remote_url
       self.headless = headless
       self.options = options
       self.debug_mode = debug_mode

    def get_instance(self):        
        global instance
        global session_id
        if self.headless == True:
            self.options.addArguments("headless")
        else:
            self.options.add_argument("--start-maximized")

        if self.remote_url == None:
            instance = webdriver.Chrome(chrome_options=self.options)
        else:
            instance = webdriver.Remote(command_executor=self.remote_url,desired_capabilities={})

        session_id = instance.session_id
        instance.implicitly_wait(15)
        return instance 

    def get_current_url(self):
        return instance.current_url

    def get_url(self, url):
        instance.get(url)
        self.remote_url = instance.command_executor._url       

    def sleep(self):
        time.sleep(randint(2, 5))

    def quit_session(self):
        instance.close()
        instance.quit()

    def login(self, login_credentials, user_element_finder, pw_element_finder):  # list type and text correspodingly (strings)
        if self.debug_mode == True:
            print("Attempting to login")
        user_element_type, user_element_text = user_element_finder[0], user_element_finder[1]
        pw_element_type, pw_element_text = pw_element_finder[0], pw_element_finder[1]
        if user_element_type == "id":
            userElem = instance.find_element_by_id(user_element_text).send_keys(login_credentials[0])
        self.sleep()
        if pw_element_type == "id":
            passwordElem = instance.find_element_by_id(pw_element_text).send_keys(login_credentials[1])
        self.sleep() 
        submitElem = instance.find_element_by_id("submit").click()

    def select_drop_down(self, id_name, visible_text):
        select = Select(instance.find_element_by_id(id_name))
        select.select_by_visible_text(visible_text)

    def cookies_add_to_driver(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                instance.add_cookie(cookie)
        except:
            print("No cookie file found for previous, continuing...")        

    def cookies_save(self):
        pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
