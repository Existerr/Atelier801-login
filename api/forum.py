from api.urls import INDEX_PAGE, IDENTIFICATION

from utils import regex, encrypt

import asyncio

name_value = regex(r'<input type="hidden" name="([a-z]{10})" value="(.*?)"')

class Forum:

    def __init__(self, client, _id=None, password=None):
        self.client = client
        self.id = _id
        self.password = password

        self.credentials = f"{_id}:{password}"

        self.negatives = ["ECHEC_AUTHENTIFICATION", "BANNIS"]

    async def fetch_login_tokens(self):
        while not (content := await self.client.request("GET", INDEX_PAGE, return_object=True)):
            await asyncio.sleep(1.0)

        if text_vars := name_value.search(content["text"]):
            return text_vars.group(1), text_vars.group(2), content["cookies"]

        return await self.fetch_login_tokens()
        
    async def login(self, username=None, password=None):
        self.client.cookie_jar.clear()

        name, value, cookies = await self.fetch_login_tokens()
        
        data = {
            "rester_connecte": "on",
            "id": username,
            "pass": encrypt(password),
            "redirect": "https://atelier801.com/index",
            name: value
        }

        content = await self.client.request("POST", IDENTIFICATION, data=data, headers={ "Referer": INDEX_PAGE }, cookies=cookies)
    
        if content.get("supprime"):
            return True
        elif content.get("resultat") in self.negatives:
            return False
        else:
            print(content.get("resultat"))
            return await self.login(username, password)
        

        
