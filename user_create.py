from names_generator import generate_name
from playwright.sync_api import sync_playwright, Playwright
import time

import random
from typing import List

from ten_mmail import Mail


def full_name() -> List[str]:
    return generate_name(style='capital').split(' ')


def create_user(page: Playwright.Response, full_name_lst: List[str], session: Mail):
    email, _ = session.create()
    mails = session.get_mails()
    
    create_button = page.query_selector('a[role="button"][data-testid="open-registration-form-button"]')
    create_button.click()

    page.fill('input[name="firstname"]', full_name_lst[0], timeout=500)
    page.fill('input[name="lastname"]', full_name_lst[1], timeout=500)
    
    page.fill('input[name="reg_email__"]', email, timeout=500)
    page.click('div[class="registration_redesign"]', timeout=100)
    page.fill('input[name="reg_email_confirmation__"]', email, timeout=300)
    page.fill('input[name="reg_passwd__"]', 'ybt@agr.com', timeout=200)
    
    page.select_option('select[name="birthday_day"]', 
                       value=f'{random.choice([i for i in range(1, 29)])}')
    page.select_option('select[name="birthday_month"]', 
                       value=f'{random.choice([i for i in range(1, 13)])}')
    page.select_option('select[name="birthday_year"]', 
                       value=f'{random.choice([i for i in range(1962, 2004)])}')
    
    random_value = random.choice(["-1", "1", "2"])
    page.evaluate('''
    (value) => {
        const radio = document.querySelector('input[name="sex"][value="$value"]');
        if (radio) radio.click();
    }
    ''', random_value)
    page.click('button[type="submit"]')
    time.sleep(2)
    
    page.fill('input[name="code"]', mails[0].title.split(' ')[0].split('-')[1])
    page.click('button[type="submit"]')
    

def main():
    full_name_lst = full_name()
    session = Mail()
    start_url = 'https://www.facebook.com'
    
    with sync_playwright() as playwright:
        chrome = playwright.chromium
        browser = chrome.launch(headless=False)
        page = browser.new_page()
        fb_reg = page.goto(start_url)
        page.fill()
        create_user(fb_reg, full_name_lst, session)    