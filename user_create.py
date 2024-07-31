from names_generator import generate_name
from playwright.sync_api import sync_playwright, Playwright, Page

from fake_useragent import UserAgent
import random
import time
from typing import List, Optional

from data import RegisterData
from generate import generate_password
from ten_mmail import Mail


def full_name() -> List[str]:
    return generate_name(style='capital').split(' ')


def _cookies_agree(page: Page):
    page.click('span[class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"]')
    time.sleep(1)
    page.click('div[class="x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x6s0dn4 xzolkzo x12go9s9 x1rnf11y xprq8jg x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xl56j7k xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xc9qbxq x14qfxbe x1qhmfi1"]')
    time.sleep(1)
    page.click('span[class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"]')
    time.sleep(1)
    page.click('div[class="x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x6s0dn4 xzolkzo x12go9s9 x1rnf11y xprq8jg x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xl56j7k xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xc9qbxq x14qfxbe x1qhmfi1"]')
    time.sleep(1)
    page.click('span[class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"]')
    time.sleep(20)
    

def create_user(page: Page, full_name_lst: List[str], 
                password: str, session: Mail) -> RegisterData:
    email, _ = session.create()
    print(f'email - {email}')
    print(f'password - {password}')
    
    create_button = page.query_selector('a[role="button"][class="_42ft _4jy0 _6lti _4jy6 _4jy2 selected _51sy"]')
    create_button.click()

    _input_name(page, full_name_lst)
    time.sleep(2)
    
    _email_password(page, email, password)
    time.sleep(3)
    
    _date_of_birth(page)
    _select_sex(page)
    time.sleep(1)
    # page.click('div[class="registration_redesign"]')
    
    page.query_selector('button[name="websubmit"]').click()
    time.sleep(15)
    
    # page.wait_for_selector('input[name="code"]')
    
    mails = session.get_mails()
    print(f'mails - {mails}')
    while len(mails) < 2:
        time.sleep(5)
        mails = session.get_mails()
        print(f'len mails - {len(mails)}')
        print(f'mails - {mails}')
        # print(f"mail find - {mails[0].title.split(' ')[0].split('-')[1]}")
    
    # _check_error(page)
    time.sleep(20)
    page.fill('input[name="code"]', mails[0].title.split(' ')[0].split('-')[1])
    page.click('button[name="confirm"]')
    RegisterData(full_name_lst[0], full_name_lst[1], email, password)
    
    return RegisterData 


def _input_name(page: Page, full_name_lst: List[str]):
    page.fill('input[name="firstname"]', full_name_lst[0])
    time.sleep(0.5)
    page.fill('input[name="lastname"]', full_name_lst[1])
    time.sleep(0.7)


def _email_password(page: Page, email: str, password: str):
    page.fill('input[name="reg_email__"]', email)
    time.sleep(0.6)
    page.click('div[class="registration_redesign"]')
    time.sleep(0.4)
    page.fill('input[name="reg_email_confirmation__"]', email)
    page.fill('input[name="reg_passwd__"]', password)


def _date_of_birth(page: Page):
    page.select_option('select[name="birthday_day"]', 
                       value=f'{random.choice([i for i in range(1, 29)])}')
    page.select_option('select[name="birthday_month"]', 
                       value=f'{random.choice([i for i in range(1, 13)])}')
    page.select_option('select[name="birthday_year"]', 
                       value=f'{random.choice([i for i in range(1962, 2004)])}')


def _select_sex(page: Page):
    random_value = random.choice(["1", "2"])
    print(f'random value - {random_value}')
    
    page.evaluate('''
        (value) => {
        const radio = document.querySelector('input[class="_8esa"][value="' + value + '"]');
        if (radio) {
            radio.click();
        } else {
            const otherRadio = document.querySelector('input[class="_8esa"][value="2"]');
            if (otherRadio) {
            otherRadio.click();
            } else {
            console.warn('Radio buttons with class "_8esa" and values "' + value + '" or "2" not found.');
            }
        }
        }
    ''', random_value)


def _check_error(page: Page):
    error = page.query_selector('div[id="reg_error_inner"]')
    if error:
        start_browser_mail()


def start_browser_mail(ua: UserAgent):
    full_name_lst = full_name()
    password = generate_password(length=18)
    session = Mail()
    start_url = 'https://www.facebook.com'
    
    with sync_playwright() as playwright:
        chrome = playwright.chromium
        browser = chrome.launch(headless=False, timeout=100000)
        page = browser.new_page(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15')
        page.goto(start_url)
        print(create_user(page, full_name_lst, password, session))
        browser.close() 
    

def main():
    ua = UserAgent()
    start_browser_mail(ua)  
        
if __name__ == '__main__':
    main()        