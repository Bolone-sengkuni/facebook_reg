import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

from typing import Tuple

from exceptions import EmailAddress


@dataclass
class Message:
    sender: str
    title: str
    time: str
    text: str


class Mail:
    def __init__(self):
        self.base_url = 'https://10minutemail.net/'
        self._session = requests.Session()
        self._session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15'
            }
        self.email_address = None
    
    def _main_response(self):
        response = self._session.get(self.base_url)
        return BeautifulSoup(response.content, 'html.parser')
           
    def create(self) -> Tuple:
        soup = self._main_response()  
        if email_element := soup.find('input', id='fe_text'):
            self.email_address = email_element.get('value')
            return self.email_address, soup
        else:
            return EmailAddress
    
    def _ses_url(self, url: str):
        if not self.email_address:
            self.create()
        return self._session.get(url)    
    
    def _find_text(self, mail_line):
        mail_url = self.base_url + mail_line[0].find('a')['href']
        soup_mail = BeautifulSoup(self._ses_url(mail_url).content, 'html.parser')
        return soup_mail.find('div', class_='mailinhtml').text
        
    def get_mails(self):
        mails =[]
        _, soup = self.create()  
        
        lines = soup.find('table', id='maillist').find_all('tr')[1:]
        for line in lines:
            mail_line = line.find_all('td')
            
            mails.append(Message(mail_line[0].text, mail_line[1].text, 
                                 mail_line[2].text, self._find_text(mail_line)))
        
        return mails
    


# print(Mail().create())
# print(Mail().get_mails())