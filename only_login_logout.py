from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

import time

URL = "http://192.168.0.240/app/signin"
RESTART_INTERVAL = 100  # N회 단위 driver 재시작

def create_driver(): # driver 생성
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--auto-open-devtools-for-tabs")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)
    driver.execute_cdp_cmd("Network.enable", {})

    return driver

def login_logout_cycle(driver):
    wait = WebDriverWait(driver, 10)

    # ID Input 로드 될때까지 대기
    id_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//label[normalize-space()="ID"]/following::input[1]')
        )
    )
    id_input.clear()
    id_input.send_keys('a') # 테스트할 ID 입력

    # 비밀번호 Input 로드 될때까지 대기
    pw_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//label[normalize-space()="Password"]/following::input[1]')
        )
    )
    pw_input.clear()
    pw_input.send_keys('1') # 테스트할 비밀번호 입력

    # 로그인 버튼 로드 되기까지 대기
    login_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//p[normalize-space()='Log In']]")
        )
    )
    login_btn.click() # 로그인 버튼 클릭

    # Connected ID 팝업 → 종료 조건
    try:
        # 중복로그인 모달 탐지
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@role='dialog' and .//span[normalize-space()='Connected ID']]")
            )
        )
        print("Connected ID detected → test stop")
        return False # 테스트 종료
    except TimeoutException:
        pass

    # 로그아웃 버튼 로드 까지 대기
    logout_div = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//p[normalize-space()='Log Out']/ancestor::div[contains(@style, 'cursor')]")
        )
    )
    logout_div.click() # 로그 아웃

    # 로그아웃 확인용, ID 라벨 확인될때까지 대기
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//label[normalize-space()="ID"]')
        )
    )

    return True

def main():
    driver = create_driver()
    count = 0

    while True: #  자동화 시작
        try:
            print(f"cycle: {count}")
            result = login_logout_cycle(driver) # login logout 사이클 실행
            if not result:
                break

            count += 1 # 횟수 증가

            if count % RESTART_INTERVAL == 0: # 100회 미만일 경우 드라이버 초기화
                print("restart driver")
                driver.quit() 
                driver = create_driver()

        except WebDriverException as e: # 에러 발생시 예외 처
            print(f"WebDriver error → restart driver\n{e}")
            try:
                driver.quit()
            except Exception:
                pass
            driver = create_driver()

    driver.quit()

if __name__ == "__main__":
    main()
