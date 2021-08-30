import re,pymysql,bs4,tkinter.messagebox
from bs4 import BeautifulSoup
import 路由生成
#-----------------------------------------------------数据库-------------------------------------------------------#
conn = pymysql.connect(user='root', passwd='',host='localhost', db='f7update')
cur = conn.cursor()
cur1 = conn.cursor()
removelist = []
cur.execute("SELECT * FROM f7remove")
for r in cur:
    removelist.append(r[1])
oldlist=[]
newlist=[]
cur.execute("SELECT * FROM f7rename WHERE version='v1'")
for r in cur:
    oldlist.append(r[1])
cur.execute("SELECT * FROM f7rename WHERE version='v2'")
for r in cur:
    newlist.append(r[1])
#----------------------------------------HTML更新-------------------------------------------------------#
def appinit(soup):
    docs = soup.find("body")
    if docs:
        app = soup.find(attrs={'id':"app"})
        if not app:
            a = str(soup)
            pattern = r"<body.*?>"
            m = re.findall(pattern, a)
            m = ''.join(m)
            a = a.replace(m, m + "\n" + "<div id=\"app\">")
            a = a.replace("</body>", "</div>" + "\n" + "</body>")
            soup = BeautifulSoup(a, "html.parser")
    docs = soup.find(attrs={'id':'app'})
    if docs:
        js=docs.find_all("script")
        if js:
            for j in js:
                docs.insert_after(j)
            a = str(soup)
            a = a.replace("<script","\n" + "<script")
            soup = BeautifulSoup(a, "html.parser")
    return soup
def pageinit(soup):
    docs = soup.find_all(attrs={'class': 'page'})
    if docs:
        for d in docs:
            if 'data-page' in d.attrs:
                p = d.attrs['data-page']
                d.attrs['data-name'] = p
                del d['data-page']
    docs = soup.find_all(attrs={'class': 'view'})
    if docs:
        for d in docs:
            if 'data-page' in d.attrs:
                p = d.attrs['data-page']
                d.attrs['data-name'] = p
                del d['data-page']
    return soup
def delallold(soup):
    for r in removelist:
        docs = soup.find_all(attrs={'class': r})
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
    return soup
def renameallold(soup):
    count = -1
    for old in oldlist:
        count = count + 1
        docs = soup.find_all(attrs={'class': old})
        if docs:
            for d in docs:
                cls = d.attrs['class']
                if len(cls) > 1:
                    i = -1
                    for cls1 in cls:
                        i = i + 1
                        if cls1 == old:
                            cls[i] = newlist[count]
                else:
                    cls = newlist[count]
                d.attrs['class'] = cls
    return soup
def delattr(soup,r):
    docs = soup.find_all(attrs={'class': r})
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
    return soup
def renameatr(soup,old,new):
    docs = soup.find_all(attrs={'class': old})
    if docs:
        for d in docs:
            cls = d.attrs['class']
            if len(cls) > 1:
                i = -1
                for cls1 in cls:
                    i = i + 1
                    if cls1 == old:
                        cls[i] = new
            else:
                cls = new
            d.attrs['class'] = cls
    return soup
def addcls(soup,elem,new):
    docs = soup.find_all(attrs={'class': elem})
    if docs:
        for d in docs:
            if "class" in d.attrs:
                if not new in d.attrs['class']:
                    cls = d.attrs['class']
                    cls.append(new)
                    d.attrs['class'] = cls
            else:
                d.attrs['class']=new
    return soup
def renamecls(soup,elem,old,new):
    docs = soup.find_all(attrs={'class': elem})
    if docs:
        for d in docs:
            if "class" in d.attrs:
                for i in d.attrs['class']:
                    if i==old:
                        cls=d.attrs['class']
                        ind=cls.index(i)
                        cls[ind]=new
                        d.attrs['class']=cls
    return soup
def renfatherattr(soup,child,old,new):
    docs = soup.find_all(attrs={'class': child})
    if docs:
        for d in docs:
            p = d.parent
            while("class" in p.attrs) and (p.attrs['class']==old):
                if (p.attrs['class']==old):
                    break
                else:
                    p=p.parent
            rem=p.unwrap()
            soup=renameatr(soup,child,new)
    return soup
def renchildattr(soup,father,old,new):
    elem = soup.find_all(attrs={'class': father})
    if elem:
        for i in elem:
            docs = i.find_all(attrs={'class': old})
            if docs:
                for d in docs:
                    cls = d.attrs['class']
                    if len(cls) > 1:
                        j = -1
                        for cls1 in cls:
                            j = j + 1
                            if cls1 == old:
                                cls[j] = new
                    else:
                        cls = new
                    d.attrs['class'] = cls
    return soup
def wrapchild(soup,father,child):
    elem = soup.find_all(attrs={'class': father})
    if elem:
        for s in elem:
            docs = s.find_all(attrs={'class':child})
            if not docs:
                obj = bs4.element.Tag(name='div', attrs={'class': child})
                child1 = s.children
                for i in child1:
                    v = i.wrap(obj)
                s.clear()
                s.append(obj)

    return soup
def searchbarinit(soup):
    docs = soup.find_all(attrs={'class': 'searchbar'})
    list = []
    if docs:
        for d in docs:
            child = d.children
            for child1 in d.find_all():
                if "class" in child1.attrs:
                    list.append(child1.attrs['class'])
            icon = d.find(attrs={'class': 'input-clear-button'})
            if icon:
                if icon.name == "a":
                    icon.name = "span"
                    del icon['href']
                if not "searchbar-icon" in list:
                    obj = bs4.element.Tag(name='i', attrs={'class': 'searchbar-icon'})
                    icon.insert_before(obj)
            sdisab = d.find(attrs={'class': 'searchbar-disable-button'})
            if sdisab:
                if sdisab.name == "a":
                    sdisab.name = "span"
                    del sdisab['href']
            if "data-search-list" in d.attrs:
                d.attrs["data-search-container"] = d.attrs['data-search-list']
                del d['data-search-list']
    return soup
def changetagname(soup,elem,new):
    docs = soup.find_all(attrs={'class':elem})
    if docs:
        for d in docs:
            if d.name != new:
                d.name=new
    return soup
def iteminit(soup):
    inplist=["input","select","textarea"]
    elem=soup.find_all(attrs={'class':'item-content'})
    if elem:
        for i in elem:
            for j in inplist:
                docs = i.find(j)
                if docs:
                    par = i.parent
                    i = renameatr(i, "item-input", "item-input-wrap")
                    par = addcls(par, "item-content", "item-input")
                docs = i.find(attrs={'class':'label'})
                if docs:
                    par = i.parent
                    i = renameatr(i, "label", "item-label")
                    par = addcls(par,"item-content","inline-label")
                    d=i.find("item-inner")
                    if not d:
                        par=wrapchild(par,"item-content","item-inner")
    return soup
def colortrans(soup):
    old =[("red","pink"),("blue","purple","deeppurple","indigo","lightblue","cyan"),("green","teal","lightgreen","lime"),("yellow","amber"),("orange","deeporange","brown"),("gray","bluegray"),("white","white"),("black","black")]
    c="bg- color- border- theme-"
    col=c.split(" ")
    c1="bg-color- text-color- border-color- color-theme-"
    col1=c1.split(" ")
    for a in col:
        ind=col.index(a)
        for i in old:
            for j in i:
                soup = renameatr(soup, a+j, col1[ind]+i[0])
                soup = renamecls(soup, "button-fill", "text-color-"+i[0], "color-"+i[0])
    return soup
def iconinit(soup,elem,icon):
    i = soup.find_all(attrs={'type': elem})
    if i:
        for inp in i:
            next=inp.find_next()
            if next.name!="i":
                obj = bs4.element.Tag(name='i', attrs={'class': "icon "+icon})
                inp.insert_after(obj)
            else:
                if not "class" in next.attrs:
                    next.attrs['class']="icon "+icon
    return soup
def checkboxinit(soup):
    soup=iconinit(soup,"checkbox","icon-checkbox")
    return soup
def soupfilter(soup):
    tag = soup.find_all('i')
    if tag:
        for t in tag:
            if not t.attrs:
                rem = t.unwrap()
    docs = soup.find_all(attrs={"class":"item-media"})
    if docs:
        for d in docs:
            elem=d.find_all(attrs={"class":"icon-checkbox"})
            if elem:
                for e in elem:
                    rem=e.unwrap()
            child=d.children
            len=0
            for i in child:
                len=len+1
            if len<1:
                rem=d.unwrap()
    return soup
def navfilter(soup):
    nav=soup.find_all(attrs={'class':'navbar'})
    if nav:
        for i in nav:
            if i.parent:
                p = i.parent
                if "class" in p.attrs:
                    if p.attrs['class']!="page":
                        page=i.find_next(attrs={'class':'page'})
                        if page:
                            page.insert(0,i)
                else:
                    page = i.find_next(attrs={'class': 'page'})
                    if page:
                        page.insert(0, i)
    return soup
def routefilter(soup):
    link=soup.find_all("a")
    if link:
        for a in link:
            if "href" in a.attrs:
                href=a.attrs['href']
                if href!="#" and href.find(".html")>-1:
                    href="/"+href.replace(".html","")+"/"
                    a.attrs['href']=href
    return soup
def iconfilter(soup,old,new):
    icon = soup.find_all(attrs={'class':old})
    if icon:
        for j in icon:
            cls=j.attrs['class']
            if len(cls)>1:
                for i in cls:
                    if i.strip()==old:
                        cls.remove(i)
                        if "f7-icons" not in cls:
                            cls.append("f7-icons")
                        j.string=new

    return soup
def fabinit(soup):
    fab = soup.find_all(attrs={'class': 'floating-button'})
    if fab:
        for i in fab:
            p=i.parent
            if "class" in p.attrs:
                if "fab" not in p.attrs['class']:
                    obj = bs4.element.Tag(name='div', attrs={'class': 'fab fab-right-bottom'})
                    cls = i.attrs['class']
                    if len(cls) > 0:
                        cnt = 0
                        for c in cls:
                            if c.find("text-color") > -1:
                                cls[cnt] = cls[cnt].replace("text-color", "color")
                                color = "color" + c[10:]
                                c2 = obj.attrs['class']
                                c2 = c2 + " " + color
                                obj.attrs['class'] = c2
                                cls.remove(c)
                                cnt = cnt + 1
                        cls.remove("floating-button")
                    if len(cls) < 1:
                        del i['class']
                    v = i.wrap(obj)
            else:
                obj = bs4.element.Tag(name='div', attrs={'class': 'fab fab-right-bottom'})
                cls = i.attrs['class']
                if len(cls) > 0:
                    cnt = 0
                    for c in cls:
                        if c.find("text-color") > -1:
                            cls[cnt] = cls[cnt].replace("text-color", "color")
                            color = "color" + c[10:]
                            c2 = obj.attrs['class']
                            c2 = c2 + " " + color
                            obj.attrs['class'] = c2
                            cls.remove(c)
                            cnt = cnt + 1
                    cls.remove("floating-button")
                if len(cls) < 1:
                    del i['class']
                v = i.wrap(obj)
    return soup
def messageinit(soup):
    docs = soup.find_all(attrs={'class':'message-text'})
    if docs:
        for d in docs:
            p=d.parent
            if "class" in p.attrs:
                cls = p.attrs['class']
                if "message-bubble" not in cls:
                    obj=bs4.element.Tag(name='div', attrs={'class':'message-bubble'})
                    v = d.wrap(obj)
    docs = soup.find_all(attrs={'class':'message-content'})
    if docs:
        for d in docs:
            avatar=d.find_all(attrs={'class':'message-avatar'})
            if avatar:
                for i in avatar:
                    rem = i.unwrap()
                    d.parent.insert(0,i)
    return soup
def swiperinit(soup):
    swiper=soup.find_all(attrs={'class':'swiper-container'})
    if swiper:
        for i in swiper:
            if "data-scrollbar" in i.attrs:
                scroll="{\"el\":\"" +i.attrs['data-scrollbar']+ "\"}"
                i.attrs['data-scrollbar']=scroll
            if "data-next-button" in i.attrs and "data-prev-button" in i.attrs:
                n=i.attrs['data-next-button']
                prev=i.attrs['data-prev-button']
                nav="{\"nextEl\":\""+n+"\",\"prevEl\":\""+prev+"\"}"
                del i['data-next-button']
                del i['data-prev-button']
                i.attrs['data-navigation']=nav
            if "data-pagination" in i.attrs:
                p="{\"el\":\"" +i.attrs['data-pagination']+ "\""
                if "data-pagination-type" in i.attrs:
                    if i.attrs['data-pagination-type']=="progress":
                        i.attrs['data-pagination-type'] = "progressbar"
                if "data-pagination-clickable" in i.attrs or "data-pagination-type" in i.attrs:
                    if "data-pagination-clickable" in i.attrs and not "data-pagination-type" in i.attrs:
                        p=p+", \"clickable\":"+i.attrs['data-pagination-clickable']+"}"
                        del i['data-pagination-clickable']
                    elif "data-pagination-type" in i.attrs and not "data-pagination-clickable" in i.attrs:
                        p = p + ", \"type\":\"" + i.attrs['data-pagination-type'] + "\"}"
                        del i['data-pagination-type']
                    elif "data-pagination-clickable" in i.attrs and "data-pagination-type" in i.attrs:
                        p = p + ", \"clickable\":" + i.attrs['data-pagination-clickable']
                        p = p + ", \"type\":\"" + i.attrs['data-pagination-type'] + "\"}"
                        del i['data-pagination-clickable']
                        del i['data-pagination-type']
                else:
                    p=p+"}"
                    del i['data-pagination']
                i.attrs['data-pagination']=p
            if "data-lazy-loading" in i.attrs:
                lazy="{\"enabled\":"+i.attrs['data-lazy-loading']+"}"
                i.attrs['data-lazy']=lazy
            preload=i.find_all(attrs={'class':'preloader'})
            if preload:
                for j in preload:
                    cls=j.attrs['class']
                    if "swiper-lazy-preloader" not in cls:
                        cls.append("swiper-lazy-preloader")
            if "data-zoom" in i.attrs:
                zoom="{\"enabled\":"+i.attrs['data-zoom']+"}"
                i.attrs['data-zoom']=zoom
    return soup

def f7htmlupdate(path):
    code_file = open(path, "r", encoding='utf-8')
    code = code_file.read()
    code_file.close()
    if path.find("index.html")>-1:
        code=code.replace("</script>","</script><script src=\"js/route.js\" type=\"text/javascript\"></script>",1)
    soup = BeautifulSoup(code, "html.parser")
    soup = appinit(soup)
    soup = pageinit(soup)
    soup = colortrans(soup)
    soup = renfatherattr(soup, "content-block-inner", "content-block", "block block-strong")
    soup = renfatherattr(soup, "card-content-inner", "card-content", "card-content card-content-padding")
    soup = renchildattr(soup, "navbar", "center", "title")
    soup = renchildattr(soup, "message", "message-label", "message-footer")
    soup = renchildattr(soup, "messages", "messages-date", "messages-title")

    soup = renchildattr(soup, "tabs", "active", "tab-active")
    soup = renchildattr(soup, "buttons", "active", "button-active")
    soup = renamecls(soup, "tab-link", "active", "tab-link-active")
    soup = renamecls(soup, "button", "active", "button-active")
    soup = wrapchild(soup, "navbar", "navbar-inner")
    soup = wrapchild(soup, "subnavbar", "subnavbar-inner")
    soup = wrapchild(soup, "toolbar", "toolbar-inner")
    soup = wrapchild(soup, "message", "message-content")
    soup = renchildattr(soup, "label-switch", "checkbox", "toggle-icon")
    soup = changetagname(soup, "toggle-icon", "i")
    soup= iteminit(soup)
    soup = searchbarinit(soup)
#    soup= checkboxinit(soup)
    soup = checkboxinit(soup)
    soup = iconinit(soup, "radio", "icon-radio")
    soup = renameatr(soup, "speed-dial", "fab fab-right-bottom")
    soup = addcls(soup,"range-slider","range-slider-init")
    soup = wrapchild(soup, "searchbar", "searchbar-inner")
    soup = renameallold(soup)
    soup = delallold(soup)
    soup = navfilter(soup)
    soup = routefilter(soup)
    soup = fabinit(soup)
    soup = messageinit(soup)
    soup = swiperinit(soup)
    soup = iconfilter(soup,"icon-camera","camera_fill")
    soup = iconfilter(soup, "icon-bars", "bars")

    soup=soupfilter(soup)
    s1 = str(soup)
    return s1
#path="C:\\Users\\Administrator\\Desktop\\f7-final-test\\v1\\messages.html"
#s=f7htmlupdate(path)
#print(s)
