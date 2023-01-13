import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import optparse
import random


class Instagram:

    def driver_initialize(self):
        chrome_options = Options()
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--dns-prefetch-disable")
        chrome_options.add_argument('ignore-certificate-errors')
        chrome_options.add_argument('ignore-ssh-errors')
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(), options=chrome_options)
        driver.set_page_load_timeout(300)
        return driver

    def login_random_credential(self):
        credential = [{'email': 'kleontiou0@gmail.com', 'password': '?5@wuKTuj$s9?3T'},
                      {'email': 'kyrileontiou2@gmail.com',
                          'password': '?5@wuKTuj$s9?3T'},
                      {'email': 'kyrileontiou3@gmail.com',
                          'password': '?5@wuKTuj$s9?3T'},
                      {'email': 'kyrileontiou4@gmail.com', 'password': '?5@wuKTuj$s9?3T'}]
        user_agent = random.choice(credential)
        return user_agent

    def checking_channeltype(self):
        try:
            channel_type = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//article//h2'))
                )
            return 'Channel is Private'
        except:
            return 'Channel is working fine'

    def checking_page(self):
        try:
            channel_type = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//main//header//h2'))
                )
            return 'page Opened'
        except:
            return 'Sorry, this page is not available.'

    def login_profile(self, loginUrl, user_name, password):
        driver.get(loginUrl)
        driver.implicitly_wait(10)
        input_username_element = driver.find_element(
            By.XPATH, '//input[@name="username"]')
        input_username_element.send_keys(user_name)
        input_password_element = driver.find_element(
            By.XPATH, '//input[@name="password"]')
        input_password_element.send_keys(password)
        button_login_element = driver.find_element(
            By.XPATH, '//button[@type="submit"]')
        button_login_element.click()
        driver.implicitly_wait(20)

    def instagram_profile_url(self, profile_url, comment):
        comment_stat = ""
        driver.get(profile_url)
        driver.implicitly_wait(10)
        checkingPage = self.checking_page()
        if 'page Opened' in checkingPage:
            channelType = self.checking_channeltype()
            if 'Channel is Private' in channelType:
                return channelType
            else:
                titleName = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//main//header//h2'))
                )
                print(f'Profile Title Name: {titleName.text}')
                post_links = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH, '//main[@role="main"]//article//a')))
                count = 0
                for post in post_links:
                    post.click()
                    driver.implicitly_wait(30)
                    close = driver.find_element(
                        By.CSS_SELECTOR, '[aria-label="Close"]')
                    if (count == 0):
                        comment_stat = self.post_section(comment)
                        self.click_heart_icon()
                    elif (count <= 2):
                        self.click_heart_icon()
                    else:
                        close.click()
                        break
                    driver.implicitly_wait(30)
                    count = count + 1
                    close.click()
                return comment_stat
        else:
            return checkingPage
    
    def checking_searchbox(self):
        try:
            search_dialogue = driver.find_element(
            By.XPATH, '//div[@role="dialog"]')
            if search_dialogue:
                searchSvg = driver.find_element(
                    By.XPATH, '//*[@aria-label="Search"]'
                    )
                searchSvg.click()
        except:
            pass


    def instagram_search_user_name(self, user_name, comment):
        comment_stat = ""
        search_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Search']"))
        )
        search_button.click()
        search_bar = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Search input']"))
        )
        search_bar.send_keys(f"{user_name}")
        driver.implicitly_wait(5)
        action = ActionChains(driver)
        options = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='none']"))
        )
        option = driver.find_element(
            By.XPATH, "//div[@role='none']")
        action.move_to_element(option).perform()
        action.move_to_element(option).click().perform()
        time.sleep(7)
        self.checking_searchbox()
        profile_url = driver.current_url
        checkingPage = self.checking_page()
        if 'page Opened' in checkingPage:
            channelType = self.checking_channeltype()
            if 'Channel is Private' in channelType:
                return [channelType, profile_url]
            else:
                titleName = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//main//header//h2'))
                )
                print(f'Profile Title Name: {titleName.text}')
                post_links = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH, '//main[@role="main"]//article//a')))
                count = 0
                for post in post_links:
                    post.click()
                    driver.implicitly_wait(30)
                    close = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, '[aria-label="Close"]'))
                    )
                    if (count == 0):
                        comment_stat = self.post_section(comment)
                        self.click_heart_icon()
                    elif (count <= 2):
                        self.click_heart_icon()
                    else:
                        close.click()
                        break
                    driver.implicitly_wait(30)
                    count = count + 1
                    close.click()
                return [comment_stat, profile_url]
        else:
            return [checkingPage, profile_url]

    def post_section(self, comment):
        try:
            comment_section_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(@id,"mount")]//form/textarea'))
            )
            comment_section_element.click()
            driver.implicitly_wait(40)
            comment_element = driver.find_element(
                By.XPATH, '//div[contains(@id,"mount")]//form/textarea')
            comment_element.send_keys(comment)
            driver.implicitly_wait(10)
            post_comment_element = driver.find_element(
                By.XPATH, '//div[contains(@id,"mount")]//form//div[@role="button"]')
            post_comment_element.click()
            driver.implicitly_wait(30)
            return "Comment Added Successfully in post"
        except:
            return "Comment didn't added in post"

    def click_heart_icon(self):
        heart_icon_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@role="presentation"]//section/span[1]'))
        )
        heart_icon_element.click()
        driver.implicitly_wait(10)
        print("Click Heart icon Successfully in post")

    def message_section(self, message):
        try:
            message_button = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@role="button"][contains(text(),"Message")]'))
            )
            message_button.click()
            driver.implicitly_wait(40)
            message_element = driver.find_element(
                By.XPATH, '//textarea[@placeholder="Message..."]')
            message_element.send_keys(message)
            driver.implicitly_wait(10)
            send_button = driver.find_element(
                By.XPATH, '//button[contains(text(),"Send")]')
            send_button.click()
            driver.implicitly_wait(30)
            return "Message Sent Successfully"
        except:
            return "Message didn't Sent Successfully"


if __name__ == '__main__':
    instagram = Instagram()
    driver = instagram.driver_initialize()
    user_agent = instagram.login_random_credential()
    user_name = user_agent['email']
    password = user_agent['password']
    print(f'Logging in via {user_name}')
    url = 'https://www.instagram.com/login'
    instagram.login_profile(url, user_name, password)
    time.sleep(5)
    parser = optparse.OptionParser()
    parser.add_option("--path", "-p")
    options, args = parser.parse_args()
    type_Of_file = options.path
    output_dict = {}
    fail_out_dict = {}
    business_name = []
    user_profile_url = []
    instagram_url = []
    comment_sent = []
    message_sent = []
    comment_status = []
    message_status = []
    failed_business_name = []
    failed_user_profile_url = []
    failed_instagram_url = []
    failed_comment_sent = []
    failed_message_sent = []
    failed_comment_status = []
    failed_message_status = []

    if 'profileurl' in f'{type_Of_file}':
        profile_instagram_file = pd.read_csv(f'{type_Of_file}.csv')
        for num in range(len(profile_instagram_file['Instagram'].dropna())):
            if (num+1 % 20 == 0):
                driver.close()
                instagram.driver_initialize()
                user_agent = instagram.login_random_credential()
                user_name = user_agent['email']
                password = user_agent['password']
                instagram.login_profile(url, user_name, password)
                time.sleep(5)

            profile_url = profile_instagram_file['Instagram'][num]
            user_name = profile_instagram_file['BusinessName'][num]
            comment = f'Hey {user_name}, I will create free of charge amazing podcast clips for you. Check dms.'
            message = f'Hey {user_name}, I will create free of charge amazing podcast clips for you. Fair?'
            print(f'Username: {user_name}')
            comm_stat = instagram.instagram_profile_url(
                profile_url, comment)
            time.sleep(10)
            mess_stat = instagram.message_section(message)
            print(mess_stat)
            time.sleep(10)
            if "Message didn't Sent" in mess_stat or "Comment didn't added" in comm_stat:
                failed_business_name.append(user_name)
                failed_instagram_url.append(profile_url)
                failed_message_sent.append(message)
                failed_comment_sent.append(comment)
                failed_comment_status.append(comm_stat)
                failed_message_status.append(mess_stat)
                fail_out_dict['BusinessName'] = failed_business_name
                fail_out_dict['InstagramUrl'] = failed_instagram_url
                fail_out_dict['Message'] = failed_message_sent
                fail_out_dict['message_status'] = failed_message_status
                fail_out_dict['comment'] = failed_comment_sent
                fail_out_dict['comment_status'] = failed_comment_status
                df = pd.DataFrame(fail_out_dict)
                df.to_csv('Failed_message_Output.csv', index=False)
            else:
                business_name.append(user_name)
                instagram_url.append(profile_url)
                message_sent.append(message)
                comment_sent.append(comment)
                comment_status.append(comm_stat)
                message_status.append(mess_stat)
                output_dict['BusinessName'] = business_name
                output_dict['InstagramUrl'] = instagram_url
                output_dict['Message'] = message_sent
                output_dict['message_status'] = message_status
                output_dict['comment'] = comment_sent
                output_dict['comment_status'] = comment_status
                df = pd.DataFrame(output_dict)
                df.to_csv('Final_Output.csv', index=False)
                print('Data Saved')

    elif 'username' in f'{type_Of_file}':
        profile_instagram_file = pd.read_csv(f'{type_Of_file}.csv')
        for num in range(len(profile_instagram_file['Username'].dropna())):
            if (num+1 % 20 == 0):
                driver.close()
                driver_initialize()
                user_agent = instagram.login_random_credential()
                user_name = user_agent['email']
                password = user_agent['password']
                instagram.login_profile(url, user_name, password)
                time.sleep(5)

            full_name = profile_instagram_file['Fullname'][num]
            user_name = profile_instagram_file['Username'][num]
            comment = f'Hey {full_name}, I want to work for you for free as a short form video editor. Check dms.'
            message = f'Hey {full_name}, I want to work for you for free as a short form video editor.'
            print(f'Username: {full_name}')
            values = instagram.instagram_search_user_name(
                user_name, comment)
            comm_stat = values[0]
            profile_url = values[1].split('/?')[0]
            print(f'profile_url: {profile_url}')
            time.sleep(10)
            mess_stat = instagram.message_section(message)
            print(mess_stat)
            time.sleep(10)
            if "Message didn't Sent" in mess_stat or "Comment didn't added" in comm_stat:
                failed_business_name.append(user_name)
                failed_instagram_url.append(profile_url)
                failed_message_sent.append(message)
                failed_comment_sent.append(comment)
                failed_comment_status.append(comm_stat)
                failed_message_status.append(mess_stat)
                fail_out_dict['BusinessName'] = failed_business_name
                fail_out_dict['InstagramUrl'] = failed_instagram_url
                fail_out_dict['Message'] = failed_message_sent
                fail_out_dict['message_status'] = failed_message_status
                fail_out_dict['comment'] = failed_comment_sent
                fail_out_dict['comment_status'] = failed_comment_status
                df = pd.DataFrame(fail_out_dict)
                df.to_csv('Failed_message_Output.csv', index=False)
            else:
                business_name.append(user_name)
                instagram_url.append(profile_url)
                message_sent.append(message)
                comment_sent.append(comment)
                comment_status.append(comm_stat)
                message_status.append(mess_stat)
                output_dict['BusinessName'] = business_name
                output_dict['InstagramUrl'] = instagram_url
                output_dict['Message'] = message_sent
                output_dict['message_status'] = message_status
                output_dict['comment'] = comment_sent
                output_dict['comment_status'] = comment_status
                df = pd.DataFrame(output_dict)
                df.to_csv('Final_Output.csv', index=False)
                print('Data Saved')