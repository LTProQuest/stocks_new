import requests
from bs4 import BeautifulSoup

url = "https://www.glassdoor.co.uk/job-listing/JV.htm?jl=3600842212"


with requests.session() as s:
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    headers = {"user-agent" : USER_AGENT}
    r = s.get(url, headers=headers)
    plain_text = r.text
    soup = BeautifulSoup(plain_text)
    description = soup.find("div", {"id":"JobDescriptionContainer"})
    description = description.find("div").getText()
    print('description: ', description)

    
