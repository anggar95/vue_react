import re,pymysql,bs4,tkinter.messagebox
from bs4 import BeautifulSoup
from xml.sax.saxutils import unescape
def f7tovue(soup,old,new):
    docs = soup.find_all(attrs={'class':old})
    if docs:
        for d in docs:
            d.name = new
            cls = d.attrs['class']
            i = -1
            if len(cls) > 1:
                for cls1 in cls:
                    i = i + 1
                    if cls1 == old:
                        cls.remove(cls1)
            else:
                del d['class']
    return soup
def extattr(soup,old,elem,new):
    docs=soup.find_all(attrs={'class':old})
    if docs:
        for d in docs:
            d.name=elem
            cls = d.attrs['class']
            if len(cls) > 1:
                for cls1 in cls:
                    if cls1 == old:
                        cls.remove(cls1)
            else:
                del d['class']
            d.attrs[new]=""
    return soup
def checkcardinner(soup):
    docs = soup.find_all(attrs={'class':'card-content'})
    if docs:
        for d in docs:
            elem=d.find_all(attrs={'class':'card-content-inner'})
            if not elem:
                d.attrs[":inner"]="false"
    return soup
def addattr(soup,old,new,att):
    docs = soup.find_all(attrs={'class':att})
    if docs:
        for d in docs:
            d=f7tovue(d,old,new)
            if "class" in d.attrs:
                cls=d.attrs['class']
                if att in cls:
                    cls.remove(att)
                if len(cls)<1:
                    del d['class']
                d.attrs[att]=""
    return soup
def innerattr(soup,par,child,attr):
    docs=soup.find_all(attrs={'class':par})
    if docs:
        for d in docs:
            elem=d.find_all(attrs={'class':child})
            if elem:
                for e in elem:
                    rem = e.unwrap()
                    d.name=attr.split(" ")[0].strip()
                    d.attrs[attr.split(" ")[1].strip()]=""
    return soup
def changeattrname(soup,elem,old,new):
    docs=soup.find_all(elem)
    if docs:
        for d in docs:
            if old in d.attrs:
                oldval=d.attrs[old]
                del d[old]
                d.attrs[new]=oldval
    return soup
def renattr(soup,elem,attr,old,new):
    docs=soup.find_all(attrs={attr:elem})
    if docs:
        for d in docs:
            if attr in d.attrs:
                a = d.attrs[attr]
                i = -1
                if len(a) > 1:
                    for cls1 in a:
                        i = i + 1
                        if cls1 == old:
                            a.remove(cls1)
                            d.attrs[new]=""
                else:
                    if d.attrs[attr]==old:
                        del d[attr]
                        d.attrs[new]=""
    return soup
def colorattr(soup,elem):
    docs=soup.find_all(attrs={'class':elem})
    if docs:
        for d in docs:
            if "class" in d.attrs:
                cls = d.attrs['class']
                for c in cls:
                    if c.find("ripple-")>-1:
                        prop = c.split("color-")[1]
                        cls.remove(c)
                        d.attrs['ripple-color'] = prop
                for c in cls:
                    if c.find("color-") > -1:
                        prop = c.split("color-")[1]
                        cls.remove(c)
                        d.attrs['color'] = prop
                for c in cls:
                    if c.find("theme-")>-1:
                        prop = c.split("theme-")[1]
                        cls.remove(c)
                        d.attrs['theme'] = prop
                for c in cls:
                    if c.find("bg-") > -1:
                        prop = c.split("bg-")[1]
                        cls.remove(c)
                        d.attrs['bg'] = prop
                for c in cls:
                    if c.find("layout-") > -1:
                        prop = c.split("layout-")[1]
                        cls.remove(c)
                        d.attrs['layout'] = prop
    return soup
def chipinit(soup):
    docs=soup.find_all(attrs={'class':'chip'})
    if docs:
        soup=colorattr(soup, "chip")
        for d in docs:
            text=d.find(attrs={'class':'chip-label'})
            if text:
                inner=text.get_text()
                d.attrs['text']=inner
                text.clear()
                rem = text.unwrap()
            media=d.find(attrs={'class':'chip-media'})
            if media:
                img=media.find("img")
                if img:
                    inner=img.decode().replace("\"","'")
                    d.attrs['media']=inner
                cls=media.attrs['class']
                for c in cls:
                    if c.find("bg-") > -1:
                        prop = c.split("bg-")[1]
                        cls.remove(c)
                        d.attrs['media-bg'] = prop
                for c in cls:
                    if c.find("color-") > -1:
                        prop = c.split("color-")[1]
                        cls.remove(c)
                        d.attrs['media-color'] = prop
                media.clear()
                rem = media.unwrap()
            deletable=d.find(attrs={'class':'chip-delete'})
            if deletable:
                d.attrs['deleteable'] = ""
                d.attrs['@delete']="onChipDelete"
                deletable.clear()
                rem = deletable.unwrap()
    return soup
def fabinit(soup):
    color="pink green blue black white red orange lightblue gray yellow bluegray brown deeporange amber lime lightgreen teal cyan indigo deeppurple purple".split(" ")
    soup = colorattr(soup, "speed-dial-buttons")
    soup = colorattr(soup, "speed-dial")
    soup = colorattr(soup,"floating-action-button")
    docs=soup.find_all(attrs={'class':'speed-dial-buttons'})
    if docs:
        for d in docs:
            elem=d.find_all("a")
            if elem:
                for e in elem:
                    e.name="f7-fab-action"
                    if "class" in e.attrs:
                        cls=e.attrs['class']
                        for c in cls:
                            if c in color:
                                cls.remove(c)
                                e.attrs['color']=c
                        if len(e.attrs['class'])<1:
                            del e['class']
    return soup
def checkform(soup):
    key="false"
    form = soup.find_all(attrs={'class':'list-block'})
    if form:
        for i in form:
            inp = soup.find_all("input")
            sel = soup.find_all("select")
            area = soup.find_all("textarea")
            if inp:
                key="true"
            if sel:
                key="true"
            if area:
                key="true"
    return key
def forminit(soup):
    docs = soup.find_all(attrs={'class':'floating-label'})
    if docs:
        for d in docs:
            cls=d.attrs['class']
            cls.remove("floating-label")
            if len(cls)<1:
                del d['class']
            par = d.parent
            while par.parent:
                if par.name=="li":
                    break
                else:
                    par=par.parent
            if "label" not in cls:
                par.attrs['floating']=""
            else:
                d.attrs['floating']=""
    docs=soup.find_all("form")
    if docs:
        for d in docs:
            if "class" in d.attrs:
                if not "list-block" in d.attrs['class']:
                    rem = d.unwrap()
            else:
                rem=d.unwrap()
    form = soup.find_all(attrs={'class': 'list-block'})
    if form:
        for i in form:
            inp = i.find_all("input")
            sel = i.find_all("select")
            area = i.find_all("textarea")
            item = i.find_all(attrs={'class':'item-input'})
            if item:
                for j in item:
                    rem=j.unwrap()
            item = i.find_all(attrs={'class': 'label-switch'})
            if item:
                for j in item:
                    check = j.find_all(attrs={'type':'checkbox'})
                    if check:
                        for k in check:
                            k.attrs['type']="switch"
                    rem = j.unwrap()
            item = i.find_all(attrs={'class': 'checkbox'})
            if item:
                for j in item:
                    rem = j.unwrap()
            item = i.find_all(attrs={'class': 'range-slider'})
            if item:
                for j in item:
                    rem = j.unwrap()

            if inp:
                i.attrs['form']=""
                for j in inp:
                    j.name="f7-input"
                label=i.find_all(attrs={'class':'label'})
                if label:
                    for l in label:
                        l.name="f7-label"
                        cls=l.attrs['class']
                        cls.remove("label")
                        if "item-title" in cls:
                            cls.remove("item-title")
                        if len(cls)<1:
                            del l['class']
                button=soup.find_all(attrs={'class':'list-button'})
                if button:
                    for btn in button:
                        inner = btn.get_text().strip()
                        if inner != "":
                            btn.clear()
            if sel:
                for s in sel:
                    s.name="f7-input"
                    s.attrs['type']="select"
            if area:
                for a in area:
                    a.name="f7-input"
                    a.attrs['type']="textarea"

    return soup

def iconinit(soup):
    docs = soup.find_all(attrs={'class':'icon'})
    if docs:
        soup=colorattr(soup,"icon")
        for d in docs:
            if "style" in d.attrs:
                style=d.attrs['style']
                st=style.split(";")
                for s in st:
                    d.attrs['size']=s
                    if s.find("font-size")>-1:
                        font=s.split(":")[1].strip()
                        d.attrs['size']=font
                        st.remove(s)
                        style=(";").join(st)
                        d.attrs['style']=style
                        if len(d.attrs['style'])<0:
                            del d['style']
            cls=d.attrs['class']
            if "f7-icons" in cls:
                d.attrs['f7']=d.get_text().strip()
                cls.remove('f7-icons')
            if "material-icons" in cls:
                d.attrs['material']=d.get_text().strip()
                cls.remove('material-icons')
            if "fa" in cls:
                for c in cls:
                    if c.find("fa-")>-1:
                        faval=c.split("-")[1]
                        d.attrs['fa']=faval
                        cls.remove(c)
                        cls.remove("fa")
            for c in cls:
                if c.find("ion-")>-1:
                    ionval = c.split("-")[1]
                    d.attrs['ion'] = ionval
                    cls.remove(c)
            for c in cls:
                if c.find("icon-") > -1:
                    ionval = c.split("-")[1]
                    d.attrs['icon'] = ionval
                    cls.remove(c)
            if len(d.attrs['class'])<0:
                del d['class']
    return soup
def gridinit(soup):
    docs=soup.find_all(attrs={'class':'row'})
    if docs:
        for d in docs:
            for child in d.find_all():
                if "class" in child.attrs:
                    cls=child.attrs['class']
                    for c in cls:
                        if c.find("col-")>-1:
                            child.name="f7-col"
                            val=c.split("col-")[1]
                            if val=="auto":
                                cls.remove(c)
                            else:
                                child.attrs['width']=val
                                cls.remove(c)
                    for c in cls:
                        if c.find("tablet-")>-1:
                            val=c.split("tablet-")[1]
                            if val=="auto":
                                cls.remove(c)
                            else:
                                child.attrs['tablet-width']=val
                                cls.remove(c)
                    if len(cls)<1:
                        del child["class"]
    return soup
def listinit(soup):
    docs = soup.find_all(attrs={"class":"list-block"})
    if docs:
        for d in docs:
            cls = d.attrs['class']
            if "inset" in d.attrs['class']:
                d.attrs['inset']=""
                cls.remove("inset")
            if "tablet-inset" in d.attrs['class']:
                d.attrs['tablet-inset']=""
                cls.remove("tablet-inset")
            ul=d.find_all("ul")
            if ul:
                for u in ul:
                    rem = u.unwrap()
            inner=d.find_all(attrs={'class':'item-inner'})
            if inner:
                for i in inner:
                    rem=i.unwrap()
            row=d.find_all(attrs={'class':'item-title-row'})
            if row:
                for i in row:
                    rem=i.unwrap()
            divider=d.find_all(attrs={'class':'item-divider'})
            if divider:
                for j in divider:
                    j.name="f7-list-item"
                    j.attrs['divider']=""
                    cls=j.attrs['class']
                    cls.remove('item-divider')
                    if len(cls)<1:
                        del j['class']
                    j.attrs['title']=j.get_text().strip()
                    j.clear()
            item=d.find_all(attrs={'class':'item-content'})
            if item:
                for i in item:
                    cls = i.attrs['class']
                    cls.remove("item-content")
                    if len(cls) < 1:
                        del i['class']
                    if i.name!="li":
                        rem=i.unwrap()
            li=d.find_all("li")
            if li:
                for i in li:
                    i.name="f7-list-item"
                    link=i.find_all(attrs={'class':'item-link'})
                    if link:
                        for l in link:
                            i.attrs=dict(i.attrs,**l.attrs)
                    title=i.find(attrs={'class':'item-title'})
                    if title:
                        i.attrs['title']=title.get_text()
                        title.clear()
                        rem = title.unwrap()
                    subtitle=i.find(attrs={'class':'item-subtitle'})
                    if subtitle:
                        i.attrs['subtitle']=subtitle.get_text().strip()
                        subtitle.clear()
                        rem = subtitle.unwrap()
                    itemtext=i.find(attrs={'class':'item-text'})
                    if itemtext:
                        i.attrs['text']=itemtext.get_text().strip()
                        itemtext.clear()
                        rem = itemtext.unwrap()
                    badge=i.find(attrs={'class':'badge'})
                    if badge:
                        i.attrs['badge']=badge.get_text().strip()
                        if 'bg' in badge.attrs:
                            i.attrs['badge-color']=badge.attrs['bg']
                        badge.clear()
                        rem = badge.unwrap()
                    media = d.find(attrs={'class': 'item-media'})
                    if media:
                        i.attrs['media'] = ""
                        img = media.find("img")
                        if img:
                            inner = img.decode().replace("\"", "'")
                            i.attrs['media'] = inner
                            media.clear()
                        rem = media.unwrap()
                    after = d.find(attrs={'class': 'item-after'})
                    if after:
                        aftertext=after.get_text().strip()
                        if aftertext!="":
                            i.attrs['after']=aftertext
                        after.clear()
                        rem = after.unwrap()
                    swipeout=d.find(attrs={'class':'swipeout'})
                    if swipeout:
                        i.attrs['swipeout']=""
                        cls=swipeout.attrs['class']
                        cls.remove("swipeout")
                        if len(cls)<1:
                            del swipeout['class']
                        cont=swipeout.find_all(attrs={'class':'swipeout-content'})
                        if cont:
                            for c in cont:
                                rem=c.unwrap()
                        right=swipeout.find_all(attrs={'class':'swipeout-actions-right'})
                        left=swipeout.find_all(attrs={'class':'swipeout-actions-left'})
                        if right:
                            for right_act in right:
                                right_act.name="f7-swipeout-actions"
                                cls=right_act.attrs['class']
                                cls.remove("swipeout-actions-right")
                                if len(cls)<1:
                                    del right_act['class']
                                    swipebtn=right_act.find_all("a")
                                    if swipebtn:
                                        for s in swipebtn:
                                            s.name="f7-swipeout-button"
                                            if "class" in s.attrs:
                                                cls=s.attrs['class']
                                                for c in cls:
                                                    if c.find("color-")>-1:
                                                        c=c.strip()
                                                        ind=c.index("color-")+6
                                                        s.attrs['color']=c[ind:]
                                                        cls.remove(c)
                                                if len(cls)<1:
                                                    del s['class']
                                    swipedel=right_act.find(attrs={'class':'swipeout-delete'})
                                    if swipedel:
                                        swipedel.attrs['delete']=""
                                        cls=swipedel.attrs['class']
                                        cls.remove("swipeout-delete")
                                        if len(cls)<1:
                                            del swipedel['class']
                                        i.attrs['@swipeout:deleted']="onSwipeoutDeleted"
                                    overswipe = right_act.find(attrs={'class': 'swipeout-overswipe'})
                                    if overswipe:
                                        overswipe.attrs['overswipe'] = ""
                                        cls = overswipe.attrs['class']
                                        cls.remove("swipeout-overswipe")
                                        if len(cls) < 1:
                                            del overswipe['class']
                                        i.attrs['@swipeout:overswipe'] = "onSwipeoutOverswipe"
                                    close = right_act.find(attrs={'class': 'swipeout-close'})
                                    if close:
                                        close.attrs['close'] = ""
                                        cls = close.attrs['class']
                                        cls.remove("swipeout-close")
                                        if len(cls) < 1:
                                            del close['class']
                                        i.attrs['@swipeout:close'] = "onSwipeoutClose"
                        if left:
                            for left_act in left:
                                left_act.name="f7-swipeout-actions"
                                left_act.attrs['left']=""
                                cls = left_act.attrs['class']
                                cls.remove("swipeout-actions-left")
                                if len(cls) < 1:
                                    del left_act['class']
                                swipebtn = left_act.find_all("a")
                                if swipebtn:
                                    for s in swipebtn:
                                        s.name = "f7-swipeout-button"
                                        if "class" in s.attrs:
                                            cls = s.attrs['class']
                                            for c in cls:
                                                if c.find("color-") > -1:
                                                    c = c.strip()
                                                    ind = c.index("color-") + 6
                                                    s.attrs['color'] = c[ind:]
                                                    cls.remove(c)
                                            if len(cls) < 1:
                                                del s['class']
                                swipedel = left_act.find(attrs={'class': 'swipeout-delete'})
                                if swipedel:
                                    swipedel.attrs['delete'] = ""
                                    cls = swipedel.attrs['class']
                                    cls.remove("swipeout-delete")
                                    if len(cls) < 1:
                                        del swipedel['class']
                                    i.attrs['@swipeout:deleted'] = "onSwipeoutDeleted"
                                overswipe = left_act.find(attrs={'class': 'swipeout-delete'})
                                if overswipe:
                                    overswipe.attrs['overswipe'] = ""
                                    cls = overswipe.attrs['class']
                                    cls.remove("swipeout-overswipe")
                                    if len(cls) < 1:
                                        del overswipe['class']
                                    i.attrs['@swipeout:overswipe'] = "onSwipeoutOverswipe"
                                close = left_act.find(attrs={'class': 'swipeout-close'})
                                if close:
                                    close.attrs['close'] = ""
                                    cls = close.attrs['class']
                                    cls.remove("swipeout-close")
                                    if len(cls) < 1:
                                        del close['class']
                                    i.attrs['@swipeout:close'] = "onSwipeoutClose"
                    btn=i.find(attrs={'class':'list-button'})
                    if btn:
                        i.name="f7-list-button"
                        if "href" in btn.attrs:
                            if btn.attrs['href'].strip()=="#":
                                del btn['href']
                            else:
                                i.attrs['href']=btn.attrs['href']
                        cls=btn.attrs['class']
                        cls.remove("list-button")
                        if "item-link" in cls:
                            cls.remove("item-link")
                        for c in cls:
                            if c.find("color-") > -1:
                                ind=c.index("color-")+6
                                i.attrs['color'] = c[ind:].strip()
                                cls.remove(c)
                        if len(cls)<1:
                            del btn['cls']
                        else:
                            i.attrs['class']=cls
                        inner=btn.get_text().strip()
                        if inner!="":
                            i.attrs['title']=inner
                            btn.clear()

                        rem=btn.unwrap()
                    link = i.find(attrs={'class': 'item-link'})
                    if link:
                        i.attrs['link'] = link.attrs['href']
                        del link['href']
                        cls = link.attrs['class']
                        cls.remove('item-link')
                        if len(cls) < 1:
                            del link['class']
                        else:
                            i.attrs['class'] = cls
                            del link['class']
                        if not "title" in i.attrs:
                            i.attrs['title'] = link.get_text().strip()
                            link.clear()
                        rem = link.unwrap()
            group=d.find_all(attrs={'class':'list-group-title'})
            if group:
                for g in group:
                    gtitle=g.get_text()
                    g.name="f7-list-item"
                    g.attrs['group-title']=""
                    g.attrs['title']=gtitle
                    cls=g.attrs['class']
                    cls.remove("list-group-title")
                    if len(cls)<1:
                        del g['class']
                    g.clear()
    return soup
def listfilter(soup):
    docs = soup.find_all("f7-list",attrs={'form':''})
    if docs:
        for d in docs:
            elem=d.find_all("f7-icon")
            if elem:
                for e in elem:
                    e.attrs['slot']="media"
                    par=e.parent
                    while par:
                        if par.name=="f7-list-item":
                            break
                        else:
                            par=par.parent
                    if "media" in par.attrs:
                        del par['media']
            elem=d.find_all("f7-list-item")
            if elem:
                for e in elem:
                    if "class" in e.attrs:
                        cls=e.attrs['class']
                        if "smart-select" in cls:
                            cls.remove("smart-select")
                            e.attrs['smart-select']=""
                            if len(cls)<1:
                                del e['class']
                            dlist = list(e.attrs.keys())
                            for i in dlist:
                                if i.find("data-") > -1:
                                    e.attrs["smart-select-" + i[5:]]=e.attrs[i]
                                    del e[i]
                            input=e.find_all("f7-input",attrs={'type':'select'})
                            if input:
                                for inp in input:
                                    inp.name="select"
                                    optgroup=inp.find_all("optgroup")
                                    if optgroup:
                                        for opt in optgroup:
                                            inp.attrs['multiple']="multiple"

    docs = soup.find_all("f7-list-item")
    if docs:
        for d in docs:
            elem=d.find_all("f7-input",attrs={'type':'checkbox'})
            if elem:
                for e in elem:
                    d.attrs=dict(d.attrs, **e.attrs)
                    del d['type']
                    d.attrs['checkbox']=""
                    if "checked" in d.attrs:
                        d.attrs['checked']=""
                    rem = e.unwrap()
    docs = soup.find_all("f7-list-item")
    if docs:
        for d in docs:
            elem = d.find_all("f7-input", attrs={'type': 'radio'})
            if elem:
                for e in elem:
                    d.attrs = dict(d.attrs, **e.attrs)
                    del d['type']
                    d.attrs['radio'] = ""
                    if "checked" in d.attrs:
                        d.attrs['checked'] = ""
                    rem = e.unwrap()
    docs = soup.find_all("f7-icon",attrs={'icon':'form'})
    if docs:
        for d in docs:
            rem=d.unwrap()

    docs=soup.find_all("f7-list")
    if docs:
        for d in docs:
            a=d.find_all("f7-accordion-item")
            if a:
                for accordion in a:
                    d.attrs['accordion']=""
                    accordion.name="f7-list-item"
                    accordion.attrs["accordion-item"]=""
                    if "link" in accordion.attrs and accordion.attrs['link'].strip()=="#":
                        del accordion['link']
                    cont=accordion.find_all("f7-accordion-content")
                    if cont:
                        for content in cont:
                            child = content.children
                            obj = bs4.element.Tag(name='f7-block')
                            for i in child:
                                v = i.wrap(obj)
                            content.clear()
                            v=content.wrap(obj)
            if "class" in d.attrs:
                if "contacts-block" in d.attrs['class']:
                    cls=d.attrs['class']
                    cls.remove("contacts-block")
                    if len(cls)<1:
                        del d['class']
                    d.attrs['contacts']=""
                    title=[]
                    tit=d.find_all("f7-list-item")
                    if tit:
                        for j in tit:
                            if 'title' in j.attrs:
                                x = j.attrs['title']
                                if not x in title:
                                    title.append(x)
                    str1=("\n").join(title)
                    list1=str1.split("\n")
                    j=0
                    while j<len(list1):
                        if list1[j].strip()=="":
                            list1.remove(list1[j])
                        list1[j]="'"+list1[j]+"'"
                        if len(list1[j])<4:
                            list1[j]=list1[j]+":["
                            if j!=0:
                                list1[j-1]=list1[j-1]+"\n"+"],"
                        else:
                            list1[j]=list1[j]+","
                        j=j+1
                    j=0
                    while j < len(list1):
                        if list1[j].find("]")>0:
                            list1[j]=list1[j].replace("',","'")
                        j=j+1
                    list1[len(list1) - 1] = list1[len(list1) - 1].replace("',","'") + "\n"+"]"
                    str1=("\n").join(list1)
                    d.clear()
                    obj = bs4.element.Tag(name='f7-list-group', attrs={'v-for': "(group, key) in contacts"})
                    d.append(obj)
                    obj1=bs4.element.Tag(name='f7-list-item', attrs={':title': "(group, key) in contacts", "group-title":''})
                    obj2 = bs4.element.Tag(name='f7-list-item', attrs={'v-for': "name in group", ':title':"name"})
                    obj.append(obj1)
                    obj.append(obj2)
                    script=bs4.element.Tag(name='script')
                    soup.append(script)
                    scripttext="export default {"+"\n"+"data: function () {"+"\n"+ "return {"+"\n"+"contacts: {"+"\n"
                    scripttext=scripttext+str1+"\n"+"}"+"\n"+"}"+"\n"+"}"+"\n"+"}"+"\n"
                    script.string=scripttext

    return soup
def linkinit(soup):
    docs = soup.find_all(attrs={"href": "#"})
    if docs:
        for d in docs:
            del d['href']
    docs = soup.find_all("a")
    if docs:
        for d in docs:
            d.name = "f7-link"
            if 'class' in d.attrs:
                cls = d.attrs['class']
                if "link" in cls:
                    cls.remove('link')
                if len(cls) < 1:
                    del d['class']
    docs=soup.find_all(attrs={'class':'open-panel'})
    if docs:
        for d in docs:
            panel=""
            if "data-panel" in d.attrs:
                panel=d.attrs['data-panel']
                del d['data-panel']
            d.attrs['open-panel']=panel
            cls=d.attrs['class']
            cls.remove("open-panel")
            if len(cls)<1:
                del d['class']
    docs = soup.find_all(attrs={'class': 'close-panel'})
    if docs:
        for d in docs:
            panel = ""
            if "data-panel" in d.attrs:
                panel = d.attrs['data-panel']
                del d['data-panel']
            d.attrs['close-panel'] = panel
            cls = d.attrs['class']
            cls.remove("close-panel")
            if len(cls) < 1:
                del d['class']
    docs = soup.find_all(attrs={'class': 'open-popover'})
    if docs:
        for d in docs:
            popover = ""
            if "data-popover" in d.attrs:
                popover = d.attrs['data-popover']
                del d['data-popover']
            d.attrs['open-popover'] = popover
            cls = d.attrs['class']
            cls.remove("open-popover")
            if len(cls) < 1:
                del d['class']
    docs = soup.find_all(attrs={'class': 'close-popover'})
    if docs:
        for d in docs:
            popover = ""
            if "data-popover" in d.attrs:
                popover = d.attrs['data-popover']
                del d['data-popover']
            d.attrs['close-popover'] = popover
            cls = d.attrs['class']
            cls.remove("close-popover")
            if len(cls) < 1:
                del d['class']
    docs = soup.find_all(attrs={'class': 'open-popup'})
    if docs:
        for d in docs:
            popup = ""
            if "data-popup" in d.attrs:
                popup = d.attrs['data-popup']
                del d['data-popup']
            d.attrs['open-popup'] = popup
            cls = d.attrs['class']
            cls.remove("open-popup")
            if len(cls) < 1:
                del d['class']
    docs = soup.find_all(attrs={'class': 'close-popup'})
    if docs:
        for d in docs:
            popup = ""
            if "data-popup" in d.attrs:
                popup = d.attrs['data-popup']
                del d['data-popup']
            d.attrs['close-popup'] = popup
            cls = d.attrs['class']
            cls.remove("close-popup")
            if len(cls) < 1:
                del d['class']
    docs = soup.find_all(attrs={'class': 'open-sortable'})
    if docs:
        for d in docs:
            sortable = ""
            if "data-sortable" in d.attrs:
                sortable = d.attrs['data-sortable']
                del d['data-sortable']
            d.attrs['open-sortable'] = sortable
            cls = d.attrs['class']
            cls.remove("open-sortable")
            if len(cls) < 1:
                del d['class']
    docs = soup.find_all(attrs={'class': 'close-sortable'})
    if docs:
        for d in docs:
            sortable = ""
            if "data-sortable" in d.attrs:
                sortable = d.attrs['data-sortable']
                del d['data-sortable']
            d.attrs['close-sortable'] = sortable
            cls = d.attrs['class']
            cls.remove("close-sortable")
            if len(cls) < 1:
                del d['class']
    docs = soup.find_all(attrs={'class': 'toggle-sortable'})
    if docs:
        for d in docs:
            sortable = ""
            if "data-sortable" in d.attrs:
                sortable = d.attrs['data-sortable']
                del d['data-sortable']
            d.attrs['toggle-sortable'] = sortable
            cls = d.attrs['class']
            cls.remove("toggle-sortable")
            if len(cls) < 1:
                del d['class']
    docs = soup.find_all(attrs={'class': 'open-picker'})
    if docs:
        for d in docs:
            picker = ""
            if "data-picker" in d.attrs:
                picker = d.attrs['data-picker']
                del d['data-picker']
            d.attrs['open-picker'] = picker
            cls = d.attrs['class']
            cls.remove("open-picker")
            if len(cls) < 1:
                del d['class']
    docs = soup.find_all(attrs={'class': 'close-picker'})
    if docs:
        for d in docs:
            picker = ""
            if "data-picker" in d.attrs:
                picker = d.attrs['data-picker']
                del d['data-picker']
            d.attrs['close-picker'] = picker
            cls = d.attrs['class']
            cls.remove("close-picker")
            if len(cls) < 1:
                del d['class']
    docs = soup.find_all(attrs={'class': 'open-login-screen'})
    if docs:
        for d in docs:
            login = ""
            d.attrs['open-login-screen'] = login
            cls = d.attrs['class']
            cls.remove("open-login-screen")
            if len(cls) < 1:
                del d['class']
    docs = soup.find_all(attrs={'class': 'close-login-screen'})
    if docs:
        for d in docs:
            login = ""
            d.attrs['close-login-screen'] = login
            cls = d.attrs['class']
            cls.remove("close-login-screen")
            if len(cls) < 1:
                del d['class']
    docs = soup.find_all("f7-link")
    if docs:
        for d in docs:
            icon=d.find_all("f7-icon")
            if icon:
                for i in icon:
                    if "f7" in i.attrs:
                        d.attrs['icon-f7']=i.attrs['f7']
                    if "material" in i.attrs:
                        d.attrs['icon-material']=i.attrs['material']
                    if "fa" in i.attrs:
                        d.attrs['icon-fa'] = i.attrs['fa']
                    if "ion" in i.attrs:
                        d.attrs['icon-ion'] = i.attrs['ion']
                    if "size" in i.attrs:
                        d.attrs['icon-size']=i.attrs['size']
                    if "icon" in i.attrs:
                        d.attrs['icon'] = i.attrs['icon']
                    i.clear()
                    rem = i.unwrap()
                badge=d.find_all("f7-badge")
                if badge:
                    for b in badge:
                        d.attrs['badge']=b.get_text().strip()
                        if "color" in b.attrs:
                            d.attrs['badgeColor']=b.attrs['color']
                inner=d.get_text()
                d.clear()
                if inner.strip()!="":
                    d.attrs['text']=inner.strip()


    return soup
def logininit(soup):
    docs=soup.find_all("f7-page-content")
    if docs:
        for d in docs:
            if "class" in d.attrs:
                cls=d.attrs['class']
                if "login-screen-content" in cls:
                    par=d.parent
                    while par.name=="f7-page":
                        if par.name=="f7-page":
                            break
                        else:
                            par=par.parent
                    par.attrs['login-screen']=""
                    cls.remove("login-screen-content")
                    if len(cls)<1:
                        del d['class']
                    else:
                        par.attrs['class']=cls
                    rem = d.unwrap()
    return soup
def messageinit(soup):
    docs=soup.find_all("f7-message")
    if docs:
        for d in docs:
            if "message-received" in d.attrs['class']:
                d.attrs['type']="receiverd"
            if "message-sent" in d.attrs['class']:
                d.attrs['type']="sent"
            name=d.find(attrs={'class':"message-name"})
            text=d.find(attrs={'class':'message-text'})
            date = d.find(attrs={'class': 'message-date'})
            label = d.find(attrs={'class': 'message-label'})
            avatar = d.find(attrs={'class': 'message-avatar'})
            day = d.find(attrs={'class': 'message-day'})
            time = d.find(attrs={'class': 'message-time'})
            first = d.find(attrs={'class': 'message-first'})
            last = d.find(attrs={'class': 'message-last'})
            if name:
                d.attrs['name']=name.get_text().strip()
                name.clear()
                rem = name.unwrap()
            if text:
                d.attrs['text'] = text.get_text().strip()
                text.clear()
                rem = text.unwrap()
            if date:
                d.attrs['date']=date.get_text().strip()
                date.clear()
                rem = date.unwrap()
            if label:
                d.attrs['label']=label.get_text().strip()
                label.clear()
                rem = label.unwrap()
            if avatar:
                if "style" in avatar.attrs:
                    av=avatar.attrs['style']
                    for s in av:
                        if s.find("background-image")>-1:
                            image=s.split(":")[1].strip()
                            d.attrs['avatar']=avatar.attrsget_text().strip()
                            avatar.clear()
                            rem = avatar.unwrap()
            if day:
                d.attrs['day']=name.get_text().strip()
                day.clear()
                rem = day.unwrap()
            if time:
                d.attrs['time']=name.get_text().strip()
                day.clear()
                rem = day.unwrap()
            if first:
                d.attrs['first'] = first.get_text().strip()
                first.clear()
                rem = first.unwrap()
            if last:
                d.attrs['last'] = last.get_text().strip()
                last.clear()
                rem = last.unwrap()
    docs = soup.find_all("f7-messagebar")
    if docs:
        for d in docs:
            if "toolbar" in d.attrs['class']:
                cls=d.attrs['class']
                cls.remove("toolbar")
                if len(cls)<1:
                    del d['class']
            inner = d.find_all(attrs={'class':'toolbar-inner'})
            if inner:
                for i in inner:
                    cls = i.attrs['class']
                    cls.remove("toolbar-inner")
                    if len(cls) > 0:
                        d.attrs['class']=cls
                    rem = i.unwrap()
            tarea = d.find_all("textarea")
            if tarea:
                for i in tarea:
                    d.attrs['placeholder']=i.attrs['placeholder']
                    rem=i.unwrap()
            send = d.find_all(attrs={'class':'link'})
            if send:
                for i in send:
                    d.attrs['send-link'] = i.get_text().strip()
                    d.attrs['@submit']="onSubmit"
                    i.clear()
                    rem = i.unwrap()

    return soup
def barinit(soup):
    docs=soup.find_all(attrs={'class':'navbar-inner'})
    if docs:
        for d in docs:
            par=d.parent
            while par.name=="f7-navbar":
                if par.name=="f7-navbar":
                    break
                else:
                    par=par.parent
            sliding=par.find_all(attrs={'class':'sliding'})
            if sliding:
                for s in sliding:
                    s.attrs['sliding']=""
                    cls=s.attrs['class']
                    cls.remove("sliding")
                    if len(cls)<1:
                        del s['class']
            left = par.find_all(attrs={'class': 'left'})
            if left:
                for c in left:
                    c.name = "f7-nav-left"
                    cls = c.attrs['class']
                    cls.remove("left")
                    if len(cls) < 1:
                        del c['class']
                    elem = c.find_all("f7-link")
                    if elem:
                        for e in elem:
                            if "back" in e.attrs:
                                if "text" in e.attrs:
                                    e.attrs['back-link'] = e.attrs['text']
                                    del e['text']
                                else:
                                    e.attrs['back-link'] = ""
                                del e['back']
                            else:
                                if "icon" in e.attrs:
                                    e.attrs['icon'] = "icon-" + e.attrs['icon']
                                elif "ion" in e.attrs:
                                    e.attrs['icon'] = e.attrs['ion']
                                    del e['ion']
                                elif "f7" in e.attrs:
                                    e.attrs['icon'] = e.attrs['f7']
                                    del e['f7']
                                elif "material" in e.attrs:
                                    e.attrs['icon'] = e.attrs['material']
                                    del e['material']
                                elif "fa" in e.attrs:
                                    e.attrs['icon'] = e.attrs['fa']
                                    del e['fa']
                            c.attrs = {**c.attrs, **e.attrs}
                            rem=e.unwrap()

            center=par.find_all(attrs={'class':'center'})
            if center:
                for c in center:
                    c.name="f7-nav-center"
                    cls = c.attrs['class']
                    cls.remove("center")
                    if len(cls)<1:
                        del c['class']
            right = par.find_all(attrs={'class': 'right'})
            if right:
                for c in right:
                    c.name = "f7-nav-right"
                    cls = c.attrs['class']
                    cls.remove("right")
                    if len(cls) < 1:
                        del c['class']
                    elem = c.find_all("f7-link")
                    if elem:
                        for e in elem:
                            if "back" in e.attrs:
                                if "text" in e.attrs:
                                    e.attrs['back-link'] = e.attrs['text']
                                    del e['text']
                                else:
                                    e.attrs['back-link'] = ""
                                del e['back']
                            else:
                                if "icon" in e.attrs:
                                    e.attrs['icon'] = "icon-" + e.attrs['icon']
                                elif "ion" in e.attrs:
                                    e.attrs['icon'] = e.attrs['ion']
                                    del e['ion']
                                elif "f7" in e.attrs:
                                    e.attrs['icon'] = e.attrs['f7']
                                    del e['f7']
                                elif "material" in e.attrs:
                                    e.attrs['icon'] = e.attrs['material']
                                    del e['material']
                                elif "fa" in e.attrs:
                                    e.attrs['icon'] = e.attrs['fa']
                                    del e['fa']
                            c.attrs = {**c.attrs, **e.attrs}
                            rem=e.unwrap()
            rem = d.unwrap()
    docs=soup.find_all(attrs={'class':'toolbar-inner'})
    if docs:
        for d in docs:
            rem=d.unwrap()
    docs=soup.find_all("f7-toolbar")
    if docs:
        for d in docs:
            if "class" in d.attrs:
                cls=d.attrs['class']
                if "toolbar-bottom" in cls:
                    cls.remove("toolbar-bottom")
                    d.attrs['bottom']=""
                if "tabbar" in cls:
                    cls.remove("tabbar")
                    d.attrs['tabbar'] = ""
                if "tabbar-labels" in cls:
                    cls.remove("tabbar-labels")
                    d.attrs['labels'] = ""
                if "tabbar-scrollable" in cls:
                    cls.remove("tabbar-scrollable")
                    d.attrs['scrollable'] = ""
                if len(cls)<1:
                    del d['class']
    docs=soup.find_all(attrs={'class':'tabs-animated-wrap'})
    if docs:
        for d in docs:
            elem=d.find_all("f7-tabs")
            if elem:
                for e in elem:
                    e.attrs['animated']=""
                    rem = d.unwrap()
    docs = soup.find_all(attrs={'class': 'tabs-swipeable-wrap'})
    if docs:
        for d in docs:
            elem = d.find_all("f7-tabs")
            if elem:
                for e in elem:
                    e.attrs['swipeable'] = ""
                    rem = d.unwrap()

    return soup
def pageinit(soup):
    docs=soup.find_all(attrs={'class':'page-content'})
    if docs:
        for d in docs:
            if "class" in d.attrs:
                if "hide-bars-on-scroll" in d.attrs['class']:
                    cls = d.attrs['class']
                    cls.remove("hide-bars-on-scroll")
                    par = d.parent
                    while par.parent:
                        if par.name == "f7-page":
                            break
                        else:
                            par = par.parent
                    par.attrs['hide-bars-on-scroll'] = ""
                if "hide-navbar-on-scroll" in d.attrs['class']:
                    cls = d.attrs['class']
                    cls.remove("hide-navbar-on-scroll")
                    par = d.parent
                    while par.parent:
                        if par.name == "f7-page":
                            break
                        else:
                            par = par.parent
                    par.attrs['hide-navbar-on-scroll'] = ""
                if "hide-toolbar-on-scroll" in d.attrs['class']:
                    cls = d.attrs['class']
                    cls.remove("hide-toolbar-on-scroll")
                    par = d.parent
                    while par.parent:
                        if par.name == "f7-page":
                            break
                        else:
                            par = par.parent
                    par.attrs['hide-toolbar-on-scroll'] = ""
                if "hide-tabbar-on-scroll" in d.attrs['class']:
                    cls = d.attrs['class']
                    cls.remove("hide-tabbar-on-scroll")
                    par = d.parent
                    while par.parent:
                        if par.name == "f7-page":
                            break
                        else:
                            par = par.parent
                    par.attrs['hide-tabbar-on-scroll'] = ""
    docs=soup.find_all(attrs={'class':'page-content'})
    if docs:
        for d in docs:
            if "class" in d.attrs:

                if d.name=="f7-tab":
                    d.name = "f7-page-content"
                    cls = d.attrs['class']
                    cls.remove("page-content")
                    if len(cls)<1:
                        del d['class']
                    par = d.parent
                    while par.parent:
                        if par.name == "f7-page":
                            break
                        else:
                            par = par.parent
                    par.attrs['tabs'] = ""
                    par.attrs['no-page-content']=""
                elif "pull-to-refresh-content" in d.attrs['class']:
                    par=d.parent
                    while par.parent:
                        if par.name=="f7-page":
                            break
                        else:
                            par=par.parent
                    par.attrs['pull-to-refresh']=""
                    par.attrs['@ptr:refresh']="onRefresh"
                    if "data-ptr-distance" in d.attrs:
                        d.attrs['pull-to-refresh-distance']=d.attrs['data-ptr-distance']
                        del d['data-ptr-distance']
                    elem=d.find_all(attrs={'class':'pull-to-refresh-layer'})
                    if elem:
                        for e in elem:
                            rem = e.unwrap()
                    elem = d.find_all("f7-preloader")
                    if elem:
                        for e in elem:
                            rem = e.unwrap()
                    elem = d.find_all(attrs={'class': 'pull-to-refresh-arrow'})
                    if elem:
                        for e in elem:
                            rem = e.unwrap()
                    rem = d.unwrap()
                elif "infinite-scroll" in d.attrs['class']:
                    if "data-distance" in d.attrs:
                        d.attrs['infinite-scroll-distance'] = d.attrs['data-distance']
                        del d['data-ptr-distance']
                    par = d.parent
                    while par.parent:
                        if par.name == "f7-page":
                            break
                        else:
                            par = par.parent
                    par.attrs['infinite-scroll'] = ""
                    par.attrs['@infinite'] = "onInfiniteScroll"
                    elem = d.find_all(attrs={'class': 'infinite-scroll-preloader'})
                    if elem:
                        for e in elem:
                            rem = e.unwrap()
                    elem = d.find_all("f7-preloader")
                    if elem:
                        for e in elem:
                            rem = e.unwrap()
                    rem = d.unwrap()
                elif "messages-content" in d.attrs['class']:
                    par = d.parent
                    while par.parent:
                        if par.name == "f7-page":
                            break
                        else:
                            par = par.parent
                    par.attrs['messages'] = ""
                elif "login-screen-content" in d.attrs['class']:
                    par = d.parent
                    while par.parent:
                        if par.name == "f7-page":
                            break
                        else:
                            par = par.parent
                    par.attrs['login-screen'] = ""

                else:
                    rem=d.unwrap()

    return soup
def swiperinit(soup):
    docs=soup.find_all("f7-swiper")
    if docs:
        for d in docs:
            dlist = list(d.attrs.keys())
            str1=""
            for i in dlist:
                if i.find("data-")>-1:
                    str1=str1+i[5:]+":"+d.attrs[i]+", "
                    del d[i]
            if str1.strip()!="":
                str1="{"+str1[:-2]+"}"
                d.attrs[':params']=str1

    return soup
def timelineinit(soup):
    docs = soup.find_all("f7-timeline-year")
    if docs:
        for d in docs:
            elem = d.find_all(attrs={'class':'timeline-year-title'})
            if elem:
                for e in elem:
                    d.attrs['title']=e.get_text().strip()
                    e.clear()
                    rem = e.unwrap()
    docs = soup.find_all("f7-timeline-month")
    if docs:
        for d in docs:
            elem = d.find_all(attrs={'class': 'timeline-month-title'})
            if elem:
                for e in elem:
                    d.attrs['title'] = e.get_text().strip()
                    e.clear()
                    rem = e.unwrap()
            item = d.find_all("f7-timeline-item")
            if item:
                for i in item:
                    elem = i.find_all(attrs={'class': 'timeline-item-date'})
                    if elem:
                        for e in elem:
                            i.attrs['date'] = e.get_text().strip()
                            e.clear()
                            rem = e.unwrap()
    docs = soup.find_all("f7-timeline")
    if docs:
        for d in docs:
            if "class" in d.attrs:
                cls=d.attrs['class']
                if "timeline-sides" in cls:
                    cls.remove("timeline-sides")
                    d.attrs['sides']=""
                if "timeline-horizontal" in cls:
                    cls.remove("timeline-horizontal")
                    d.attrs['horizontal']=""
                if "tablet-sides" in cls:
                    cls.remove("tablet-sides")
                    d.attrs['tablet-sides']=""
                for i in cls:
                    if i.find("col-")>-1:
                        d.attrs['col']=i[4:]
                        cls.remove(i)
                for i in cls:
                    if i.find("tablet-") > -1:
                        d.attrs['tablet-col']=i[7:]
                        cls.remove(i)
                if len(cls)<1:
                    del d['class']
    docs = soup.find_all(attrs={'class':'timeline-item-date'})
    if docs:
        for d in docs:
            par = d.parent
            while par:
                if par.name=="f7-timeline-item":
                    break
                else:
                    par = par.parent
            cls=d.attrs['class']
            cls.remove("timeline-item-date")
            if len(cls) < 1:
                del d['class']
            month=d.find("small")
            if month:
                m=month.get_text().strip()
                if m!="":
                    par.attrs['month']=m
                    month.clear()
                    rem = month.unwrap()
                    day = d.get_text().strip()
                    if day!="":
                        par.attrs['day']=day
                        d.clear()
                        rem = d.unwrap()
            div=par.find_all(attrs={'class':'timeline-item-divider'})
            if div:
                for n in div:
                    rem = n.unwrap()
            div = par.find_all(attrs={'class': 'timeline-item-inner'})
            if div:
                if len(div)<2:
                    rem = div[0].unwrap()
                    par.attrs['inner']=""
                else:
                    for n in div:
                        n.name="f7-timeline-item-child"
                        cls=n.attrs['class']
                        cls.remove("timeline-item-inner")
                        if len(cls)<1:
                            del n['class']
                        time = n.find_all(attrs={'class': 'timeline-item-time'})
                        if time:
                            for t in time:
                                x = t.get_text().strip()
                                t.clear()
                                rem = t.unwrap()
                                n.attrs['time'] = x
                        title = n.find_all(attrs={'class': 'timeline-item-title'})
                        if title:
                            for t in title:
                                x = t.get_text().strip()
                                t.clear()
                                rem = t.unwrap()
                                n.attrs['title'] = x
                        subtitle = n.find_all(attrs={'class': 'timeline-item-subtitle'})
                        if subtitle:
                            for t in subtitle:
                                x = t.get_text().strip()
                                t.clear()
                                rem = t.unwrap()
                                n.attrs['subtitle'] = x
                        text = n.find_all(attrs={'class': 'timeline-item-text'})
                        if text:
                            for t in text:
                                x = t.get_text().strip()
                                t.clear()
                                rem = t.unwrap()
                                n.attrs['text'] = x
            time = par.find_all(attrs={'class': 'timeline-item-time'})
            if time:
                for t in time:
                    x = t.get_text().strip()
                    t.clear()
                    rem = t.unwrap()
                    par.attrs['time'] = x
            title = par.find_all(attrs={'class': 'timeline-item-title'})
            if title:
                for t in title:
                    x = t.get_text().strip()
                    t.clear()
                    rem = t.unwrap()
                    par.attrs['title'] = x
            subtitle = par.find_all(attrs={'class': 'timeline-item-subtitle'})
            if subtitle:
                for t in subtitle:
                    x = t.get_text().strip()
                    t.clear()
                    rem = t.unwrap()
                    par.attrs['subtitle'] = x
            text = par.find_all(attrs={'class': 'timeline-item-text'})
            if text:
                for t in text:
                    x = t.get_text().strip()
                    t.clear()
                    rem = t.unwrap()
                    par.attrs['text'] = x
            div = par.find_all(attrs={'class': 'timeline-item-content'})
            if div:
                for n in div:
                    inner=n.get_text().strip()
                    rem = n.unwrap()
                    if inner!="":
                        par.attrs['content']=inner
                        n.clear()



    return soup
def searchbarinit(soup):
    docs=soup.find_all(attrs={'class':'searchbar-input'})
    if docs:
        for d in docs:
            rem=d.unwrap()
    docs=soup.find_all("f7-searchbar")
    if docs:
        for d in docs:
            d.attrs['@searchbar:search'] = "onSearch"
            d.attrs['@searchbar:enable'] = "onEnable"
            d.attrs['@searchbar:disable'] = "onDisable"
            if "class" in d.attrs:
                cls=d.attrs['class']
                if "searchbar-init" in cls:
                    cls.remove("searchbar-init")
                    d.attrs[':init']="true"
                if len(cls)<1:
                    del d['class']
            if "data-search-list" in d.attrs:
                d.attrs['search-list']=d.attrs['data-search-list']
                del d['data-search-list']
            if "data-search-in" in d.attrs:
                d.attrs['search-in'] = d.attrs['data-search-in']
                del d['data-search-in']
            if "data-found" in d.attrs:
                d.attrs['found'] = d.attrs['data-found']
                del d['data-found']
            if "data-not-found" in d.attrs:
                d.attrs['not-found'] = d.attrs['data-not-found']
                del d['data-not-found']
            overlay=soup.find_all(attrs={'class':'searchbar-overlay'})
            if overlay:
                for o in overlay:
                    rem=o.unwrap()
                    d.attrs["overlay"]=""
            input=d.find_all("input",attrs={'type':'search'})
            if input:
                for inp in input:
                    if "placeholder" in inp.attrs:
                        d.attrs['placeholder']=inp.attrs['placeholder']
                    rem = inp.unwrap()
            s_clear=d.find_all(attrs={'class':'searchbar-clear'})
            if s_clear:
                for c in s_clear:
                    rem = c.unwrap()
                    d.attrs['clear-button']="true"
                    d.attrs['@searchbar:clear'] = "onClear"
            cancel = d.find_all(attrs={'class': 'searchbar-cancel'})
            if cancel:
                for c in cancel:
                    if c.get_text().strip()!="":
                        text=c.get_text().strip()
                        c.clear()
                    else:
                        text="Cancel"
                    d.attrs['cancel-link'] = text
                    rem = c.unwrap()


    return soup
def photoinit(soup):

    return soup
def vuefilter(soup):
    docs=soup.find_all(attrs={'class':'picker-modal-inner'})
    if docs:
        for d in docs:
            rem=d.unwrap()
    docs = soup.find_all(attrs={'class': 'popover-angle'})
    if docs:
        for d in docs:
            rem = d.unwrap()
    docs = soup.find_all(attrs={'class': 'popover-content'})
    if docs:
        for d in docs:
            rem = d.unwrap()
    docs = soup.find_all("f7-link")
    if docs:
        for d in docs:
            par=d.parent
            while not par:
                if par.name=="f7-buttons":
                    break
                else:
                    par=par.parent
            if par.name=="f7-buttons":
                d.name="f7-button"
    docs = soup.find_all("f7-progressbar")
    if docs:
        for d in docs:
            elem = d.find_all("span")
            if elem:
                for e in elem:
                    if not e.string:
                        rem = e.unwrap()
    docs = soup.find_all("script",attrs={'type':'text/template7'})
    if docs:
        for d in docs:
            d.name="t7-template"
            del d['type']
    docs = soup.find_all(attrs={'class':'sortable-handler'})
    if docs:
        for d in docs:
            rem=d.unwrap()

    soup=str(soup)
    soup=soup.replace("inset"+'=""',"inset")
    soup = soup.replace("tablet-inset" + '=""', "tablet-inset")
    soup = soup.replace("no-hairlines" + '=""', "no-hairlines")
    soup=soup.replace("inner"+'=""',"inner")
    soup = soup.replace("active" + '=""', "active")
    soup = soup.replace("big" + '=""', "big")
    soup = soup.replace("round" + '=""', "round")
    soup = soup.replace("raised" + '=""', "raised")
    soup = soup.replace("fill" + '=""', "fill")
    soup = soup.replace("back"+'=""',"back")
    soup = soup.replace("external" + '=""', "external")
    soup = soup.replace("force" + '="true"', "force")
    soup = soup.replace("reload" + '="true"', "reload")
    soup = soup.replace("deleteable"+'=""',"deleteable")
    soup = soup.replace("icon"+'=""',"icon")
    soup = soup.replace("no-gutter"+'=""',"no-gutter")
    soup = soup.replace("group-title" + '=""', "group-title")
    soup = soup.replace("media-list"+'=""',"media-list")
    soup = soup.replace("divider"+'=""',"divider")
    soup = soup.replace("accordion"+'=""',"accordion")
    soup = soup.replace("accordion-item"+'=""',"accordion-item")
    soup = soup.replace("contacts"+'=""',"contacts")
    soup = soup.replace("swipeout" + '=""', "swipeout")
    soup = soup.replace("right" + '=""', "right")
    soup = soup.replace("left" + '=""', "left")
    soup = soup.replace("delete" + '=""', "delete")
    soup = soup.replace("close" + '=""', "close")
    soup = soup.replace("open-panel"+'=""',"open-panel")
    soup = soup.replace("close-panel"+'=""',"close-panel")
    soup = soup.replace("open-popup"+'=""',"open-popup")
    soup = soup.replace("close-popup"+'=""',"close-popup")
    soup = soup.replace("open-popover"+'=""',"open-popover")
    soup = soup.replace("close-popover"+'=""',"close-popover")
    soup = soup.replace("open-picker"+'=""',"open-picker")
    soup = soup.replace("close-picker"+'=""',"close-picker")
    soup = soup.replace("open-login-screen"+'=""',"open-login-screen")
    soup = soup.replace("close-login-screen"+'=""',"close-login-screen")
    soup = soup.replace("open-sortable"+'=""',"open-sortable")
    soup = soup.replace("close-sortable"+'=""',"close-sortable")
    soup = soup.replace("toggle-sortable"+'=""',"toggle-sortable")
    soup = soup.replace("bold"+'=""',"bold")
    soup = soup.replace("tablet-fullscreen"+'=""',"tablet-fullscreen")
    soup = soup.replace("login-screen" + '=""', "login-screen")
    soup = soup.replace("form" + '=""',"form")
    soup = soup.replace("sliding"+'=""',"sliding")
    soup = soup.replace("back-link" + '=""', "back-link")
    soup = soup.replace("bottom"+'=""',"bottom")
    soup = soup.replace("tabbar"+'=""',"tabbar")
    soup = soup.replace("labels" + '=""', "labels")
    soup = soup.replace("scrollable" + '=""', "scrollable")
    soup = soup.replace("pull-to-refresh" + '=""', "pull-to-refresh")
    soup = soup.replace("infinite-scroll" + '=""', "infinite-scroll")
    soup = soup.replace("tabs" + '=""', "tabs")
    soup = soup.replace("no-page-content"+'=""',"no-page-content")
    soup = soup.replace("reveal" + '=""', "reveal")
    soup = soup.replace("cover" + '=""', "cover")
    soup = soup.replace("infinite"+'=""',"infinite")
    soup = soup.replace("scrollbar" + '=""', "scrollbar")
    soup = soup.replace("prev-button" + '=""', "prev-button")
    soup = soup.replace("next-button" + '=""', "next-button")
    soup = soup.replace("pagination" + '=""', "pagination")
    soup = soup.replace("zoom" + '=""', "zoom")
    soup = soup.replace("init" + '=""', "init")
    soup = soup.replace("navbar-fixed"+ '=""', "navbar-fixed")
    soup = soup.replace("navbar-through"+ '=""', "navbar-through")
    soup = soup.replace("toolbar-fixed"+ '=""', "toolbar-fixed")
    soup = soup.replace("toolbar-through"+ '=""', "toolbar-through")
    soup = soup.replace("tabbar-fixed"+ '=""', "tabbar-fixed")
    soup = soup.replace("tabbar-through"+ '=""', "tabbar-through")
    soup = soup.replace("tabbar-labels-fixed"+ '=""', "tabbar-labels-fixed")
    soup = soup.replace("tabbar-labels-through"+ '=""', "tabbar-labels-through")
    soup = soup.replace("cached" + '=""', "cached")
    soup = soup.replace("animated" + '=""', "animated")
    soup = soup.replace("swipeable" + '=""', "swipeable")
    soup = soup.replace("sides" + '=""', "sides")
    soup = soup.replace("horizontal" + '=""', "horizontal")
    soup = soup.replace("tablet-sides" + '=""', "tablet-sides")
    soup = soup.replace("main" + '=""', "main")
    soup = soup.replace("sortable" + '=""', "sortable")
    soup = soup.replace("overlay" + '=""', "overlay")
    soup = soup.replace("virtual" + '=""', "virtual")
    soup = soup.replace("media" + '=""', "media")
    soup = soup.replace("floating" + '=""', "floating")
    soup = soup.replace("value" + '=""', "")
    soup = soup.replace("radio" + '=""', "radio")
    soup = soup.replace("checkbox" + '=""', "checkbox")
    soup = soup.replace("checked" + '=""', "checked")
    soup = soup.replace("selected" + '=""', "selected")
    soup = soup.replace("smart-select" + '=""', "smart-select")


    soup = soup.replace(" style" + '=""', "")
    soup = soup.replace(" ="+'""', "")
    soup=unescape(soup)
    soup=re.sub('[\n]+', '\n',soup)
    if soup.find("<template")<-1 and soup.find("</template>")<-1:
        soup="<template>\n"+soup+"\n</template>"
    return soup
def f7update(path):
    code_file = open(path, "r", encoding='utf-8')
    code = code_file.read()
    code_file.close()
    soup = BeautifulSoup(code, "html.parser")
    soup = colorattr(soup, "pages")
    soup = colorattr(soup, "page")
    soup = colorattr(soup, "badge")
    soup = colorattr(soup, "link")
    soup = colorattr(soup, "preloader")
    soup = colorattr(soup, "progressbar")
    soup = colorattr(soup, "actions-modal-button")
    soup = colorattr(soup, "popup")
    soup = colorattr(soup, "picker-modal")
    soup = colorattr(soup, "navbar")
    soup = colorattr(soup, "toolbar")
    soup = colorattr(soup, "panel")
    soup = colorattr(soup, "view")
    soup = colorattr(soup, "views")
    soup = f7tovue(soup, "searchbar", "f7-searchbar")
    soup = f7tovue(soup, "statusbar", "f7-statusbar")

    soup = addattr(soup, "content-block", "f7-block", "inset")
    soup = addattr(soup, "content-block", "f7-block", "tablet-inset")
    soup = addattr(soup, "content-block", "f7-block", "no-hairlines")
    soup = renattr(soup, "views", "class", "navbar-fixed", "navbar-fixed")
    soup = renattr(soup, "views", "class", "navbar-through", "navbar-through")
    soup = renattr(soup, "views", "class", "toolbar-fixed", "toolbar-fixed")
    soup = renattr(soup, "views", "class", "toolbar-through", "toolbar-through")
    soup = renattr(soup, "views", "class", "tabbar-fixed", "tabbar-fixed")
    soup = renattr(soup, "views", "class", "tabbar-through", "tabbar-through")
    soup = renattr(soup, "views", "class", "tabbar-labels-fixed", "tabbar-labels-fixed")
    soup = renattr(soup, "views", "class", "tabbar-labels-through", "tabbar-labels-through")
    soup = renattr(soup, "views", "class", "tabs", "tabs")
    soup = renattr(soup, "view", "class", "navbar-fixed", "navbar-fixed")
    soup = renattr(soup, "view", "class", "navbar-through", "navbar-through")
    soup = renattr(soup, "view", "class", "toolbar-fixed", "toolbar-fixed")
    soup = renattr(soup, "view", "class", "toolbar-through", "toolbar-through")
    soup = renattr(soup, "view", "class", "tabbar-fixed", "tabbar-fixed")
    soup = renattr(soup, "view", "class", "tabbar-through", "tabbar-through")
    soup = renattr(soup, "view", "class", "tabbar-labels-fixed", "tabbar-labels-fixed")
    soup = renattr(soup, "view", "class", "tabbar-labels-through", "tabbar-labels-through")
    soup = renattr(soup, "view", "class", "tab", "tab")
    soup = renattr(soup, "view", "class", "view-main", "main")
    soup = renattr(soup, "view", "class", "active", "active")
    soup = renattr(soup, "list-block", "class", "virtual-list", "virtual")

    soup = renattr(soup, "pages", "class", "navbar-fixed", "navbar-fixed")
    soup = renattr(soup, "pages", "class", "navbar-through", "navbar-through")
    soup = renattr(soup, "pages", "class", "toolbar-fixed", "toolbar-fixed")
    soup = renattr(soup, "pages", "class", "toolbar-through", "toolbar-through")
    soup = renattr(soup, "pages", "class", "tabbar-fixed", "tabbar-fixed")
    soup = renattr(soup, "pages", "class", "tabbar-through", "tabbar-through")
    soup = renattr(soup, "pages", "class", "tabbar-labels-fixed", "tabbar-labels-fixed")
    soup = renattr(soup, "pages", "class", "tabbar-labels-through", "tabbar-labels-through")
    soup = renattr(soup, "page", "class", "navbar-fixed", "navbar-fixed")
    soup = renattr(soup, "page", "class", "navbar-through", "navbar-through")
    soup = renattr(soup, "page", "class", "toolbar-fixed", "toolbar-fixed")
    soup = renattr(soup, "page", "class", "toolbar-through", "toolbar-through")
    soup = renattr(soup, "page", "class", "tabbar-fixed", "tabbar-fixed")
    soup = renattr(soup, "page", "class", "tabbar-through", "tabbar-through")
    soup = renattr(soup, "page", "class", "tabbar-labels-fixed", "tabbar-labels-fixed")
    soup = renattr(soup, "page", "class", "tabbar-labels-through", "tabbar-labels-through")
    soup = renattr(soup, "page", "class", "cached", "cached")
    soup = renattr(soup, "page", "class", "no-swipeback", "no-swipeback")
    soup = renattr(soup, "panel", "class", "panel-left", "left")
    soup = renattr(soup, "panel", "class", "panel-right", "right")
    soup = renattr(soup, "panel", "class", "panel-reveal", "reveal")
    soup = renattr(soup, "panel", "class", "panel-cover", "cover")
    soup = renattr(soup, "timeline-item", "class", "timeline-item-right", "right")
    soup = renattr(soup, "timeline-item", "class", "timeline-item-left", "left")

    soup = renattr(soup, "button", "class", "button-big", "big")
    soup = renattr(soup, "button", "class", "button-round", "round")
    soup = renattr(soup, "button", "class", "button-raised", "raised")
    soup = renattr(soup, "button", "class", "button-fill", "fill")
    soup = renattr(soup, "row", "class", "no-gutter", "no-gutter")
    soup = renattr(soup, "progressbar", "class", "progressbar-infinite", "infinite")
    soup = renattr(soup, "popup", "class", "swiper-zoom", "zoom")

    soup = renattr(soup, "actions-modal-button", "class", "actions-modal-button-bold", "bold")
    soup = renattr(soup, "popup", "class", "tablet-fullscreen", "tablet-fullscreen")
    soup = innerattr(soup, "content-block", "content-block-inner", "f7-block inner")
    soup = addattr(soup, "tab", "f7-tab", "active")
    soup = addattr(soup, "button", "f7-button", "active")
    soup = renattr(soup, "swiper-container", "class", "swiper-init", "init")

    soup = colorattr(soup, "button")
    soup = changeattrname(soup, "a", "data-tab", "tab-link")
    soup = changeattrname(soup, "a", "data-view", "view")
    soup = addattr(soup, "link", "f7-link", "external")
    soup = addattr(soup, "link", "f7-link", "back")
    soup = changeattrname(soup, "a", "data-force", "force")
    soup = changeattrname(soup, "span", "data-progress", ":progress")

    soup = changeattrname(soup, "a", "data-reload", "reload")
    soup = changeattrname(soup, "a", "data-animate-pages", ":animate-pages")
    soup = changeattrname(soup, "a", "data-ignore-cache", ":ignore-cache")
    soup = changeattrname(soup, "div", "data-page", "name")
    soup = changeattrname(soup, "a", "data-template", "template")
    soup = extattr(soup, "no-fastclick", "f7-link", ":no-fast-click")
    soup = checkcardinner(soup)
    soup = innerattr(soup, "card-content", "card-content-inner", "card-content ")
    soup = innerattr(soup, "swiper-container", "swiper-pagination", "f7-swiper pagination")
    soup = innerattr(soup, "swiper-container", "swiper-scrollbar", "f7-swiper scrollbar")
    soup = innerattr(soup, "swiper-container", "swiper-button-next", "f7-swiper next-button")
    soup = innerattr(soup, "swiper-container", "swiper-button-prev", "f7-swiper prev-button")
    soup = innerattr(soup, "swiper-slide", "swiper-zoom-container", "f7-swiper-slide zoom")

    soup = chipinit(soup)
    soup = fabinit(soup)
    soup = iconinit(soup)
    soup = gridinit(soup)
    soup = forminit(soup)
    soup = listinit(soup)

    soup = addattr(soup, "media-list", "f7-list", "media-list")
    soup = addattr(soup, "sortable", "f7-list", "sortable")
    soup = addattr(soup, "store-data", "f7-list", "store-data")
    soup = addattr(soup, "no-hairlines", "f7-list", "no-hairlines")
    soup = addattr(soup, "no-hairlines-between", "f7-list", "no-hairlines-between")
    soup = addattr(soup, "item-divider", "f7-list-item", "divider")
    soup = addattr(soup, "virtual-list", "f7-list", "virtual")

    soup = f7tovue(soup, "accordion-list", "f7-accordion")
    soup = f7tovue(soup, "accordion-item", "f7-accordion-item")
    soup = f7tovue(soup, "accordion-item-toggle", "f7-accordion-toggle")
    soup = f7tovue(soup, "accordion-item-content", "f7-accordion-content")
    soup = f7tovue(soup, "badge", "f7-badge")
    soup = f7tovue(soup, "content-block-title", "f7-block-title")
    soup = f7tovue(soup, "content-block", "f7-block")
    soup = f7tovue(soup, "list-block", "f7-list")
    soup = f7tovue(soup, "buttons-row", "f7-buttons")
    soup = f7tovue(soup, "button", "f7-button")
    soup = f7tovue(soup, "tabs", "f7-tabs")
    soup = f7tovue(soup, "tab", "f7-tab")
    soup = f7tovue(soup, "tab-link", "f7-link")
    soup = f7tovue(soup, "card", "f7-card")
    soup = f7tovue(soup, "card-header", "f7-card-header")
    soup = f7tovue(soup, "card-content", "f7-card-content")
    soup = f7tovue(soup, "card-footer", "f7-card-footer")
    soup = f7tovue(soup, "chip", "f7-chip")
    soup = f7tovue(soup, "floating-action-button", "f7-fab")
    soup = f7tovue(soup, "speed-dial", "f7-fab-speed-dial")
    soup = f7tovue(soup, "speed-dial-buttons", "f7-fab-actions")
    soup = f7tovue(soup, "icon", "f7-icon")
    soup = f7tovue(soup, "row", "f7-grid")
    soup = f7tovue(soup, "list-block", "f7-list")
    soup = f7tovue(soup, "list-block-group", "f7-list-group")
    soup = f7tovue(soup, "list-block-label", "f7-list-label")
    soup = f7tovue(soup, "messages", "f7-messages")
    soup = f7tovue(soup, "message", "f7-message")
    soup = f7tovue(soup, "messagebar", "f7-messagebar")
    soup = f7tovue(soup, "actions-modal", "f7-actions")
    soup = f7tovue(soup, "actions-modal-group", "f7-actions-group")
    soup = f7tovue(soup, "actions-modal-label", "f7-actions-label")
    soup = f7tovue(soup, "actions-modal-button", "f7-actions-button")
    soup = f7tovue(soup, "login-screen", "f7-login-screen")
    soup = f7tovue(soup, "picker-modal", "f7-picker-modal")
    soup = f7tovue(soup, "popover", "f7-popover")
    soup = f7tovue(soup, "popup", "f7-popup")
    soup = f7tovue(soup, "navbar", "f7-navbar")
    soup = f7tovue(soup, "toolbar", "f7-toolbar")
    soup = f7tovue(soup, "subnavbar", "f7-subnavbar")
    soup = f7tovue(soup, "pages", "f7-pages")
    soup = f7tovue(soup, "page", "f7-page")
    soup = f7tovue(soup, "panel", "f7-panel")
    soup = f7tovue(soup, "preloader", "f7-preloader")
    soup = f7tovue(soup, "progressbar", "f7-progressbar")
    soup = f7tovue(soup, "searchbar", "f7-searchbar")
    soup = f7tovue(soup, "statusbar-overlay", "f7-statusbar")
    soup = f7tovue(soup, "swiper-container", "f7-swiper")
    soup = f7tovue(soup, "swiper-slide", "f7-swiper-slide")
    soup = f7tovue(soup, "tabs", "f7-tabs")
    soup = f7tovue(soup, "tab", "f7-tab")
    soup = f7tovue(soup, "timeline", "f7-timeline")
    soup = f7tovue(soup, "timeline-item", "f7-timeline-item")
    soup = f7tovue(soup, "timeline-year", "f7-timeline-year")
    soup = f7tovue(soup, "timeline-month", "f7-timeline-month")
    soup = f7tovue(soup, "views", "f7-views")
    soup = f7tovue(soup, "view", "f7-view")
    soup = f7tovue(soup, "login-screen-title", "f7-login-screen-title")

    soup = messageinit(soup)
    soup = listfilter(soup)
    soup = linkinit(soup)
    soup = logininit(soup)
    soup = barinit(soup)
    soup = pageinit(soup)
    soup = swiperinit(soup)
    soup = searchbarinit(soup)
    soup = photoinit(soup)
    soup = timelineinit(soup)
    s1 = vuefilter(soup)
    return s1
#"""
#path="C:\\Users\\Administrator\\Desktop\\f7-final-test\\v2-test\\f7-test\\timeline-vertical.html"
#s1=f7update(path)
#print(s1)
#"""