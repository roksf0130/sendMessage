import telegram, requests
from bs4 import BeautifulSoup
import os

my_token = '1416123949:AAEw0e3g9jiyvSVe6Thf1W5zOmP-o266yO0'
bot = telegram.Bot(token = my_token)
#chat_id = bot.getUpdates()[-1].message.chat.id
#chat_id = '1347563170' 
chat_id = '-408388337'
url_prefix = 'https://www.ppomppu.co.kr/zboard/'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get('http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu')

html = req.text
soup = BeautifulSoup(html, 'html.parser')
posts = soup.find_all('tr',{'class':['list0','list1']})

latest_contents = []
before_contents = []
send_message_list = []
send_message = ''
write_message = ''

for i in range(1, 11) :
    #latest_contents.append(posts[i].find('font').text + ' : ' + url_prefix + posts[i].find_all('a')[1]["href"])
    latest_contents.append(url_prefix + posts[i].find_all('a')[1]["href"])

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
        bot.sendMessage(chat_id=chat_id, text=send_message.strip())

with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write :
    for i in latest_contents :
        write_message = write_message + i + '\n'

    f_write.write(write_message.strip())
    f_write.close()
