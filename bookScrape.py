import base64
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

browser = webdriver.Chrome()


def barnesandnoble():
    url = "https://www.barnesandnoble.com/h/books/browse"
    browser.get(url)
    time.sleep(5)
    actions = ActionChains(browser)
    navigate_signbtn = browser.find_element_by_xpath("//a[@id='navbarDropdown']")
    actions.move_to_element(navigate_signbtn).perform()
    time.sleep(5)
    signin = browser.find_element_by_link_text("Sign In")
    signin.click()
    time.sleep(10)

    WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it(
        (By.XPATH, "//iframe[@title='Sign in or Create an Account']")))
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                "//a[@id='loginForgotPassword']"))).click()
    time.sleep(10)

    browser.switch_to.default_content()
    time.sleep(5)
    WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it(
        (By.XPATH, "//iframe[@title='Password Assistance']")))

    try:
        browser.find_element_by_xpath("//input[@id='email']").send_keys('abc@gmail.com')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                     "//aside[@id='passwordAssistantErr']")))
        message = browser.find_element_by_xpath("//em[@class='emphasis emphasis--alert']").text
        if message:
            print(message)
    except Exception as e :
        print(e)


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
def get_email():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credetials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    result = service.users().messages().list(userId='me', q="barnesandnoble@mail.barnesandnoble.com").execute()
    messages = result.get('messages')
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        try:
            payload = txt['payload']
            headers = payload['headers']

            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']

            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)

            soup = BeautifulSoup(decoded_data, "lxml")
            body = soup.body()
            print("Subject: ", subject)
            print("From: ", sender)
            print("Message: ", body)
        except Exception as e:
            print(e)


barnesandnoble()
