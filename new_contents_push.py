import telegram, requests, os, time
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
URL_PREFIX = 'https://www.ppomppu.co.kr/zboard/'
CURR_TIME = time.localtime()

latest_contents = {}
send_contents = {}

def getBaseInfo(val) :

    if val == '1' :
        temp = 'resources/token'
    else :
        temp = 'resources/chatid'
    
    with open(os.path.join(BASE_DIR, temp), 'r') as f :
        ret_val = f.readline().strip()
        f.close()

    return ret_val

my_token = getBaseInfo('1')
my_chatid = getBaseInfo('2')

bot = telegram.Bot(token = my_token)

req = requests.get('https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu')

html = req.text
soup = BeautifulSoup(html, 'html.parser')
posts = soup.find_all('tr',{'class':['list0','list1']})

for i in range(0, 15) :
    link_str = posts[i].find_all('a')[1]["href"]
    latest_contents[link_str[link_str.rfind('=')+1:]] = posts[i].find('font').text + ' : ' + URL_PREFIX + link_str

#send_contents = latest_contents.copy()
temp_list = sorted(latest_contents.items(), reverse=True)

for i in range(0, 10) :
    send_contents[temp_list[i][0]] = temp_list[i][1]

with open(os.path.join(BASE_DIR, 'resources/saved_contents'), 'r') as f_read :
    for content_id in f_read :
        if send_contents.get(content_id.strip()) != None :
            del send_contents[content_id.strip()]
    f_read.close()

if len(send_contents) != 0 :
    for send_message in send_contents.values() :
        if CURR_TIME.tm_hour >= 21 or CURR_TIME.tm_hour <= 9 :
            bot.sendMessage(chat_id=my_chatid, text=send_message.strip(), disable_notification=True)
            #print(send_message)
        else :
            bot.sendMessage(chat_id=my_chatid, text=send_message.strip())
            #print(send_message)

with open(os.path.join(BASE_DIR, 'resources/saved_contents'), 'w+') as f_write :
    for write_message in latest_contents.keys() :
        f_write.write(write_message.strip() + '\n')
    f_write.close()
