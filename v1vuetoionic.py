import re,pymysql,bs4,tkinter.messagebox,os
from bs4 import BeautifulSoup
from xml.sax.saxutils import unescape

def jsvar(soup,var):
    pattern = re.compile(r"var "+var+" = (.*?);$", re.MULTILINE | re.DOTALL)
    a=pattern.findall(soup)
    if a:
        s=a
    else:
        s=[]
    return s
def scriptfilter(script):
    s1=script.split("\n")
    line=-1
    for i in s1:
        i=i.strip()
        line=line+1
        if i.find("}")>0 and s1[line+1].find(")")>0:
            i=i.replace("\n","")
    script=("\n").join(s1)[1:]
    return script

def actioninit(soup):
    z=0
    docs=soup.find_all("script")
    if docs:
        for d in docs:
            script=d.get_text()
            script=scriptfilter(script)
            pattern="\.actions(.*)"
            m=re.findall(pattern,script)
            if m:
               for m1 in m:
                    m1=m1.replace("(","").replace(")","").replace(";","").strip()
                    varval=jsvar(script,m1)
                    for i in varval:
                        act=""
                        if i.find("{")>=0:
                            if i.find("]")<0:
                                pat=script.index(i)
                                s1=script[pat+len(i):]
                                ind=s1.index("]")
                                i=i+s1[:ind+1]
                                act=act+"\n"+i
                                z=z+1
                            else:
                                act=act+"\n"+i
                                z=z+1
                            print(act)
                            print("----------------------"+str(z)+"---------------------")
    return soup

path="C:/Users/Administrator/Desktop/f7tovue.txt"
code_file = open(path, "r", encoding='utf-8')
code = code_file.read()
code_file.close()
soup = BeautifulSoup(code, "html.parser")
soup = actioninit(soup)
#print(soup)
