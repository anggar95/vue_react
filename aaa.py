from bs4 import BeautifulSoup
import re

def scriptfilter(script):
    s1 = script.split("\n")
    line = -1
    for i in s1:
        i = i.strip()
        line = line + 1
        if i.find("}") > -1 and i.find(")") < 0:
            if s1[line + 1].find(")") > -1:
                s1[line] = i + s1[line + 1]
                l = line + 1
                s1[l] = ""
    while '' in s1:
        s1.remove('')
    script = ("\n").join(s1)[1:]
    return script

def actioninit(soup):
    docs=soup.find_all("script")
    if docs:
        for d in docs:
            act_list=[]
            d=scriptfilter(d.get_text())
            act=re.findall(r"(.*)actions(.*)",d)
            if act:
                for i in act:
                    i=i[0]+"actions"+i[1]
                    i=i.strip()
                    act_list.append(i)
            l=d.split("\n")
            ind=0
            line = []
            for i in l:
                ind=ind+1
                for j in act_list:
                    if i.find(j)>-1:
                        k=ind
                        s=l[k]
                        str1=i
                        while s.find('});')>-1:
                            s=l[k]
                            str1=str1+"\n"+s
                            k+=1
                            if s.find("});")>-1:
                                break
                        if str1.strip()!="" and k>-1:
                            line.append(k)
                        break
            ind=0
            for j in l:
                if j.find("{") > -1:
                    break
                ind = ind + 1
            k=ind
            for i in line:
                body = ""
                while k<i:
                    if l[k].find("{") < 0:
                        k = k + 1
                    else:
                        break
                while k<i:
                    body=body+"\n"+l[k]
                    k=k+1
                body=body[1:]
                c=body.count("[")

                print("------------"+str(c)+"-----------------")
                print(body)
    return soup

path="C:/Users/Administrator/Desktop/f7tovue.txt"
code_file = open(path, "r", encoding='utf-8')
code = code_file.read()
code_file.close()
soup = BeautifulSoup(code, "html.parser")
soup = actioninit(soup)
