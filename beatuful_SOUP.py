from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


options = Options()
options.add_argument("--headless=new")  # 헤드리스 모드
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://m.sports.naver.com/kfootball/news")
time.sleep(2)  # JS 로딩 대기

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

ul = soup.select_one("ul.NewsList_news_list__juPdd")
#print(ul.get_text())
items = ul.select("li")

for item in items:
    title = item.get_text(strip=True)
    print(title)


'''
import requests
from bs4 import BeautifulSoup

url = 'https://m.sports.naver.com/kfootball/news'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.select_one('ul.NewsList_news_list__juPdd')
    print(ul)
else : 
    print(response.status_code)

'''
'''
import requests
from bs4 import BeautifulSoup

url = 'https://kin.naver.com/search/list.nhn?query=%ED%8C%8C%EC%9D%B4%EC%8D%AC'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('#s_content > div.section > ul > li:nth-child(1) > dl > dt > a') # css 선택
    print(title)
    # print(title.get_text()) 텍스트만 뽑아올떄
else : 
    print(response.status_code)
'''
