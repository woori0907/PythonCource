# requests : 파이썬에서 요청을 만드는 패키지. 이걸 사용하면 html 정보를 가져올 수 있음.
import requests
# beautiful : html에서 정보를 추출하기 위한 패키지 
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_indeed_pages():
  result = requests.get(URL)

  #페이지 수를 알기 위해 bs4 사용. soup를 이용해서 데이터를 탐색하고 추출
  soup = BeautifulSoup(result.text, "html.parser")

  #indeed_soup에서 찾은 데이터에서 탐색하여 필요한 데이터만 추출. 여기서는 pagination 데이터만 가져옴
  pagination = soup.find("div", {"class":"pagination"})

  links = pagination.find_all('a')
  pages = []

  #각 링크에서 페이지 번호 추출하여 span 리스트에 추가. 리스트는 mutable. 즉, 변경 가능함.
  #요소 안에 string이 하나만 있으면 string메소드만 써도 알아서 찾아줌.
  #list[-1] : 마지막아이템부터 첫번째 아이템까지 슬라이싱
  for link in links[:-1]:
    pages.append(int(link.string))

  max_page = pages[-1]
  return max_page


def extract_indeed_jobs(last_page):
  for page in range(last_page):
    result = requests.get(f"{URL}&start={page*LIMIT}")
    #status_code : 페이지 요청이 정상적으로 잘 작동하는지 확인. 200이면 요청이 정상적으로 작동되었다는 의미.
    print(result.status_code)