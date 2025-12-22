from selenium import webdriver # 브라우저 제어
from selenium.webdriver.chrome.service import Service # 드라이버 관리
from webdriver_manager.chrome import ChromeDriverManager # 크롬 드라이버 관
from selenium.webdriver.common.by import By # 요소탐색
from selenium.webdriver.support.ui import WebDriverWait   # 명시적 대기(조건 충족까지 기다림)
from selenium.webdriver.support import expected_conditions as EC  # 대기 조건 모음 (클릭 가능, 표시 여부 등)
from selenium.common.exceptions import TimeoutException

import time

def main():

    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")

       
    url = "http://192.168.0.240/app/signin"
    
    service = Service(ChromeDriverManager().install()) # 반드시 service 객체 사
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    # 명시적 대기 객체 생성
    # -> React 앱은 렌더링 타이밍이 늦기 때문에 필
    wait = WebDriverWait(driver, 10)

    count = 0
    while True:
        print(count)
        count += 1
  
        id_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//label[normalize-space()="ID"]/following::input[1]')
            )
        )
        id_input.clear() # send_keys에 쌓임 방지를 위해 clear 추가
        id_input.send_keys('a')

        pw_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//label[normalize-space()="Password"]/following::input[1]')
            )
        )
        pw_input.clear()
        pw_input.send_keys('1') # send_keys에 쌓임 방지를 위해 clear 추가

        # 확인 버튼 클릭
        check = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//p[normalize-space()='Log In']]")
            )
        )
        check.click()

        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[@role='dialog' and .//span[normalize-space()='Connected ID']]"
                ))
            )
            print("Connected ID dialog detected → loop stop")
            break
        except TimeoutException:
            pass

        
        # 1️⃣ nav 태그가 DOM에 나타날 때까지 대기
        # - class, id 사용 안 함 (MUI 동적 클래스 때문)
        # - 태그 자체로 의미 있는 부모를 먼저 잡음
        nav = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "nav"))
        )

        # 2️⃣ nav 내부에서만 a 태그 탐색
        # - 전역 탐색 방지
        # - 다른 메뉴(nav, footer 등)와 충돌 방지
        links = nav.find_elements(By.CSS_SELECTOR, "ul li a")
      
        # 3 각 메뉴 클릭
        '''
        for i in range(len(links)):
            # 🔹 클릭 차단 오버레이 제거 대기
            wait.until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, 'div[data-block="true"]')
                )
            )
            # 🔴 여기서 다시 찾는다 (중요)
            nav = wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))
            links = nav.find_elements(By.CSS_SELECTOR, "ul li a")

            
            # 🔹 클릭 가능 + 클릭
            wait.until(EC.element_to_be_clickable(links[i]))
            links[i].click()
        '''

        for i in range(len(links)):
            # 오버레이 사라질 때까지 대기
            wait.until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, 'div[data-block="true"]')
                )
            )

            # stale 방지를 위해 nav / links 재탐색
            nav = wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))
            links = nav.find_elements(By.CSS_SELECTOR, "ul li a")

            # 바로 클릭
            links[i].click()

                
        logout_div = driver.find_element(
            By.XPATH,
            "//p[normalize-space()='Log Out']/ancestor::div[@style[contains(., 'cursor: pointer')]]"
        )

        logout = wait.until(EC.element_to_be_clickable(logout_div))
        logout.click()

        # 로그아웃 완료 확인 
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//label[normalize-space()="ID"]')
            )
        )
        

if __name__ == '__main__':
    main()
