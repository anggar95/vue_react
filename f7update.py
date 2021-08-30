import os,requests,bs4,pymysql,re,string
#-----------------------------------------------------数据库-------------------------------------------------------#
removelist = []
oldlist=[]
newlist=[]
oldappparam=[]
newappparam=[]
appparampar=[]
oldjsparam=[]
newjsparam=[]
jsparampar=[]
oldjsmethod=[]
newjsmethod=[]
jsmethodpar=[]
oldjsevent=[]
newjsevent=[]
oldonevent=[]
newonevent=[]
oneventpar=[]
conn = pymysql.connect(user='root', passwd='',host='localhost', db='f7update')
cur = conn.cursor()
cur1 = conn.cursor()
cur.execute("SELECT * FROM f7remove")
for r in cur:
    removelist.append(r[1])
r=[]
cur.execute("SELECT * FROM f7rename WHERE version='v1'")
for r in cur:
    oldlist.append(r[1])
r=[]
cur.execute("SELECT * FROM f7rename WHERE version='v2'")
for r in cur:
    newlist.append(r[1])
cur.execute("SELECT * FROM f7jsappparam WHERE version='v2'")
for r in cur:
    oldappparam.append(r[1])
    newappparam.append(r[2])
    appparampar.append(r[4])
cur.execute("SELECT * FROM f7jsparam WHERE version='v2'")
for r in cur:
    oldjsparam.append(r[1])
    newjsparam.append(r[2])
    jsparampar.append(r[4])
cur.execute("SELECT * FROM f7jsmethod WHERE version='v2'")
for r in cur:
    oldjsmethod.append(r[1])
    newjsmethod.append(r[2])
    jsmethodpar.append(r[4])
cur.execute("SELECT * FROM f7jsevents WHERE version='v2'")
for r in cur:
    oldjsevent.append(r[1])
    newjsevent.append(r[2])
cur.execute("SELECT * FROM f7onevent WHERE version='v2'")
for r in cur:
    oldonevent.append(r[1])
    newonevent.append(r[2])
    oneventpar.append(r[4])
#---2.3.1----#
def deleteelem(aa,bb,cc,dd):

    pass
def find_string(s,t):
    try:
        if s.index(t)>-1:
            return True
    except(ValueError):
        return False
def opener(s):
    str1 = s.split("\n")
    open = 0
    close = 0
    for i in str1:
        open = open + i.count("{")
        open = open - i.count("}")
        close = close + i.count("}")
        if open == 0:
            break
    return close

#------------------------------------------------读取页面----------------------------------------------------------#
fname="C:\\Users\\Administrator\\Desktop\\f7\\framework7-1.6.4\\kitchen-sink-ios\\index.html"
html_code=open(fname,"r+")
h=html_code.readlines()
html_code.close()
s=""
for i in h:
    s=s+i
str1=s.split("\n")
s2=""
for i in str1:
    if (i.strip()!=""):
        s2=s2+i+"\n"
s2=s2[:-1]
#h1=open(fname,"w")
#h1.write(s2)
#h1.close()
soup=bs4.BeautifulSoup(s2,"html.parser")
#--------------------------------------------------删除------------------------------------------------------------#
"""
for r in removelist:
    docs=soup.find_all(attrs={'class':r})
    if docs:
        for d in docs:
            cls = d.attrs['class']
            if len(cls) > 1:
                i = -1
                for cls1 in cls:
                    i = i + 1
                    if cls1 == r:
                        cls.remove(cls1)
            else:
                rem = d.unwrap()
"""
#-------------------------------------------------替换-------------------------------------------------------------#
count=-1
for old in oldlist:
    count=count+1
    docs = soup.find_all(attrs={'class': old})
    if docs:
        for d in docs:
            cls = d.attrs['class']
            if len(cls)>1:
                i=-1
                for cls1 in cls:
                    i=i+1
                    if cls1==old:
                        cls[i]=newlist[count]
            else:
                cls=newlist[count]
            d.attrs['class']=cls
#--------------------------------------------css修改--------------------------------------------------------------#
"""
docs = soup.find_all("link",attrs={'rel':'stylesheet'})
list1=[]
if docs:
    par=docs[0].parent
    ind=par.index(par.find("link",attrs={'rel':'stylesheet'}))
    for d in docs:
        code=str(d)
        if code.find("rtl.css")>-1:
            list1.append("rtl")
        elif code.find("rtl.min.css")>-1:
            list1.append("rtl.min")
        elif code.find("min.css") > -1:
            if code.find("rtl") == -1:
                list1.append("min")
        rem=d.unwrap()
    if len(list1)>0:
        list2=list(set(list1))
        list1=list2
        i=-1
        for c in list1:
            i=i+1
            if c=="rtl":
                obj = bs4.element.Tag(name='link', attrs={'href': 'framework7.rtl.css','rel':'stylesheet','type':'text/css/'})
            elif c=="min":
                obj = bs4.element.Tag(name='link', attrs={'href': 'framework7.min.css','rel':'stylesheet','type':'text/css/'})
            elif c == "rtl.min":
                obj = bs4.element.Tag(name='link', attrs={'href': 'framework7.rtl.min.css', 'rel': 'stylesheet', 'type': 'text/css/'})
            par.insert(i+ind,obj)
    else:
        obj = bs4.element.Tag(name='link', attrs={'href': 'framework7.css', 'rel': 'stylesheet', 'type': 'text/css/'})
        par.insert(ind,obj)
#--------------------------------------------VIEWS转换-------------------------------------------------------------#
for v1 in soup.find_all(attrs={'class': 'views'}):
    count = 0
    for v2 in v1.find_all(attrs={'class': 'view'}):
        count=count+1
    if count<2:
        rem=v1.unwrap()
"""
#------------------------------------------NAVBAR&TOOLBAR---------------------------------------------------------#
navbar = soup.find_all(attrs={'class':'navbar'})
if navbar:
    for i in navbar:
        docs = i.find_all(attrs={'class':'center'})
        if docs:
            for d in docs:
                cls = d.attrs['class']
                if len(cls) > 1:
                    j = -1
                    for cls1 in cls:
                        j=j + 1
                        if cls1 == 'center':
                            cls[j] = "title"
                else:
                    cls = "title"
                d.attrs['class'] = cls
        par=i.parent
        if "class" in par.attrs:
            if "view" in par.attrs['class']:
                obj=bs4.element.Tag(name='div', attrs={'class': 'page'})
                i.wrap(obj)
                if "data-page" in par.attrs:
                    p=par.attrs['data-page']
                    obj.attrs['data-name']=p
                    del par['data-page']
        docs = i.find_all(attrs={'class': 'navbar-inner'})
        if not docs:
            inner=i.children
            obj = bs4.element.Tag(name='div',attrs={'class':'navbar-inner'})
            for j in inner:
                j.wrap(obj)
subnavbar = soup.find_all(attrs={'class':'subnavbar'})
if subnavbar:
    for s in subnavbar:
        docs = s.find_all(attrs={'class': 'subnavbar-inner'})
        if not docs:
            inner = s.children
            obj = bs4.element.Tag(name='div', attrs={'class': 'subnavbar-inner'})
            for j in inner:
                j.wrap(obj)
toolbar = soup.find_all(attrs={'class':'toolbar'})
if toolbar:
    for t in toolbar:
        docs = t.find_all(attrs={'class': 'toolbar-inner'})
        if not docs:
            inner = t.children
            obj = bs4.element.Tag(name='div', attrs={'class': 'toolbar-inner'})
            for j in inner:
                j.wrap(obj)
#---------------------------------------------Content Block-------------------------------------------------------#
docs = soup.find_all(attrs={'class':'content-block-inner'})
if docs:
    for d in docs:
        p=d.parent
        cls = p.attrs['class']
        if "block" in cls:
            if len(cls) > 1:
                i = -1
                for cls1 in cls:
                    i = i + 1
                    if cls1 == "block":
                        cls[i] = "block block-strong"
            else:
                cls = "block block-strong"
            p.attrs['class'] = cls
            c=d.attrs['class']
            for c1 in c:
                if c1 == "content-block-inner":
                    c.remove(c1)
            rem = d.unwrap
            c2=""
            for c1 in c:
                c2=c2+" "+c1
                c2=c2.strip()
            if c2!="":
                p.attrs['class'] = cls+c2
docs = soup.find_all(attrs={'class':'card-content-inner'})
if docs:
    for d in docs:
        p=d.parent
        cls = p.attrs['class']
        if "card-content" in cls:
            if len(cls) > 1:
                i = -1
                for cls1 in cls:
                    i = i + 1
                    if cls1 == "card-content":
                        cls[i] = "card-content card-content-padding"
            else:
                cls = "card-content card-content-padding"
            p.attrs['class'] = cls
            c=d.attrs['class']
            for c1 in c:
                if c1 == "card-content-inner":
                    c.remove(c1)
            rem = d.unwrap
            for c1 in c:
                c2=c2+" "+c1
                c2=c2.strip()
            p.attrs['class'] = cls+c2

#----------------------------------------------data-page----------------------------------------------------------#
docs = soup.find_all(attrs={'class':'page'})
if docs:
    for d in docs:
        if 'data-page' in d.attrs:
            p=d.attrs['data-page']
            d.attrs['data-name']=p
            del d['data-page']
docs = soup.find_all(attrs={'class':'view'})
if docs:
    for d in docs:
        if 'data-page' in d.attrs:
            p=d.attrs['data-page']
            d.attrs['data-name']=p
            del d['data-page']
#--------------------------------------------FORM INPUT------------------------------------------------------------#
docs = soup.find_all(attrs={'class':'item-content'})
if docs:
    for d in docs:
        for inp in d.find_all("input"):
            if "class" in inp.parent.attrs:
                if inp.parent.attrs['class']=="item-input":
                    inp.parent.attrs['class']="item-input-wrap"
                else:
                    obj = bs4.element.Tag(name='div', attrs={'class': 'item-input-wrap'})
                    inp.wrap(obj)
            else:
                inp.parent.attrs['class'] = "item-input-wrap"
        if not "item-input" in d.attrs['class']:
            cl=d.attrs['class']
            cl=str(cl)
            d.attrs['class']=cl+" item-input"
#--------------------------------------------SEARCHBAR-------------------------------------------------------------#
docs = soup.find_all(attrs={'class':'searchbar'})
list=[]
if docs:
    for d in docs:
        child=d.children
        for child1 in d.find_all():
            if "class" in child1.attrs:
                list.append(child1.attrs['class'])
        if not "searchbar-inner" in list:
            obj = bs4.element.Tag(name='div',attrs={'class':'serachbar-inner'})
            for c in child:
                c.wrap(obj)
        icon = d.find(attrs={'class':'input-clear-button'})
        if icon:
            if icon.name=="a":
                icon.name="span"
                del icon['href']
            if not "searchbar-icon" in list:
                obj = bs4.element.Tag(name='i',attrs={'class':'searchbar-icon'})
                icon.insert_before(obj)
        sdisab = d.find(attrs={'class':'searchbar-disable-button'})
        if sdisab:
            if sdisab.name=="a":
                sdisab.name="span"
                del sdisab['href']
#-----------------------------------------------FAB----------------------------------------------------------------#
docs = soup.find_all(attrs={'class':'floating-button'})
if docs:
    for d in docs:
        if len(d.attrs['class'])>1:
            for ss in d.attrs['class']:
                if ss=="floating-button":
                    ss="fab fab-right-bottom"
                    d.attrs['class'].remove(ss)
                s=s+" "+ss
                s=s.strip()
        else:
            s="fab fab-right-bottom"
            del d.attrs['class']
        obj = bs4.element.Tag(name='div',attrs={'class':s})
        d.wrap(obj)
#--------------------------------------Tabs & Buttons & Links -----------------------------------------------------#
docs = soup.find_all(attrs={'class':'tabs'})
if docs:
    for d in docs:
        for acttab in d.find_all(attrs={'class':'active'}):
            if len(acttab.attrs['class'])>1:
                i = -1
                cls=acttab.attrs['class']
                for cls1 in cls:
                    i = i + 1
                    if cls1 == "active":
                        cls[i] = "tab-active"
            else:
                cls = "tab-active"
            acttab.attrs['class'] = cls
        for actlink in d.find_all(attrs={'class': 'tablink'}):
            for i in actlink.attrs['class']:
                if i=="active":
                    i="tab-link-active"
docs = soup.find_all(attrs={'class':'segmented'})
if docs:
    for d in docs:
        for actbtn in d.find_all(attrs={'class':'active'}):
            if len(actbtn.attrs['class'])>1:
                i = -1
                cls=actbtn.attrs['class']
                for cls1 in cls:
                    i = i + 1
                    if cls1 == "active":
                        cls[i] = "button-active"
            else:
                cls = "button-active"
            actbtn.attrs['class'] = cls
#------------------------------------------Switch/Toggle-----------------------------------------------------------#
docs = soup.find_all("label")
if docs:
    for d in docs:
        if "toggle" in d.attrs['class']:
            for cb in d.find_all(attrs={'class':'checkbox'}):
                if len(cb.attrs['class']) > 1:
                    i = -1
                    cls = []
                    cls = cb.attrs['class']
                    for cls1 in cls:
                        i = i + 1
                        if cls1 == "checkbox":
                            cls[i] = "toggle-icon"
                else:
                    cls = "toggle-icon"
                cb.attrs['class'] = cls
                if cb.name!="span":
                    cb.name="span"
#---------------------------------------------HTML APP-------------------------------------------------------------#
docs=soup.find_all(attrs={'id':'app'})
if not docs:
    if soup.find("body"):
        a=str(soup)
        pattern=r"<body.*?>"
        m = re.findall(pattern,a)
        m=''.join(m)
        a=a.replace(m,m+"\n"+"<div id=\"app\">")
        a=a.replace("</body>","</div>"+"\n"+"</body>")
        soup=a
a=str(soup)
a=a.replace("['item-content'] item-input","item-content")
#f = open(fname, 'w',encoding='utf-8')
#f.write(a)
#f.close()
print(a)
print("完成")
