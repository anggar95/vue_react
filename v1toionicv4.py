import re,pymysql,bs4,tkinter.messagebox
from bs4 import BeautifulSoup
from xml.sax.saxutils import unescape

def buttoninit(soup):
    button = soup.find_all(attrs={'class':'button'})
    if button:
        for b in button:

    return soup

path="C:/Users/Administrator/Desktop/ionictestvue.txt"
code_file = open(path, "r", encoding='utf-8')
code = code_file.read()
code_file.close()
soup = BeautifulSoup(code, "html.parser")
soup = buttoninit(soup)