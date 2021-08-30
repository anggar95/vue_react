from bs4 import BeautifulSoup
import requests
#path="https://ionicons.com/"
#response = requests.get(path).text
#soup = BeautifulSoup(response,"html.parser")
#name_list = soup.find_all("i",attrs={'class': 'ion'})

s1="euro facebook github googleplus instagram linkedin rss twitter usd yen".split(" ")
for i in s1:
    print("logo-"+i)