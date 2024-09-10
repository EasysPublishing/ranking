import requests
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# HTTP 헤더 추가
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Selenium 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 헤드리스 모드
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")  # 화면 크기 설정
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 자동화 감지 방지
chrome_options.add_argument("--remote-debugging-port=9222")  # 디버깅 포트 설정

# GitHub Actions에서는 ChromeDriver를 자동으로 다운로드하여 사용
service = Service('/usr/bin/chromedriver')  # GitHub Actions에서 기본 경로

# Chrome WebDriver 실행
driver = webdriver.Chrome(service=service, options=chrome_options)

# Google Apps Script 웹 애플리케이션 URL
GAS_URL = "https://script.google.com/macros/s/AKfycbzWHJwgrT5sDStOE4lQ6r3kJYTl9chGGL1kAEKvXk7p8_z74Ww_G6F-yU_wMsne9EuC/exec"

# 책 정보 추출 함수 정의
import time

def extract_book_info(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'gd_name') or contains(@class, 'title')]"))
        )

        # 책 제목 추출 시도
        xpaths = [
            "//h2[@class='gd_name']",
            "//h1[@class='title']",
            "//div[contains(@class, 'book-title')]"
        ]

        book_title = None
        for xpath in xpaths:
            try:
                title_element = driver.find_element(By.XPATH, xpath)
                book_title = title_element.text
                break
            except:
                continue

        if not book_title:
            print(f"책 제목을 찾을 수 없습니다: {url}")
            save_debug_info(driver)  # 디버깅 정보 저장
            return None, None

        # 순위 요소 찾기
        try:
            rank_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@onclick, 'openUrl') and contains(text(), '위')]"))
            )
            category_rank = rank_element.text
        except:
            category_rank = "순위권 외"

        return book_title, category_rank

    except Exception as e:
        print(f"오류 발생 ({url}): {e}")
        save_debug_info(driver)  # 오류 발생 시 디버깅 정보 저장
        return None, None

def save_debug_info(driver):
    # 페이지 HTML 저장
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    
    # 스크린샷 저장
    driver.save_screenshot("screenshot.png")

# 모든 책 링크 목록
urls = [
    "https://www.yes24.com/Product/Goods/116777159",  # C언어 Express
    "https://www.yes24.com/Product/Goods/102485981",  # 난생처음 파이썬 프로그래밍
    "https://www.yes24.com/Product/Goods/129047020",  # 두근두근 C언어 with 챗GPT
    "https://www.yes24.com/Product/Goods/128928355",  # 명품 JAVA Programming
    "https://www.yes24.com/Product/Goods/109625396",  # 혼자 공부하는 파이썬
    "https://www.yes24.com/Product/Goods/96024871",   # 혼자 공부하는 머신러닝+딥러닝
    "https://www.yes24.com/Product/Goods/106404609",  # 데이터베이스 개론
    "https://www.yes24.com/Product/Goods/107005339",  # 명품 HTML5+CSS3+Javascript 웹 프로그래밍
    "https://www.yes24.com/Product/Goods/118982111",  # 혼자 공부하는 C 언어
    "https://www.yes24.com/Product/Goods/111378840",  # 혼자 공부하는 컴퓨터 구조+운영체제
    "https://www.yes24.com/Product/Goods/124625874",  # Android Studio를 활용한 안드로이드 프로그래밍
    "https://www.yes24.com/Product/Goods/116598806",  # 두근두근 파이썬
    "https://www.yes24.com/Product/Goods/101875856",  # 알기 쉬운 알고리즘
    "https://www.yes24.com/Product/Goods/69750539",   # C언어로 쉽게 풀어쓴 자료구조
    "https://www.yes24.com/Product/Goods/105420138",  # 명품 운영체제
    "https://www.yes24.com/Product/Goods/116977423",  # 쉽게 배우는 운영체제
    "https://www.yes24.com/Product/Goods/106009846",  # 컴퓨팅 사고력을 키우는 이산수학
    "https://www.yes24.com/Product/Goods/124326403",  # MySQL로 배우는 데이터베이스 개론과 실습
    "https://www.yes24.com/Product/Goods/117529483",  # SQL과 NoSQL 기반의 데이터베이스 입문
    "https://www.yes24.com/Product/Goods/110820505",  # 누구나 쉽게 배우는 인공지능 스타트
    "https://www.yes24.com/Product/Goods/127086641",  # 으뜸 파이썬
    "https://www.yes24.com/Product/Goods/59401348",   # 명품 C++ Programming
    "https://www.yes24.com/Product/Goods/105504683",  # C언어 for Beginner
    "https://www.yes24.com/Product/Goods/110374254",  # 쉽게 배우는 데이터 통신과 컴퓨터 네트워크
    "https://www.yes24.com/Product/Goods/102486182",  # C로 배우는 쉬운 자료구조
    "https://www.yes24.com/Product/Goods/78213148",   # 최신 컴퓨터 구조
    "https://www.yes24.com/Product/Goods/125830483",  # 혼자 공부하는 네트워크
    "https://www.yes24.com/Product/Goods/124425168",  # 쉽게 배우는 알고리즘
    "https://www.yes24.com/Product/Goods/119590391",  # 파이썬으로 쉽게 배우는 자료구조
    "https://www.yes24.com/Product/Goods/102486031",  # 정보 보안 개론
    "https://www.yes24.com/Product/Goods/4333686",    # 윤성우의 열혈 C 프로그래밍
    "https://www.yes24.com/Product/Goods/124009226",  # 처음 만나는 인공지능
    "https://www.yes24.com/Product/Goods/96547422",   # 난생처음 컴퓨팅 사고 with 파이썬
    "https://www.yes24.com/Product/Goods/61269276",   # 명품 JAVA Programming
    "https://www.yes24.com/Product/Goods/102487130",  # 쉽게 배우는 소프트웨어 공학
    "https://www.yes24.com/Product/Goods/128869338",  # 미라클 HTML5+CSS3+자바스크립트
    "https://www.yes24.com/Product/Goods/116038054",  # 시간순삭 파이썬
    "https://www.yes24.com/Product/Goods/110328996",  # C로 시작하는 컴퓨터 프로그래밍
    "https://www.yes24.com/Product/Goods/132215297",  # 명품 라즈베리파이
    "https://www.yes24.com/Product/Goods/124752226",  # 쉽게 배우는 C 자료구조
    "https://www.yes24.com/Product/Goods/119243079",  # 유니티 교과서
    "https://www.yes24.com/Product/Goods/116258760",  # 컴퓨터개론
    "https://www.yes24.com/Product/Goods/110241160",  # 새내기 파이썬
    "https://www.yes24.com/Product/Goods/107877754",  # Power JAVA
    "https://www.yes24.com/Product/Goods/116755317",  # 컴퓨터 비전과 딥러닝
    "https://www.yes24.com/Product/Goods/102830177",  # C 언어 콘서트
    "https://www.yes24.com/Product/Goods/102270283",  # 난생처음 인공지능 입문
    "https://www.yes24.com/Product/Goods/95784557",   # 파워 유저를 위한 파이썬 EXPRESS
    "https://www.yes24.com/Product/Goods/41729451",   # 알기 쉬운 정보보호개론
    "https://www.yes24.com/Product/Goods/29290543",   # 운영체제
    "https://www.yes24.com/Product/Goods/129049095",  # 딥러닝 EXPRESS
    "https://www.yes24.com/Product/Goods/124622361",  # 안드로이드 프로그래밍
    "https://www.yes24.com/Product/Goods/124396434",  # 어서와 파이썬은 처음이지!
    "https://www.yes24.com/Product/Goods/117813841",  # 인공지능
    "https://www.yes24.com/Product/Goods/118627695",  # 데이터베이스 설계 및 구축
    "https://www.yes24.com/Product/Goods/110440162",  # 우분투 리눅스
    "https://www.yes24.com/Product/Goods/3816661",    # 윤성우의 열혈 C++ 프로그래밍
    "https://www.yes24.com/Product/Goods/117095957",  # 메타버스 시대의 사물 인터넷(IoT)
    "https://www.yes24.com/Product/Goods/105673484",  # 파이썬 for Beginner
    "https://www.yes24.com/Product/Goods/56842559",   # 어서와 C++는 처음이지!
    "https://www.yes24.com/Product/Goods/124896747",  # 오렌지로 쉽게 배우는 머신러닝과 데이터 분석
    "https://www.yes24.com/Product/Goods/106400308",  # 쉽게 배우는 자료구조 with 파이썬
    "https://www.yes24.com/Product/Goods/105880982",  # 리눅스 시스템 원리와 실제
    "https://www.yes24.com/Product/Goods/104254138",  # 시스템 프로그래밍
    "https://www.yes24.com/Product/Goods/103342089",  # Perfect C
    "https://www.yes24.com/Product/Goods/102588961",  # 컴퓨터 구조와 원리 3.0
    "https://www.yes24.com/Product/Goods/97142842",   # 파이썬 자료구조와 알고리즘 for Beginner
    "https://www.yes24.com/Product/Goods/96969993"    # 파이썬으로 만드는 인공지능
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
        
    # 각 요청 사이에 2초 지연을 추가
    time.sleep(2)
    
# 드라이버 종료
driver.quit()
