from selenium import webdriver # 브라우저 제어
from selenium.webdriver.chrome.service import Service # 드라이버 관리
from webdriver_manager.chrome import ChromeDriverManager # 크롬 드라이버 관
from selenium.webdriver.common.by import By # 요소탐색
import time

def main():
    url = "https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/"
    '''
        driver = webdriver.Chrome("C:/path/to/chromedriver.exe")
        selenium 4에서는 이 방식 지원 안함
        문자열을 경로로 받으면 객체가 아닌 문자열을 처리해버림, capabilities 속성이 없어 에러
    '''
    
    service = Service(ChromeDriverManager().install()) # 반드시 service 객체 사
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    time.sleep(2) #프로세스 일시 정지
    login = driver.find_element(By.XPATH, '//*[@id="id"]').click()
    password=driver.find_element(By.XPATH, '//*[@id="pw"]').click()
    driver.find_element(By.XPATH, '//*[@id="id"]').send_keys('kkk')
    driver.find_element(By.XPATH, '//*[@id="pw"]').send_keys('kkk')

if __name__ == '__main__':
    main()
