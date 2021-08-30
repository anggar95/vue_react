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
            if old in cls:
                cls.remove(old)
            if new in cls:
                cls.remove(new)
            if len(cls) < 1:
                del d['class']
            d.attrs[new]=""
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
    if attr=="name":
        docs = soup.find_all(elem)
    else:
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
def iconinit(soup):
    docs = soup.find_all(attrs={'class':'icon'})
    if docs:
        soup=colorattr(soup,"icon")
        for d in docs:
            badge=d.find("f7-badge")
            if badge:
                badgetxt=len(badge.get_text().strip())
            else:
                badgetxt=0
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
                f7=d.get_text().strip()
                d.attrs['f7']=f7[:len(f7)-badgetxt]
                cls.remove('f7-icons')
            if "material-icons" in cls:
                md=d.get_text().strip()
                d.attrs['material']=md[:len(md)-badgetxt]
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
                    d.attrs['icon'] = c
                    cls.remove(c)
            if len(d.attrs['class'])<0:
                del d['class']
            d.clear()
    return soup
def delinner(soup,inner):
    docs = soup.find_all(attrs={'class':inner})
    if docs:
        for d in docs:
            cls=d.attrs['class']
            cls.remove(inner)
            if len(cls)<1:
                del d['class']
            par=d.findParent()
            if par:
                par.attrs=dict(d.attrs,**par.attrs)
            rem=d.unwrap()


    return soup
def navbarinit(soup):
    docs = soup.find_all("f7-navbar")
    if docs:
        for d in docs:
            back=d.find(attrs={'class':'back'})
            if back:
                d.attrs['back-link']=back.get_text().strip()
                if "href" in back.attrs:
                    d.attrs['back-link-url']=back.attrs['href']
                back.clear()
                rem=back.unwrap()
            left = d.find(attrs={'class':'left'})
            if left:
                if not "sliding" in left.attrs['class']:
                    d.attrs['sliding']="false"
                if left.get_text().strip()=="":
                    rem=left.unwrap()

            title=d.find(attrs={"class":'title'})
            if title:
                if d.find("f7-link") or d.find(attrs={'class':'button'}):
                    title.name="f7-nav-title"
                    cls = title.attrs['class']
                    cls.remove("title")
                    if len(cls)<1:
                        del title['class']
                else:
                    d.attrs['title']=title.get_text().strip()
                    title.clear()
                    rem = title.unwrap()
            right=d.find(attrs={'class':'right'})
            if right:
                link=d.find("f7-link")
                if link:
                    if "class" in link.attrs:
                        if "panel-open" in link.attrs['class']:
                            link.attrs['panel-open']="right"
                            cls=link.attrs['class']
                            cls.remove("panel-open")
                            for c in cls:
                                if c.find("icon")>-1:
                                    cls.remove(c)
                                    icon=link.find(attrs={'class':'icon'})
                                    if icon:
                                        icls=icon.attrs['class']
                                        if "f7-icons" in icls:
                                            link.attrs['icon-f7']=icon.get_text().strip()
                                        elif "fa" in icls:
                                            link.attrs['icon-fa'] = icon.get_text().strip()
                                        elif "ion" in icls:
                                            link.attrs['icon-ion'] = icon.get_text().strip()
                                        else:
                                            link.attrs['icon'] = icon.get_text().strip()
                                        icon.clear()
                                        rem=icon.unwrap()
                            if len(cls)<1:
                                del link['class']
                    right.name = "f7-nav-right"
                    cls=right.attrs['class']
                    cls.remove("right")
                    if len(cls)<1:
                        del right['class']
            sliding=d.find_all(attrs={'class':'sliding'})
            if sliding:
                for slide in sliding:
                    cls=slide.attrs['class']
                    cls.remove("sliding")
                    if len(cls)<1:
                        del slide['class']
    return soup
def linkinit(soup):

    return soup
def wrapelement(soup,child,childattr,newfathername):
    if childattr=="name":
        elem = soup.find_all(child)
    else:
        elem = soup.find_all(attrs={childattr: child})
    if elem:
        for s in elem:
            par = s.parent
            if par.name!=newfathername:
                obj = bs4.element.Tag(name=newfathername)
                s.wrap(obj)
    return soup
def accordioninit(soup):
    docs=soup.find_all(attrs={'class':'list accordion-list'})
    if docs:
        for d in docs:
            cls=d.attrs['class']
            cls.remove("accordion-list")
            cls.remove("list")
            d.name="f7-list"
            d.attrs['accordion-list']=""
            if len(cls)<1:
                del d['class']
    for docs in soup.find_all("f7-list-item"):
        if "accordion-item" in docs.attrs:
            for link in docs.find_all(attrs={'class':'item-link'}):
                link.unwrap()
            for inner in docs.find_all(attrs={'class': 'item-inner'}):
                inner.unwrap()
            title=docs.find(attrs={'class': 'item-title'})
            if title:
                docs.attrs['title']=title.get_text().strip()
                title.clear()
                title.unwrap()

    return soup
def smartinit(soup):
    soup = colorattr(soup,"list-button")
    soup = f7tovue(soup,"list-button","f7-list-button")

    labels = "false"
    for d in soup.find_all(attrs={'class':'smart-select'}):
        if d.name!="f7-list":
            par=d.parent
            while par:
                if par.name=="f7-list":
                    break
                par=par.parent
            par.attrs['smart-select'] = ""
        cls = d.attrs['class']
        cls.remove("smart-select")
        d.attrs['smart-select'] = ""
        if len(cls) < 1:
            del d['class']
    for d in soup.find_all("f7-list"):
        for ul in d.find_all("ul"):
            ul.unwrap()
        if d.find(attrs={'class': 'inline-label'}):
            d.attrs['inline-labels'] = ""
            labels = "true"
        if "class" in d.attrs:
            cls = d.attrs['class']
            if "contacts-block" in cls:
                cls.remove("contacts-block")
                d.attrs['contacts-list'] = ""
            if "contacts-list" in cls:
                cls.remove("contacts-list")
                d.attrs['contacts-list'] = ""
            if "media-list" in cls:
                cls.remove("media-list")
                d.attrs['media-list'] = ""
            if "virtual-list" in cls:
                cls.remove("virtual-list")
                d.attrs['virtual-list'] = ""

            if len(cls) < 1:
                del d['class']
        for li in d.find_all("li"):
            li.name = "f7-list-item"
            for i in li.find_all(attrs={'class': 'icon'}):
                i.attrs['slot'] = "media"
            for i in li.find_all("img"):
                i.attrs['slot'] = "media"
            if "class" in li.attrs:
                cls=li.attrs['class']
                if "item-content" in cls:
                    cls.remove("item-content")
                if len(cls)<1:
                    del li['class']
            if labels=="true":
                for label in li.find_all(attrs={'class': 'item-label'}):
                    li.attrs['label'] = label.get_text().strip()
                    label.clear()
                    label.unwrap()
            title = li.find(attrs={'class': 'item-title'})
            if title:
                li.attrs['title'] = title.get_text().strip()
                title.clear()
                title.unwrap()
            link = li.find(attrs={'class': 'item-link'})
            if link:
                cls = link.attrs['class']
                if link.name != "f7-list-button":
                    cls.remove("item-link")
                    if len(cls) < 1:
                        del link['class']
                    if "href" in link.attrs:
                        # if link.attrs['href']!="#":
                        li.attrs['link'] = link.attrs['href']
                        del link['href']
                    li.attrs=dict(li.attrs,**link.attrs)
                    link.unwrap()
                else:
                    cls.remove("item-link")
                    if len(cls) < 1:
                        del link['class']
                    li.attrs=dict(li.attrs,**link.attrs)
    for d in soup.find_all("f7-list"):
        if "smart-select" in d.attrs:
            for li in d.find_all("f7-list-item"):
                if "link" in li.attrs:
                    del li['link']
                li.attrs['smart-select']=""
                del d['smart-select']
    for btn in soup.find_all("f7-list-button"):
        item=btn.findParent("f7-list-item")
        if item:
            btn.attrs=dict(btn.attrs,**item.attrs)
            item.unwrap()



    return soup

def listinit(soup):
    for d in soup.find_all(attrs={'class':'sortable'}):
        if d.name!="f7-list":
            par=d.parent
            while par:
                if par.name=="f7-list":
                    break
                par=par.parent
            par.attrs['sortable'] = ""
        cls = d.attrs['class']
        cls.remove("sortable")
        d.attrs['sortable']=""
        if len(cls)<1:
            del d['class']

    for l in soup.find_all("f7-list-item"):

        for textarea in l.find_all("textarea"):
            l.name="f7-list-input"
            l.attrs['type']="textarea"
            if "class" in textarea.attrs:
                if "resizable" in textarea.attrs['class']:
                    l.attrs['resizable']=""
            textarea.clear()
            textarea.unwrap()
        for sel in l.find_all("select"):
            if "smart-select" not in l.attrs:
                sel.name="f7-list-input"
                sel.attrs['type']="select"
            if "label" in l.attrs:
                sel.attrs['label'] = l.attrs['label']
                del l['label']
        for badge in l.find_all("f7-badge"):
            if "color" in badge.attrs:
                l.attrs['badge-color']=badge.attrs['color']
            l.attrs['badge']=badge.get_text().strip()
            badge.clear()
            badge.unwrap()
        for after in l.find_all(attrs={'class':'item-after'}):
            if after.get_text().strip()!="":
                l.attrs['after']=after.get_text().strip()
                after.clear()
            after.unwrap()
        for subtitle in l.find_all(attrs={'class': 'item-subtitle'}):
            l.attrs['subtitle'] = subtitle.get_text().strip()
            subtitle.clear()
            subtitle.unwrap()
        for text in l.find_all(attrs={'class': 'item-text'}):
            l.attrs['text'] = text.get_text().strip()
            text.clear()
            text.unwrap()
        for header in l.find_all(attrs={'class': 'item-header'}):
            l.attrs['header'] = header.get_text().strip()
            header.clear()
            header.unwrap()
        for footer in l.find_all(attrs={'class': 'item-footer'}):
            l.attrs['footer'] = footer.get_text().strip()
            footer.clear()
            footer.unwrap()
        for inp in l.find_all(attrs={'class':'item-input'}):
            l.attrs=dict(l.attrs,**inp.attrs)
            inp.unwrap()
        for i in l.find_all("input"):
            i.name="f7-list-input"
            if "label" in l.attrs:
                i.attrs['label']=l.attrs['label']
                del l['label']
        if "class" in l.attrs:
            cls=l.attrs['class']
            if "list-group-title" in cls:
                cls.remove("list-group-title")
                l.attrs['group-title']=""
                if l.get_text().strip()!="":
                    l.attrs['title']=l.get_text().strip()
                    l.clear()
            if len(cls)<1:
                del l['class']
    for li in soup.find_all("f7-list-item"):
        if "class" in li.attrs:
            cls=li.attrs['class']
            if "item-content" in cls:
                cls.remove("item-content")
            if "item-input" in cls:
                cls.remove("item-input")
            if len(cls)<1:
                del li['class']
    for toggle in soup.find_all(attrs={'class':"toggle"}):
        for inp in toggle.find_all("input"):
            inp.name="f7-toggle"
        for i in toggle.find_all("f7-list-input"):
            i.name = "f7-toggle"
            i.attrs['slot']="input"
            if 'type' in i.attrs:
                del i['type']
    s=str(soup).replace("</f7-list-input></f7-list-item>","</f7-toggle></f7-list-item>")
    soup=BeautifulSoup(s,"lxml")
    for toggle in soup.find_all("f7-toggle"):
        par = toggle.findParent("f7-list-item")
        if par:
            par.name="f7-list-input"
            par.attrs[':input']="false"
            if "label" in toggle.attrs:
                par.attrs['label'] = toggle.attrs['label']
                del toggle['label']
    for toggle in soup.find_all(attrs={'class':'toggle-icon'}):
        toggle.clear()
        toggle.unwrap()
    for slider in soup.find_all("f7-list-input"):
        if "type" in slider.attrs:
            if slider.attrs['type']=="range":
                del slider['type']
                if "min" in slider.attrs:
                    slider.attrs[':min']=slider.attrs['min']
                    del slider['min']
                if "max" in slider.attrs:
                    slider.attrs[':max']=slider.attrs['max']
                    del slider['max']
                if "step" in slider.attrs:
                    slider.attrs[':step']=slider.attrs['step']
                    del slider['step']
                if "value" in slider.attrs:
                    slider.attrs[':value']=slider.attrs['value']
                    del slider['value']

                obj = bs4.element.Tag(name="f7-range",attrs=slider.attrs)
                slider.append(obj)
                if "label" in obj.attrs:
                    del obj['label']
                if "min" in slider.attrs:
                    del slider['min']
                if "max" in slider.attrs:
                    del slider['max']
                if "step" in slider.attrs:
                    del slider['step']
                if "value" in slider.attrs:
                    del slider['value']
                slider.attrs[':input']="false"
                obj.attrs['slot']="input"

    for checkbox in soup.find_all(attrs={'type':"checkbox"}):
        checkbox.attrs['checkbox']=""
        del checkbox['type']
        if checkbox.name=="f7-list-input":
            par=checkbox.parent
            while par.parent:
                if par.name=="f7-list-item":
                    break
                par=par.parent
            par.attrs = {**par.attrs, **checkbox.attrs}
            checkbox.unwrap()
    for radio in soup.find_all(attrs={'type':"radio"}):
        radio.attrs['radio']=""
        del radio['type']
        if radio.name=="f7-list-input":
            par=radio.parent
            while par.parent:
                if par.name=="f7-list-item":
                    break
                par=par.parent
            par.attrs = {**par.attrs, **radio.attrs}
            radio.unwrap()
    for check in soup.find_all("label",attrs={'class':'checkbox'}):
        check.name="f7-checkbox"
        cls=check.attrs['class']
        cls.remove("checkbox")
        if len(cls)<1:
            del check['class']
        inp = check.find("input")
        if inp:
            check.attrs=dict(check.attrs,**inp.attrs)
            inp.clear()
            inp.unwrap()

    soup = delinner(soup, "item-media")
    soup = delinner(soup, "toggle")
    soup = delinner(soup, "range-slider")
    soup = delinner(soup, "item-content")
    soup = delinner(soup, "item-inner")
    soup = delinner(soup, "item-input-wrap")
    soup = delinner(soup, "item-title-row")
    soup = f7tovue(soup, "list-group", "f7-list-group")
    for d in soup.find_all("f7-list-item"):
        if "swipeout" in d.attrs:
            for right in d.find_all(attrs={'class':'swipeout-actions-right'}):
                cls=right.attrs['class']
                cls.remove("swipeout-actions-right")
                if len(cls)<1:
                    del right['class']
                right.name="f7-swipeout-actions"
                right.attrs['right']=""
                for i in right.find_all():
                    i.name = "f7-swipeout-button"
                    if "class" in i.attrs:
                        cls = i.attrs['class']
                        for c in cls:
                            if c.find("bg-color") > -1:
                                i.attrs['color'] = c[9:]
                                cls.remove(c)
                        if "swipeout-overswipe" in cls:
                            i.attrs['overswipe'] = ""
                            cls.remove('swipeout-overswipe')
                        if "swipeout-close" in cls:
                            i.attrs['close'] = ""
                            cls.remove('swipeout-close')
                        if "swipeout-delete" in cls:
                            i.attrs['delete'] = ""
                            cls.remove('swipeout-delete')
                        if len(cls) < 1:
                            del i['class']
                    if "data-confirm" in i.attrs:
                        i.attrs['confirm-text'] = i.attrs['data-confirm']
                        del i['data-confirm']
                    if i.get_text().strip() != "":
                        i.attrs['text'] = i.get_text().strip()
                        i.clear()
            for left in d.find_all(attrs={'class':'swipeout-actions-left'}):
                cls = left.attrs['class']
                cls.remove("swipeout-actions-left")
                if len(cls) < 1:
                    del left['class']
                left.name = "f7-swipeout-actions"
                left.attrs['left'] = ""
                for i in left.find_all():
                    i.name = "f7-swipeout-button"
                    if "class" in i.attrs:
                        cls = i.attrs['class']
                        for c in cls:
                            if c.find("bg-color")>-1:
                                i.attrs['color']=c[9:]
                                cls.remove(c)
                        if "swipeout-overswipe" in cls:
                            i.attrs['overswipe'] = ""
                            cls.remove('swipeout-overswipe')
                        if "swipeout-close" in cls:
                            i.attrs['close'] = ""
                            cls.remove('swipeout-close')
                        if "swipeout-delete" in cls:
                            i.attrs['delete'] = ""
                            cls.remove('swipeout-delete')
                        if len(cls) < 1:
                            del i['class']
                    if "data-confirm" in i.attrs:
                        i.attrs['confirm-text'] = i.attrs['data-confirm']
                        del i['data-confirm']
                    if i.get_text().strip()!="":
                        i.attrs['text']=i.get_text().strip()
                        i.clear()
    return soup


def barinit(soup):
    soup = navbarinit(soup)
    soup = f7tovue(soup,"subnavbar","f7-subnavbar")
    soup = f7tovue(soup, "list", "f7-list")
    soup = delinner(soup,"subnavbar-inner")
    soup = f7tovue(soup, "toolbar", "f7-toolbar")
    soup = addattr(soup, "toolbar", "f7-toolbar", "tabbar")
    soup = delinner(soup, "toolbar-inner")
    soup = addattr(soup, "tab-link", "f7-link", "tab-link-active")
    soup = addattr(soup, "tab-link", "f7-link", "tab-link")
    soup = f7tovue(soup, "tabs", "f7-tabs")
    soup = f7tovue(soup, "tab", "f7-tab")
    soup = addattr(soup, "tab", "f7-tab", "tab-active")
    docs = soup.find_all("f7-toolbar")
    if docs:
        for d in docs:
            if "tabbar" in d.attrs:
                d.attrs[':bottom-md']="isBottom"
                if "class" in d.attrs:
                    cls=d.attrs['class']
                    if "tabbar-labels" in cls:
                        cls.remove("tabbar-labels")
                        d.attrs['labels']=""
                        if len(cls)<1:
                            del d['class']
    for a in soup.find_all("a"):
        if "tab-link" in a.attrs:
            if "href" in a.attrs:
                a.attrs['tab-link']=a.attrs['href']
                del a['href']
                a.name="f7-link"
    return soup
def chipinit(soup):
    soup = f7tovue(soup,"chip","f7-chip")
    docs = soup.find_all("f7-chip")
    if docs:
        for d in docs:
            label = d.find(attrs={'class':'chip-label'})
            if label:
                d.attrs['text']=label.get_text().strip()
                label.clear()
                label.unwrap()
            media = d.find(attrs={'class':'chip-media'})
            if media:
                icon=media.find("f7-icon")
                if icon:
                    icon.attrs['slot']="media"
                img=media.find("img")
                if img:
                    img.attrs['slot']="media"
                if "class" in media.attrs:
                    cls=media.attrs['class']
                    for i in cls:
                        if i.find("bg-color-")>-1:
                            cls.remove(i)
                            d.attrs['media-bg-color']=i[9:]
                if media.get_text().strip()!="":
                    d.attrs['media']=media.get_text().strip()
                    media.clear()
                media.unwrap()
            delete = d.find(attrs={'class':'chip-delete'})
            if delete:
                d.attrs['deleteable']=""
                d.attrs['click']="deleteChip"
                delete.unwrap()
                delete.clear()
            if "class" in d.attrs:
                cls=d.attrs['class']
                for i in cls:
                    if i.find("color-")>-1:
                        cls.remove(i)
                        d.attrs['color']=i[6:]
                if len(cls)<1:
                    del d['class']

    return soup
def gridinit(soup):
    soup = addattr(soup, "row", "f7-row", "no-gap")
    soup = f7tovue(soup,"row","f7-row")
    docs=soup.find_all("f7-row")
    if docs:
        for d in docs:
            for i in d.find_all():
                if "class" in i.attrs:
                    cls=i.attrs['class']
                    for c in cls:
                        if c.find("col-")>-1:
                            i.name="f7-col"
                            i.attrs['width']=c[4:]
                            cls.remove(c)
                    for c in cls:
                        if c.find("tablet-") > -1:
                            i.attrs['tablet-width'] = c[7:]
                            cls.remove(c)

                    if len(cls)<1:
                        del i['class']
    return soup
def fabinit(soup):
    soup = f7tovue(soup,"fab","f7-fab")
    soup = f7tovue(soup,"fab-buttons","f7-fab-buttons")
    docs= soup.find_all("f7-fab")
    for d in docs:
        if "class" in d.attrs:
            cls=d.attrs['class']
            for c in cls:
                if c.find("fab-")>-1:
                    d.attrs['position']=c[4:]
                    cls.remove(c)
            for c in cls:
                if c.find("color-")>-1:
                    d.attrs['color']=c[6:]
                    cls.remove(c)
            if len(cls)<1:
                del d['class']
        link=d.find_all("a",attrs={'href':'#'})
        if link:
            for a in link:
                a.unwrap()
        docs = soup.find_all("f7-fab")
        for d in docs:
            if "class" in d.attrs:
                cls = d.attrs['class']
                for c in cls:
                    if c.find("fab-") > -1:
                        d.attrs['position'] = c[4:]
                        cls.remove(c)
                for c in cls:
                    if c.find("color-") > -1:
                        d.attrs['color'] = c[6:]
                        cls.remove(c)
                if len(cls) < 1:
                    del d['class']
    docs = soup.find_all("f7-fab-buttons")
    for d in docs:
        if "class" in d.attrs:
            cls = d.attrs['class']
            for c in cls:
                if c.find("fab-") > -1:
                    d.attrs['position'] = c[12:]
                    cls.remove(c)
            for c in cls:
                if c.find("color-") > -1:
                    d.attrs['color'] = c[6:]
                    cls.remove(c)
            if len(cls) < 1:
                del d['class']
        for i in d.find_all():
            obj = bs4.element.Tag(name='f7-fab-button')
            i.wrap(obj)

    return soup
def forminit(soup):
    for form in soup.find_all("form"):
        l = form.find("f7-list")
        if l:
            form.unwrap()
            l.attrs['form']=""
            for inp in l.find_all("input"):
                inp.name="f7-list-input"
    return soup
def messageinit(soup):
    for bar in soup.find_all("f7-messagebar"):
        textarea=bar.find("textarea")
        if textarea:
            bar.attrs=dict(bar.attrs,**textarea.attrs)
            textarea.clear()
            textarea.unwrap()
        for link in bar.find_all("f7-link"):
            icon=link.find("f7-icon")
            if icon:
                link.attrs=dict(link.attrs,**icon.attrs)
                icon.clear()
                icon.unwrap()

    for message in soup.find_all("f7-message"):
        if "class" in message.attrs:
            cls=message.attrs['class']
            if "message-sent" in cls:
                cls.remove("message-sent")
                message.attrs['type']="sent"
            if "message-received" in cls:
                cls.remove("message-received")
                message.attrs['type']="received"
            if len(cls)<1:
                del message['class']
        text = message.find(attrs={'class':'message-text'})
        if text:
            image = text.find("img")
            if image:
                message.attrs['image']=image.attrs['src']
                image.clear()
                image.unwrap()
            message.attrs['text']=text.get_text().strip()
            text.clear()
            text.unwrap()
        header = message.find(attrs={'class': 'message-header'})
        if header:
            message.attrs['header'] = header.get_text().strip()
            header.clear()
            header.unwrap()
        footer = message.find(attrs={'class': 'message-footer'})
        if footer:
            message.attrs['footer'] = footer.get_text().strip()
            footer.clear()
            footer.unwrap()
        name = message.find(attrs={'class': 'message-name'})
        if name:
            message.attrs['name'] = name.get_text().strip()
            name.clear()
            name.unwrap()
        avatar = message.find(attrs={'class': 'message-avatar'})
        if avatar:
            message.attrs['avatar'] = avatar.attrs['style'].replace("background-image:","").replace("url(","").replace(")","").strip()
            avatar.clear()
            avatar.unwrap()

    soup = delinner(soup,"message-content")
    soup = delinner(soup,"message-bubble")
    return soup
def preloaderinit(soup):
    soup = f7tovue(soup, "preloader", "f7-preloader")
    for p in soup.find_all("f7-preloader"):
        if "class" in p.attrs:
            cls=p.attrs['class']
            if "ks-preloader-big" in cls:
                cls.remove("ks-preloader-big")
                p.attrs[':size']="42"
            for c in cls:
                if c.find("preloader-")>-1:
                    p.attrs['color']=c[10:]
                    cls.remove(c)
            if len(cls)<1:
                del p['class']
    return soup
def ptrinit(soup):
    for docs in soup.find_all(attrs={'class':'ptr-preloader'}):
        par = docs.findParent("f7-page")
        if par:
            par.attrs['ptr']=""
            par.attrs['ptr:refresh']="onRefresh"
    return soup
def searchinit(soup):
    soup = f7tovue(soup, "searchbar", "f7-searchbar")
    for s in soup.find_all("f7-searchbar"):
        if "class" in s.attrs:
            cls=s.attrs['class']
            if "searchbar-init" in cls:
                s.attrs[':init']="true"
                cls.remove("searchbar-init")
            if len(cls)<1:
                del s['class']
        if "data-search-container" in s.attrs:
            s.attrs['search-container']=s.attrs['data-search-container']
            del s['data-search-container']
        if "data-search-in" in s.attrs:
            s.attrs['search-in']=s.attrs['data-search-in']
            del s['data-search-in']
        inp=s.find(attrs={'type':'search'})
        if inp:
            if "placeholder" in inp.attrs:
                s.attrs['placeholder'] = inp.attrs['placeholder']
            inp.clear()
            inp.unwrap()
        btn=s.find(attrs={'class':'input-clear-button'})
        if btn:
            s.attrs[':clear-button']="true"
            btn.clear()
            btn.unwrap()
        backdrop = soup.find(attrs={'class':'searchbar-backdrop'})
        if backdrop:
            s.attrs[':backdrop']="true"
        s.attrs['disable-link-text']="Cancel"
    delinner(soup,"searchbar-inner")
    delinner(soup, "searchbar-input-wrap")
    delinner(soup,"searchbar-backdrop")

    return soup
def tabsinit(soup):
    soup = f7tovue(soup, "tabs", "f7-tabs")
    soup = f7tovue(soup, "tab", "f7-tab")
    for docs in soup.find_all("f7-tabs"):
        anim=docs.findParent(attrs={'class':'tabs-animated-wrap'})
        if anim:
            docs.attrs['animated']=""
        swipe=docs.findParent(attrs={'class':'tabs-swipeable-wrap'})
        if swipe:
            docs.attrs['swipeable']=""
    for pc in soup.find_all(attrs={'class':'page-content'}):
        if "hide-bars-on-scroll" in pc.attrs['class']:
            par=pc.findParent("f7-page")
            if par:
                par.attrs['hide-bars-on-scroll']=""
    for tab in soup.find_all("f7-tab"):
        if "class" in tab.attrs:
            cls=tab.attrs['class']
            if "page-content" in tab.attrs['class']:
                cls.remove("page-content")
            if len(cls)<1:
                del tab['class']
    for btn in soup.find_all(attrs={'class':'button'}):
        if "class" in btn.attrs:
            cls=btn.attrs['class']
            if "tab-link" in btn.attrs['class']:
                cls.remove("tab-link")
                if "href" in btn.attrs:
                    btn.attrs['tab-link'] = btn.attrs['href']
                    del btn['href']
            if len(cls)<1:
                del btn['class']
    delinner(soup,"tabs-animated-wrap")
    delinner(soup,"tabs-swipeable-wrap")
    return soup
def swiperinit(soup):
    soup = f7tovue(soup, "swiper-container", "f7-swiper")
    soup = f7tovue(soup, "swiper-slide", "f7-swiper-slide")
    for swiper in soup.find_all("f7-swiper"):
        if "class" in swiper.attrs:
            cls=swiper.attrs['class']
            if "swiper-init" in cls:
                cls.remove("swiper-init")

            if len(cls)<1:
                del swiper['class']
    soup = addattr(soup, "swiper-container", "f7-swiper", "swiper-init")

    delinner(soup,"swiper-pagination")
    delinner(soup,"swiper-wrapper")

    return soup
def vuefilter(soup):
    soup = colorattr(soup, "progressbar-infinite")
    for i in soup.find_all(attrs={'id':'app'}):
        i.name="f7-app"
        del i['id']
    for i in soup.find_all(attrs={'class':'progressbar-infinite'}):
        i.name="f7-progressbar"
        i.attrs['infinite']=""
        cls = i.attrs['class']
        cls.remove("progressbar-infinite")
        if len(cls)<1:
            del i['class']
    for i in soup.find_all("f7-link"):
        if "class" in i.attrs:
            cls=i.attrs['class']
            if "popover-open" in cls:
                cls.remove("popover-open")
            if len(cls)<1:
                del i['class']
        if "data-popover" in i.attrs:
            i.attrs['popover-open']=i.attrs['data-popover']
            del i['data-popover']
    for i in soup.find_all("f7-button"):
        if "data-login-screen" in i.attrs:
            i.attrs['login-screen-open']=i.attrs['data-login-screen']
            del i.attrs['data-login-screen']
    for i in soup.find_all("f7-link"):
        if "data-login-screen" in i.attrs:
            i.attrs['login-screen-open']=i.attrs['data-login-screen']
            del i.attrs['data-login-screen']
    for i in soup.find_all("f7-icon",attrs={'icon':"icon-checkbox"}):
        i.clear()
        i.unwrap()
    for i in soup.find_all("head"):
        i.clear()
        i.unwrap()
    for i in soup.find_all("!DOCTYPE"):
        i.unwrap()
    docs=soup.find_all("f7-icon",attrs={'icon':'checkbox'})
    if docs:
        for d in docs:
            d.unwrap()
    s1=str(soup)
    if s1.find("<template")<0 and s1.find("</template")<0:
        s1="<template>\n"+s1+"\n</template>"
    soup=BeautifulSoup(s1,"lxml")
    for i in soup.find_all("html"):
        i.unwrap()
    for i in soup.find_all("body"):
        i.unwrap()
    template=soup.find("template")
    for i in soup.find_all("script"):
        template.insert_after(i)
    s1=str(soup)
    s1=s1.replace("=\"\"","")
    strlist=s1.split("\n")
    ind = 0
    for i in strlist:
        if i.find("/>") > -1 and i.find("<f7-list-input") > -1:
            strlist[ind] = strlist[ind].replace("/>", "></f7-list-input>")
        if i.find("<!DOCTYPE")>-1:
            strlist[ind] = strlist[ind].replace(i,"")
        ind = ind + 1
    strlist = filter(None, strlist)
    s1 = "\n".join(strlist)
    s1=s1.replace("click=","@click=")
    s1 = s1.replace("ptr:refresh=","@ptr:refresh=")
    return s1
def falseattr(soup,elem,attr,old,new):
    for i in soup.find_all():
        if "sliding" in i.attrs:
            if i.attrs['sliding']=="false":
                del i['sliding']
                i.attrs[':sliding']="false"
    if attr=="name":
        docs = soup.find_all(elem)
    else:
        docs=soup.find_all(attrs={attr:elem})
    if docs:
        for d in docs:
            if "class" in d.attrs:
                cls=d.attrs['class']
                if old in cls:
                    cls.remove(old)
                else:
                    d.attrs[new]="false"
                if len(cls) < 1:
                    del d['class']
            else:
                d.attrs[new] = "false"
    return soup

def f7update(path):
    code_file = open(path, "r", encoding='utf-8')
    code = code_file.read()
    code_file.close()
    soup = BeautifulSoup(code, "html.parser")
    soup = addattr(soup, "page", "f7-page", "no-navbar")
    soup = addattr(soup, "page", "f7-page", "no-toolbar")
    soup = addattr(soup, "page", "f7-page", "no-swipeback")
    soup = addattr(soup, "page", "f7-page", "with-subnavbar")
    soup = addattr(soup, "page", "f7-page", "hide-bars-on-scroll")
    soup = addattr(soup, "page", "f7-page", "hide-navbar-on-scroll")
    soup = addattr(soup, "page", "f7-page", "hide-toolbar-on-scroll")
    soup = renattr(soup,"page-content","class","infinite-scroll","infinite")


    soup = addattr(soup, "block", "f7-block", "no-navbar")
    soup = addattr(soup, "block", "f7-block", "no-swipeback")
    soup = f7tovue(soup,"page","f7-page")
    soup = changeattrname(soup,"f7-page","data-name","name")

    soup = tabsinit(soup)
    soup = delinner(soup, "page-content")
    soup = f7tovue(soup,"link","f7-link")
    soup = f7tovue(soup,"navbar","f7-navbar")
    soup = delinner(soup,"navbar-inner")
    soup = addattr(soup, "block", "f7-block", "inset")
    soup = renattr(soup,"block","class","block-strong","strong")
    soup = addattr(soup, "block", "f7-block", "tablet-inset")
    soup = f7tovue(soup, "block", "f7-block")
    soup = f7tovue(soup, "block-header", "f7-block-header")
    soup = f7tovue(soup, "block-title", "f7-block-title")
    soup = f7tovue(soup, "block-footer", "f7-block-footer")
    soup = addattr(soup, "swipeout", "f7-list-item", "swipeout")
    soup = extattr(soup, "accordion-item", "f7-list-item", "accordion-item")
    soup = accordioninit(soup)
    soup = f7tovue(soup,"accordion-item-toggle","f7-accordion-toggle")
    soup = f7tovue(soup, "accordion-item-content", "f7-accordion-content")
    soup = colorattr(soup, "badge")
    soup = f7tovue(soup,"badge", "f7-badge")
    soup = linkinit(soup)
    soup = barinit(soup)
    soup = smartinit(soup)
    soup = listinit(soup)
    soup = colorattr(soup, "button")
    soup = renattr(soup,"button","class","button-active","active")
    soup = renattr(soup, "button", "class", "button-big", "big")
    soup = renattr(soup, "button", "class", "button-small", "small")
    soup = renattr(soup, "button", "class", "button-outline", "outline")
    soup = renattr(soup, "button", "class", "button-round", "round")
    soup = renattr(soup, "button", "class", "button-raised", "raised")
    soup = renattr(soup, "button", "class", "button-fill", "fill")
    soup = renattr(soup, "button", "class", "panel-open", "panel-open")
    soup = renattr(soup, "button", "class", "panel-close", "panel-close")
    soup = renattr(soup, "button", "class", "actions-open", "actions-open")
    soup = renattr(soup, "button", "class", "actions-close", "actions-close")
    soup = renattr(soup, "button", "class", "popup-open", "popup-open")
    soup = renattr(soup, "button", "class", "popup-close", "popup-close")
    soup = renattr(soup, "button", "class", "popover-open", "popover-open")
    soup = renattr(soup, "button", "class", "popover-close", "popover-close")
    soup = renattr(soup, "button", "class", "sheet-open", "sheet-open")
    soup = renattr(soup, "button", "class", "sheet-close", "sheet-close")
    soup = renattr(soup, "button", "class", "sortable-enable", "sortable-enable")
    soup = renattr(soup, "button", "class", "sortable-disable", "sortable-disable")
    soup = renattr(soup, "button", "class", "searchbar-enable", "searchbar-enable")
    soup = renattr(soup, "button", "class", "searchbar-disable", "searchbar-disable")
    soup = renattr(soup, "button", "class", "sortable-toggle", "sortable-toggle")
    soup = renattr(soup, "button", "class", "searchbar-toggle", "searchbar-toggle")
    soup = renattr(soup, "button", "class", "login-screen-open", "login-screen-open")
    soup = renattr(soup, "button", "class", "login-screen-close", "login-screen-close")
    soup = renattr(soup, "link", "class", "panel-open", "panel-open")
    soup = renattr(soup, "link", "class", "panel-close", "panel-close")
    soup = renattr(soup, "link", "class", "actions-open", "actions-open")
    soup = renattr(soup, "link", "class", "actions-close", "actions-close")
    soup = renattr(soup, "link", "class", "popup-open", "popup-open")
    soup = renattr(soup, "link", "class", "popup-close", "popup-close")
    soup = renattr(soup, "link", "class", "popover-open", "popover-open")
    soup = renattr(soup, "link", "class", "popover-close", "popover-close")
    soup = renattr(soup, "link", "class", "sheet-open", "sheet-open")
    soup = renattr(soup, "link", "class", "sheet-close", "sheet-close")
    soup = renattr(soup, "link", "class", "sortable-enable", "sortable-enable")
    soup = renattr(soup, "link", "class", "sortable-disable", "sortable-disable")
    soup = renattr(soup, "link", "class", "searchbar-enable", "searchbar-enable")
    soup = renattr(soup, "link", "class", "searchbar-disable", "searchbar-disable")
    soup = renattr(soup, "link", "class", "sortable-toggle", "sortable-toggle")
    soup = renattr(soup, "link", "class", "searchbar-toggle", "searchbar-toggle")
    soup = renattr(soup, "link", "class", "login-screen-open", "login-screen-open")
    soup = renattr(soup, "link", "class", "login-screen-close", "login-screen-close")
    soup = renattr(soup, "item-link", "class", "panel-open", "panel-open")
    soup = renattr(soup, "item-link", "class", "panel-close", "panel-close")
    soup = renattr(soup, "item-link", "class", "actions-open", "actions-open")
    soup = renattr(soup, "item-link", "class", "actions-close", "actions-close")
    soup = renattr(soup, "item-link", "class", "popup-open", "popup-open")
    soup = renattr(soup, "item-link", "class", "popup-close", "popup-close")
    soup = renattr(soup, "item-link", "class", "popover-open", "popover-open")
    soup = renattr(soup, "item-link", "class", "popover-close", "popover-close")
    soup = renattr(soup, "item-link", "class", "sheet-open", "sheet-open")
    soup = renattr(soup, "item-link", "class", "sheet-close", "sheet-close")
    soup = renattr(soup, "item-link", "class", "sortable-enable", "sortable-enable")
    soup = renattr(soup, "item-link", "class", "sortable-disable", "sortable-disable")
    soup = renattr(soup, "item-link", "class", "searchbar-enable", "searchbar-enable")
    soup = renattr(soup, "item-link", "class", "searchbar-disable", "searchbar-disable")
    soup = renattr(soup, "item-link", "class", "sortable-toggle", "sortable-toggle")
    soup = renattr(soup, "item-link", "class", "searchbar-toggle", "searchbar-toggle")
    soup = renattr(soup, "item-link", "class", "login-screen-open", "login-screen-open")
    soup = renattr(soup, "item-link", "class", "login-screen-close", "login-screen-close")


    soup = f7tovue(soup, "button", "f7-button")
    soup = f7tovue(soup,"segmented","f7-segmented")
    soup = f7tovue(soup,"link","f7-link")
    soup = iconinit(soup)
    soup = f7tovue(soup,"icon", "f7-icon")
    soup = f7tovue(soup,"card","f7-card")
    soup = f7tovue(soup,"card-content","f7-card-content")
    soup = f7tovue(soup, "card-header", "f7-card-header")
    soup = f7tovue(soup, "card-footer", "f7-card-footer")
    soup = falseattr(soup,"f7-card-content","name","card-content-padding",":padding")
    soup = chipinit(soup)
    soup = gridinit(soup)
    soup = fabinit(soup)
    soup = f7tovue(soup, "login-screen", "f7-login-screen")
    soup = f7tovue(soup,"login-screen-title","f7-login-screen-title")
    soup = f7tovue(soup,"list-block-label","f7-block-footer")
    soup = forminit(soup)
    soup = f7tovue(soup, "messages", "f7-messages")
    soup = f7tovue(soup, "messages-title", "f7-messages-title")
    soup = f7tovue(soup, "message", "f7-message")
    soup = f7tovue(soup, "messagebar", "f7-messagebar")
    soup = messageinit(soup)
    soup = preloaderinit(soup)
    soup = colorattr(soup, "progressbar")
    soup = f7tovue(soup,"progressbar","f7-progressbar")
    soup = changeattrname(soup,"f7-progressbar","data-progress",":progress")
    soup = changeattrname(soup,"f7-button","data-panel","panel-open")
    soup = changeattrname(soup,"f7-link","data-progress","panel-open")



    soup = f7tovue(soup, "statusbar", "f7-statusbar")
    soup = delinner(soup,"panel-overlay")
    soup = f7tovue(soup, "panel", "f7-panel")
    soup = renattr(soup, "panel", "class", "panel-left", "left")
    soup = renattr(soup, "panel", "class", "panel-right", "right")
    soup = renattr(soup, "panel", "class", "panel-reveal", "reveal")
    soup = renattr(soup, "panel", "class", "panel-cover", "cover")
    soup = f7tovue(soup,"popup","f7-popup")
    soup = f7tovue(soup, "popover", "f7-popover")
    delinner(soup,"popover-angle")
    delinner(soup, "popover-inner")
    soup = f7tovue(soup,"picker-modal","f7-sheet")
    soup = f7tovue(soup,"sheet-modal","f7-sheet")
    delinner(soup,"picker-modal-inner")
    delinner(soup,"sheet-modal-inner")

    soup = ptrinit(soup)
    soup = searchinit(soup)
    #soup = swiperinit(soup)
    soup = f7tovue(soup, "views", "f7-views")
    soup = f7tovue(soup, "view", "f7-view")
    s1=vuefilter(soup)

    return s1
#path="C:\\Users\\Administrator\\Desktop\\bianli\\untitled\\F7_files\\vue\\src\\pages\\accordion.vue"
#s1=f7update(path)
#print(s1)