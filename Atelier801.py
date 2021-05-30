import requests
from bs4 import BeautifulSoup

URL_BASE = 'https://atelier801.com/'


class Browser(object):

    def __init__(self):
        self.response = None
        self.current_page = None
        self.session = requests.Session()

    def headers(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        }
        return headers

    def send_request(self, method, url, **kwargs):
        response = self.session.request(method, url, **kwargs)
        if response.status_code == 200:
            return response

        return None


class Atelier(Browser):

    def __init__(self):
        super().__init__()
        self.token_name = None
        self.token_value = None
        self.headers = self.headers()

    def get_tokens(self, url):
        params = {
            "redirect": "https://atelier801.com/index"
        }
        self.response = self.send_request('GET', URL_BASE + url, params=params)
        if self.response:
            soup = BeautifulSoup(self.response.text, 'html.parser')
            tokens = soup.find_all(attrs={"type": "hidden"})
            self.token_name = tokens[1]['name']
            self.token_value = tokens[1]['value']
            self.current_page = self.response.url
            return True

        return False

    def auth(self, url, user, password, referer=None):
        self.headers['Referer'] = referer
        if not referer:
            self.headers['Referer'] = self.current_page

        data = {
            "rester_connecte": "on",
            "id": user,
            "pass": password,
            "redirect": "https://atelier801.com/index",
            self.token_name: self.token_value,
        }
        self.response = self.send_request('POST', URL_BASE + url, data=data, headers=self.headers)
        if self.response:
            if 'redirection' in self.response.json():
                return {"result": True, "message": "Successfuly login!!!"}
            return {"result": False, "message": self.response.json()["message"]}

        return {"result": False, "message": "Fail"}

    def get_page(self, url):
        self.response = self.send_request('GET', URL_BASE + url, headers=self.headers)
        if self.response:
            soup = BeautifulSoup(self.response.text, 'html.parser')
            return soup

        return None


if __name__ == '__main__':
    atelier = Atelier()
    atelier.get_tokens(url='login')
    authentication = atelier.auth('identification', 'wen#6475', 'LnxxqTkvJ5RzNG7fUD4S6Li8SFBTSgidA1DEwC7FvjQ=')
    if authentication["result"]:
        print(authentication["message"])
        page = atelier.get_page(url='index')
        print(page)
    else:
        print(authentication["message"])