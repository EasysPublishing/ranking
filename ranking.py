import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Selenium 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 헤드리스 모드로 실행 (GUI 없이)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # GPU 사용 안 함 (리소스 절약)
chrome_options.add_argument("--log-level=3")

# GitHub Actions에서는 ChromeDriver를 자동으로 다운로드하여 사용
service = Service('/usr/bin/chromedriver')  # GitHub Actions에서 기본 경로

# Chrome WebDriver 실행
driver = webdriver.Chrome(service=service, options=chrome_options)

# Google Apps Script 웹 애플리케이션 URL
GAS_URL = "https://script.google.com/macros/s/AKfycbzWHJwgrT5sDStOE4lQ6r3kJYTl9chGGL1kAEKvXk7p8_z74Ww_G6F-yU_wMsne9EuC/exec"

# 책 정보 추출 함수 정의
def extract_book_info(url):
    try:
        # 웹 페이지 로드
        driver.get(url)

        # 페이지 로드 대기
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//h2[@class='gd_name']"))
        )

        # 책 제목을 포함하는 요소 로드
        title_element = driver.find_element(By.XPATH, "//h2[@class='gd_name']")
        book_title = title_element.text

        # 'onclick' 속성을 사용하여 정확한 순위 요소를 선택
        try:
            rank_element = driver.find_element(By.XPATH, "//a[contains(@onclick, 'openUrl') and contains(text(), '위')]")
            category_rank = rank_element.text
        except:
            # 순위를 찾을 수 없는 경우 "순위권 외"로 설정
            category_rank = "순위권 외"

        return book_title, category_rank

    except Exception as e:
        print(f"오류 발생 ({url}): {e}")
        return None, None

# 모든 책 링크 목록
urls = [
    "https://www.yes24.com/Product/Goods/116777159",  # C언어 Express
    "https://www.yes24.com/Product/Goods/102485981",  # 난생처음 파이썬 프로그래밍
    # 추가 링크 ...
]

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")

# 각 책의 정보 추출 및 Google Sheets에 추가
for url in urls:
    title, rank = extract_book_info(url)
    if title and rank:
        # Google Apps Script에 데이터 전송
        response = requests.post(GAS_URL, json={"title": title, "rank": rank, "date": current_date})
        print(response.text)  # 응답 확인
    else:
        print(f"{url}에서 책 정보를 찾을 수 없습니다.")

# 드라이버 종료
driver.quit()
