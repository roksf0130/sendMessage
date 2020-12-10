import telegram, requests, os, time
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
URL_PREFIX = 'https://www.ppomppu.co.kr/zboard/'
CURR_TIME = time.localtime()

latest_contents = {}
send_contents = {}

# 텔레그램 봇의 TOKEN, CHAT_ID 정보 획득 Function
def getBaseInfo(val) :

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

# 메세지 전송을 위한 딕셔너리를 새로 생성
send_contents = latest_contents.copy()

# 직전 작업에서 크롤링한 게시글ID를 파일에서 read 함
# 파일에는 게시글ID가 저장되어 있으며 해당 ID 가 크롤링한 데이터에 있으면 삭제함
with open(os.path.join(BASE_DIR, 'resources/saved_contents'), 'r') as f_read :
    for content_id in f_read :
        if send_contents.get(content_id.strip()) != None :
            del send_contents[content_id.strip()]
    f_read.close()

# 전송할 메시지가 있으면 (최근 게시글에서 전송하지 않은 메세지가 있는 경우) 아래 로직 수행
if len(send_contents) != 0 :
    for send_message in send_contents.values() :
        # 21시에서 09시 사이에는 알림 없이 전송
        if CURR_TIME.tm_hour >= 21 or CURR_TIME.tm_hour <= 9 :
            bot.sendMessage(chat_id=my_chatid, text=send_message.strip(), disable_notification=True)
            #print(send_message)
        else :
            bot.sendMessage(chat_id=my_chatid, text=send_message.strip())
            #print(send_message)

# 가장 최근 게시글의 ID 를 파일에 write
with open(os.path.join(BASE_DIR, 'resources/saved_contents'), 'w+') as f_write :
    for write_message in latest_contents.keys() :
        f_write.write(write_message.strip() + '\n')
    f_write.close()
