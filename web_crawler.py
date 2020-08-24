import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime
from urllib.parse import urlparse,urljoin
import random
import string
import time

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

client=MongoClient()
db=client['test_database']
collection=db['test_database']
datas=db.datas
source_link="https://flinkhub.com/"
links=list()
links.append(source_link)
data={"link": source_link,
      "source_link": source_link,
      "is crawled": "no",
      "last crawl date": datetime.datetime.utcnow()}
datas.insert_one(data)
count=1
is_crawled=list()
while count<5000:
    for link in links:
        if link not in is_crawled:
            print("crawling ",link)
            try:
                r=requests.get(link)
                soup=BeautifulSoup(r.text,'html.parser')
                fa=soup.find_all("a")
            except:
                pass
            for a_tag in fa:
                valid = 0
                try:
                    l = a_tag['href']
                except:
                    pass
                # print(link)
                parsed_link = urlparse(l)
                # print(parsed_link)
                if parsed_link.scheme != 0 or parsed_link.netloc != 0 or parsed_link.path != 0:
                    if len(parsed_link.path) > 1:
                        link = urljoin(link, l)
                if bool(urlparse(l).netloc) == True and bool(urlparse(l).scheme) == True:
                    # print('valid')
                    valid = 1
                if valid == 1:
                    data = {"link": l,
                            "source_link": link,
                            "is crawled": "no",
                            "last crawl date": datetime.datetime.utcnow()}
                    datas.insert_one(data)
                    #print(data)
                    count += 1
                    if count>=5000:
                        break
                    with open(get_random_string(10) + '.html', 'w') as f:
                        f.write(l)
                    links.append(l)
                if count >= 5000:
                    break
            is_crawled.append(link)
            if count >= 5000:
                break
            time.sleep(5)