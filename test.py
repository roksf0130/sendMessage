import telegram, requests, os, time
from bs4 import BeautifulSoup

URL_PREFIX = 'https://www.ppomppu.co.kr/zboard/'
CURR_TIME = time.localtime()

latest_contents = {}
before_contents = {}

# 텔레그램 봇의 TOKEN, CHAT_ID 정보 획득 Function
def getBaseInfo(val) :
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # 전달받은 값이 1이면 TOKNE, 2이면 CHATID 리턴
    if val == '1' :
        temp = 'resources/token'
    else :
        temp = 'resources/chatid'
    
    with open(os.path.join(BASE_DIR, temp), 'r') as f :
        ret_val = f.readline().strip()
    f.close()

    return ret_val

# 텔레그램 봇 정보 획득
my_token = getBaseInfo('1')   # 토큰
my_chatid = getBaseInfo('2')  # CHATID

bot = telegram.Bot(token = my_token)

# 뽐뿌 게시판 크롤링
req = requests.get('http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu')

# 크롤링 결과 중 tr 태그의 클래스명이 list0, list1 인 것들을 모두 찾음
html = req.text
soup = BeautifulSoup(html, 'html.parser')
posts = soup.find_all('tr',{'class':['list0','list1']})

for i in range(0, 10) :
    # 게시글ID 와 게시글 제목으로 딕셔너리 생성
    link_str = posts[i].find_all('a')[1]["href"]   # 게시글 하이퍼링크 추출
    # 딕셔너리 키 : 하이퍼링크에서 추출한 게시글ID
    # 딕셔너리 값 : 게시글 제목 + ' : ' + 하이퍼링크
    latest_contents[link_str[link_str.rfind('=')+1:]] = posts[i].find('font').text + ' : ' + URL_PREFIX + link_str




#for i in range(1, 11) :
#    latest_contents.append(posts[i].find('font').text + ' : ' + url_prefix + posts[i].find_all('a')[1]["href"])
    #latest_contents.append(url_prefix + posts[i].find_all('a')[1]["href"])


