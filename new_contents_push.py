import telegram, requests, time
from bs4 import BeautifulSoup
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 텔레그램 봇(pororopororo_bot)의 토큰 및 ID 셋팅 - 파일에서 읽어옴
with open(os.path.join(BASE_DIR, 'resources/bot_token'), 'r') as f1 :
    my_token = f1.readline().strip()
    f1.close()

with open(os.path.join(BASE_DIR, 'resources/bot_chatid'), 'r') as f2 :
    chat_id = f2.readline().strip()
    f2.close()

bot = telegram.Bot(token = my_token)
url_prefix = 'https://www.ppomppu.co.kr/zboard/'
now = time.localtime()

req = requests.get('http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu')

# 뽐뿌게시판을 크롤링하고 tr 태그의 클래스명이 list0, list1 인 것들을 모두 찾음
html = req.text
soup = BeautifulSoup(html, 'html.parser')
posts = soup.find_all('tr',{'class':['list0','list1']})

latest_contents = []    # 뽐뿌게시판에서 크롤링한 최근 게시글
before_contents = []    # 뽐뿌게시판에서 직전에 크롤링한 게시글
send_message_list = []    # 최근 게시글에서 직전 게시글의 차집합을 저장하는 리스트
send_message = ''    # 텔레그램으로 전송할 메세지
write_message = ''   # 파일에 저장할 메세지

for i in range(1, 11) :
    latest_contents.append(posts[i].find('font').text + ' : ' + url_prefix + posts[i].find_all('a')[1]["href"])
    #latest_contents.append(url_prefix + posts[i].find_all('a')[1]["href"])

with open(os.path.join(BASE_DIR, 'latest.txt'), 'r') as f_read :
    for read_line in f_read :
        before_contents.append(read_line.strip())

    f_read.close()

latest_contents_set = set(latest_contents)
before_contents_set = set(before_contents)

final_set = latest_contents_set - before_contents_set
send_message_list = list(final_set)

if len(send_message_list) != 0 :
    for send_message in send_message_list :
        if (now.tm_hour >= 21 and now.tm_hour <= 23) :
            bot.sendMessage(chat_id=chat_id, text=send_message.strip(), disable_notification=True)
        else :
            bot.sendMessage(chat_id=chat_id, text=send_message.strip())

with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write :
    for i in latest_contents :
        write_message = write_message + i + '\n'

    f_write.write(write_message.strip())
    f_write.close()
