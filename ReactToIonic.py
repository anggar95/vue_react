import re,pymysql,bs4,tkinter.messagebox
from bs4 import BeautifulSoup
def ionicfilter(soup):
    for docs in soup.find_all("blocktitle"):
        docs.name="IonHeader"
        docs.attrs['align']="center"
    s1=str(soup).replace("&gt;",">")
    s1=s1.replace('=""',"")
    return s1
def changename(soup,old,new):
    for docs in soup.find_all(old):
        docs.name=new
    return soup
def changeattr(soup,elem,old,new,newval=""):
    for docs in soup.find_all(elem):
        if old in docs.attrs:
            if newval == "-":
                newval = docs.attrs[old]
            docs.attrs[new]=newval
            del docs[old]
    return soup
def delattr(soup,elem,attr):
    for docs in soup.find_all(elem):
        if attr in docs.attrs:
            del docs[attr]
    return soup
def delinner(soup,elem):
    for docs in soup.find_all(elem):
        if docs.parent:
            par=docs.parent
            par.attrs=dict(par.attrs,**docs.attrs)
        docs.unwrap()
    return soup
def barinit(soup):
    for docs in soup.find_all("navbar"):
        obj = bs4.element.Tag(name="IonHeader")
        docs.wrap(obj)
        docs.name="IonToolbar"
        if "backlink" in docs.attrs:
            obj1= bs4.element.Tag(name="IonButton",attrs={'slot':'start'})
            obj2 = bs4.element.Tag(name="IonBackButton")
            obj1.append(obj2)
            docs.insert(1,obj1)
            del docs.attrs['backlink']
        for right in docs.find_all("navright"):
            if right.find("a") or right.find("IonButton"):
                right.name="IonButtons"
                right.attrs['slot']="primary"
                a=right.find("a")
                if a:
                    a.name="IonButton"
    for docs in soup.find_all("IonToolbar"):
        if "title" in docs.attrs:
            obj1 = bs4.element.Tag(name="IonTitle")
            obj1.string=docs.attrs['title']
            docs.append(obj1)
            del docs['title']
    return soup
def gridinit(soup):
    for docs in soup.find_all("IonRow"):
        obj=bs4.element.Tag(name="IonGrid")
        if docs.parent.name != "IonGrid":
            docs.wrap(obj)
    for docs in soup.find_all("IonCol"):
        if "tabletwidth" in docs.attrs:
            x=int(docs.attrs['tabletwidth'])
            x=x/12
            x = round(x, 2)
            docs.attrs['lg-size']=x
            docs.attrs['xl-size'] = x
            del docs['tabletwidth']
            if "width" in docs.attrs:
                x=int(docs.attrs['width'])
                x=x/12
                x=round(x,2)
                docs.attrs['xs-size']=x
                docs.attrs['sm-size'] = x
                docs.attrs['md-size'] = x
                del docs['width']
        else:
            if "width" in docs.attrs:
                x=int(docs.attrs['width'])
                x=x/12
                x=round(x,2)
                docs.attrs['size']=x
                del docs['width']
    return soup
def listinit(soup):
    for docs in soup.find_all("IonList"):
        if "inset" in docs.attrs:
            for i in docs.find_all("IonItem"):
                i.attrs['lines']="inset"
        for attr in list(docs.attrs):
            del docs[attr]
    for docs in soup.find_all("IonItem"):
        if "checkbox" in docs.attrs:
            docs.name="IonCheckbox"
            del docs['checkbox']
            obj=bs4.element.Tag(name="IonItem")
            docs.wrap(obj)
            if "defaultchecked" in docs.attrs:
                docs.attrs['checked']=""
                del docs['defaultchecked']
        if "radio" in docs.attrs:
            docs.name = "IonRadio"
            del docs['radio']
            obj = bs4.element.Tag(name="IonItem")
            docs.wrap(obj)
            if "defaultchecked" in docs.attrs:
                docs.attrs['checked'] = ""
                del docs['defaultchecked']
            par=docs.parent.parent
            par.name="IonRadioGroup"
            obj = bs4.element.Tag(name="IonList")
            if par.parent.name!="IonList":
                par.wrap(obj)

        if "header" in docs.attrs:
            obj=bs4.element.Tag(name="p")
            obj.string=docs.attrs['header']
            docs.append(obj)
            del docs['header']
        if "title" in docs.attrs:
            if "subtitle" in docs.attrs:
                obj = bs4.element.Tag(name="h2")
                obj1 = bs4.element.Tag(name="b")
                docs.append(obj)
                obj.append(obj1)
                obj1.string=docs.attrs['title']
            else:
                obj = bs4.element.Tag(name="h3")
                docs.append(obj)
                obj.string=docs.attrs['title']
            del docs['title']
        if "subtitle" in docs.attrs:
            obj = bs4.element.Tag(name="p")
            obj1 = bs4.element.Tag(name="h3")
            docs.append(obj)
            obj.append(obj1)
            obj1.string = docs.attrs['subtitle']
            del docs['subtitle']
        if "link" in docs.attrs:
            docs.attrs['detail']=""
            docs.attrs['href']=docs.attrs['link']
            del docs['link']
        if "footer" in docs.attrs:
            obj = bs4.element.Tag(name="p")
            obj.string = docs.attrs['footer']
            docs.append(obj)
            del docs['footer']
        if "text" in docs.attrs:
            obj = bs4.element.Tag(name="IonText")
            docs.append(obj)
            obj.string = docs.attrs['text']
            del docs['text']
        if "after" in docs.attrs:
            after=docs.attrs['after']
            del docs['after']
            obj=bs4.element.Tag(name="IonLabel",attrs={'slot':'end'})
            docs.append(obj)
            obj.string=after
        if "badge" in docs.attrs:
            obj=bs4.element.Tag(name="IonBadge", attrs={'slot':'end'})
            docs.append(obj)
            obj.string=docs.attrs['badge']
            del docs['badge']
            if "badgecolor" in docs.attrs:
                obj.attrs['color']=docs.attrs['badgecolor']
                del docs['badgecolor']
        for i in docs.find_all("IonIcon"):
            i.attrs['slot']="start"
            if "icon" in i.attrs:
                i.attrs['name']=i.attrs['icon']
                del i.attrs['icon']
        for i in docs.find_all("img"):
            i.name="IonImg"
            i.attrs['src']="{"+i.attrs['src']+"}"
            i.attrs['slot'] = "start"
        if "divider" in docs.attrs:
            docs.name="IonItemDivider"
            del docs['divider']
        if "grouptitle" in docs.attrs:
            docs.name="IonItemDivider"
            del docs['grouptitle']
        for i in docs.find_all("blockfooter"):
            i.unwrap()

    return soup
def inputinit(soup):
    for li in soup.find_all("IonList"):
        for i in li.find_all("IonInput"):
            obj=bs4.element.Tag(name="IonItem")
            i.wrap(obj)
        for i in li.find_all("IonIcon"):
            i.attrs['slot']="start"
            if i.parent.name=="IonInput":
                p=i.parent.parent
                p.append(i)
        for i in li.find_all("img"):
            i.name="IonImg"
            i.attrs['slot']="start"
            i.attrs['src'] = "{" + i.attrs['src'] + "}"
    for docs in soup.find_all("IonInput"):
        if "clearbutton" in docs.attrs:
            docs.attrs['clearInput']=""
            del docs['clearbutton']
        if "label" in docs.attrs:
            obj=bs4.element.Tag(name="IonLabel",attrs={'slot':'start'})
            obj.string=docs.attrs['label']
            docs.parent.append(obj)
            del docs['label']
        if "type" in docs.attrs:
            if docs.attrs['type']=="textarea":
                docs.name="IonTextarea"
                del docs['type']
            elif docs.attrs['type']=="select":
                docs.name="IonSelect"
                for i in docs.find_all("option"):
                    i.name="IonSelectOption"
                del docs['type']
        if "input" in docs.attrs:
            if docs.attrs['input']=="false" or docs.attrs['input']=="{false}":
                docs.attrs['readonly']="true"
                del docs['input']
        for i in docs.find_all("range"):
            i.name="IonRange"
            if i.parent.name=="IonInput":
                i.parent.unwrap()
            if "slot" in i.attrs:
                del i['slot']
        for i in docs.find_all("toggle"):
            i.name="IonToggle"
            if i.parent=="IonInput":
                i.parent.unwrap()
            if "slot" in i.attrs:
                del i['slot']
    return soup
def cardinit(soup):
    for docs in soup.find_all("IonCard"):
        if "title" in docs.attrs:
            obj=bs4.element.Tag(name="IonCardTitle")
            obj.string=docs.attrs['title']
            del docs['title']
            docs.append(obj)
        if "content" in docs.attrs:
            obj = bs4.element.Tag(name="IonCardContent")
            obj.string = docs.attrs['content']
            del docs['content']
            docs.append(obj)
        if "footer" in docs.attrs:
            obj = bs4.element.Tag(name="IonCardSubtitle")
            obj.string = docs.attrs['footer']
            del docs['footer']
            docs.append(obj)
    for docs in soup.find_all("IonCardTitle"):
        if docs.parent.name!="IonCardHeader":
            obj=bs4.element.Tag(name="IonCardHeader")
            docs.wrap(obj)
    return soup
def chipinit(soup):
    for docs in soup.find_all("IonChip"):
        if "text" in docs.attrs:
            obj=bs4.element.Tag(name="IonLabel")
            obj.string=docs.attrs['text']
            docs.append(obj)
            del docs['text']
        if "mediabgcolor" in docs.attrs:
            docs.attrs['color']=docs.attrs['mediabgcolor']
            del docs['mediabgcolor']
        for i in docs.find_all("IonIcon") or docs.find_all("IonImg") or docs.find_all("img"):
            if "slot" in i.attrs:
                del i['slot']
        for i in docs.find_all("img"):
            obj=bs4.element.Tag(name="IonAvatar")
            if i.parent.name!="IonAvatar":
                i.wrap(obj)
        if "media" in docs.attrs:
            del docs['media']
        if "deleteable" in docs.attrs:
            del docs['deleteable']
            obj=bs4.element.Tag(name="IonIcon",attrs={'name':'close-circle'})
            docs.append(obj)
            if "onclick" in docs.attrs:
                obj.attrs['onclick']=docs.attrs['onclick']
                del docs['onclick']
    return soup
def fabinit(soup):
    iconlist=[]
    for docs in soup.find_all("IonFab"):
        if "position" in docs.attrs:
            fabpos=docs.attrs['position'].split("-")
            if fabpos[0]=="right":
                docs.attrs['horizontal']="end"
            if fabpos[0]=="left":
                docs.attrs['horizontal']="start"
            docs.attrs['vertical']=fabpos[1]
            del docs['position']
        if not docs.find("IonFabButton"):
            obj = bs4.element.Tag(name="IonFabButton")
            for i in docs.find_all("IonIcon"):
                i.wrap(obj)
        for i in docs.find_all("IonIcon"):
            if i.parent.name!="IonFabButton":
                iconlist.append(i)
        if len(iconlist)>0:
            obj = bs4.element.Tag(name="IonFabButton")
            docs.insert(0, obj)
            for i in iconlist:
                obj.append(i)
    return soup
def menuinit(soup):
    for docs in soup.find_all("statusbar"):
        docs.clear()
        docs.unwrap()
    for docs in soup.find_all("IonMenu"):
        for i in docs.find_all("blockheader"):
            i.name="h3"
            i.attrs['align']="center"
    return soup
def modalinit(soup):
    for docs in soup.find_all("IonModal"):
        for tool in docs.find_all("IonToolbar"):
            obj=bs4.element.Tag(name="IonHeader")
            tool.wrap(obj)
            for left in tool.find_all(attrs={'classname':'left'}):
                del left['classname']
                left.attrs['slot']="secondary"
            for right in tool.find_all(attrs={'classname': 'right'}):
                del right['classname']
                right.attrs['slot'] = "primary"
    return soup
def toolbarinit(soup):
    for docs in soup.find_all("IonToolbar"):
        if docs.parent.name!="IonHeader" and docs.parent.name!="IonFooter":
            obj = bs4.element.Tag(name="IonFooter")
            docs.wrap(obj)
    return soup
def buttoninit(soup):
    for docs in soup.find_all("listbutton"):
        docs.name="IonButton"
        docs.attrs['fill']="clear"
        docs.attrs['expand']="block"
    return soup
def ptrinit(soup):
    for docs in soup.find_all("IonContent"):
        if "ptr" in docs.attrs:
            docs.name="IonRefresherContent"
            obj=bs4.element.Tag(name="IonRefresher",attrs=docs.attrs)
            obj.attrs['slot']="fixed"
            del docs.attrs
            del obj['ptr']
            docs.wrap(obj)
            if "onptrrefresh" in obj.attrs:
                obj.attrs['onIonRefresh']=obj.attrs['onptrrefresh']
                del obj['onptrrefresh']
            obj1=bs4.element.Tag(name="IonContent")
            if not obj.findParent("IonContent"):
                obj.wrap(obj1)

    return soup
def sortableinit(soup):
    for docs in soup.find_all(attrs={'classname':'sortable-handler'}):
        obj=bs4.element.Tag(name="IonReorder",attrs={'slot':'end'})
        docs.parent.append(obj)
        docs.clear()
        docs.unwrap()
    for docs in soup.find_all("IonToolbar"):
       for b in docs.find_all("IonButton"):
           if "classname" in b.attrs:
               if "sortable-toggle" in b.attrs['classname']:
                   del b['classname']
    return soup
def searchinit(soup):
    for docs in soup.find_all("IonSearchbar"):
        if "backdrop" in docs.attrs:
            del docs['backdrop']
        if "clearbutton" in docs.attrs:
            if docs.attrs['clearbutton'].find("true")>-1:
                docs.attrs['clearIcon']="close-circle"
                del docs['clearbutton']
        if "disablebuttontext" in docs.attrs:
            docs.attrs['cancelButtonText']=docs.attrs['disablebuttontext']
            docs.attrs['showCancelButton']="focus"
            del docs['disablebuttontext']
        if "init" in docs.attrs:
            del docs['init']
        if "searchcontainer" in docs.attrs:
            del docs['searchcontainer']
        if "searchin" in docs.attrs:
            del docs['searchin']
    return soup
def tabsinit(soup):
    for docs in soup.find_all("IonToolbar"):
        if "tabbar" in docs.attrs:
            docs.name="IonTabBar"
            del docs['tabbar']
            if "bottommd" in docs.attrs:
                del docs['bottommd']
            docs.attrs['slot']="bottom"
        for a in docs.find_all("a") or docs.find_all("IonButton"):
            if "tablink" in a.attrs:
                link=a.attrs['tablink']
                if link[0]=="#":
                    link=link[1:]
                a.name="IonTabButton"
                a.attrs['tab']=link
                del a['tablink']
            if "tablinkactive" in a.attrs:
                a.attrs['selected']="true"
                del a['tablinkactive']
            if "labels" in docs.attrs:
                del docs['label']
                for i in a.find_all():
                    if "classname" in i.attrs:
                        if "tabbar-label" in i.attrs['class']:
                            del i['classname']
                            i.name="IonLabel"
    for docs in soup.find_all("IonTab"):
        if "id" in docs.attrs:
            docs.attrs['tab']=docs.attrs['id']
            del docs['id']
        if "tabactive" in docs.attrs:
            del docs['tabactive']
    return soup
def iconinit(soup):
    ionlist="add-circle-outline add-circle add alarm albums alert analytics apps archive arrow-back arrow-down arrow-dropdown-circle arrow-dropdown arrow-dropleft-circle arrow-dropleft arrow-dropright-circle arrow-dropright arrow-dropup-circle arrow-dropup arrow-forward arrow-round-back arrow-round-down arrow-round-forward arrow-round-up arrow-up at basket book bookmark briefcase browsers calculator calendar call camera card chatboxes chatbubbles checkmark-circle-outline checkmark-circle checkmark clock close-circle-outline close-circle close cloud-circle cloud-download cloud-outline cloud-upload cog compass contact contacts contrast create document download exit eye fastforward filing film flag flash folder-open folder heart heart-empty help-circle-outline help-circle home image images information-circle-outline information-circle keypad list-box list lock log-in log-out mail menu mic microphone more musical-note musical-notes navigate notifications-outline notifications options paper-plane paper pause person photos pie planet play-circle play pricetag pricetags pulse radio-button-off radio-button-on radio recording redo refresh-circle refresh remove-circle-outline remove-circle remove reorder rewind search send settings share-alt share star-outline star stopwatch text time timer today trash undo unlock videocam volume-high volume-low volume-mute volume-off logo-euro logo-facebook logo-github logo-googleplus logo-instagram logo-linkedin logo-rss logo-twitter logo-usd logo-yen".split(" ")
    f7list="add_round add_round_fill add alarm_fill albums_fill info_fill graph_round_fill layers_fill box_fill chevron_left chevron_down arrow_down_fill arrow_down_fill arrow_left_fill arrow_left_fill arrow_right_fill arrow_right_fill arrow_up_fill arrow_up_fill chevron_right arrow_left arrow_down arrow_right arrow_up chevron_up at bag_fill book_fill bookmark_fill briefcase_fill tabs_fill calendar_fill calendar phone_fill camera_fill card_fill chat_fill chats_fill check_round check_round_fill check stopwatch_fill close_round close_round_fill close cloud_fill cloud_download_fill cloud cloud_upload_fill settings compass_fill person persons circle_half compose_fill document_fill download_fill login_fill eye_fill fastforward_fill document_text_fill film_fill flag_fill bolt_fill folder_fill folder heart_fill heart help help_fill home_fill images images_fill info info_fill keyboard_fill list_fill menu lock_fill login logout email_fill bars misc_fill misc more_fill tune tune_fill navigation_fill bell bell_fill filter_fill paper_plane document_text pause_fill person photos_fill pie_fill world_fill play_round_fill play_fill tags tags_fill graph_square circle circle_fill radio tap forward_fill refresh_round_fill refresh_round delete_round delete_round_fill delete sort rewind_fill search_strong paper_plane_fill settings_fill share share_fill star star_fill stopwatch_fill chat time_fill timer today_fill trash_fill reply_fill unlock_fill videocam_fill volume_fill volume_low_fill volume_mute volume_mute_fill money_euro_fill social_facebook_fill social_github_fill social_googleplus social_instagram social_linkedin_fill social_rss_fill social_twitter_fill money_dollar_fill money_yen_fill".split(" ")
    for i in soup.find_all("i"):
        if "classname" in i.attrs:
            cls=i.attrs['classname']
            if "f7-icons" in cls:
                i.name="IonIcon"
                t=i.get_text().strip()
                if t in f7list:
                    i.attrs['name']=ionlist[f7list.index(t)]
                    i.clear()
                del i['classname']
    for i in soup.find_all("IonIcon"):
        if "f7" in i.attrs:
            t=i.attrs['f7']
            t=t.strip()
            if t in  f7list:
                i.attrs['name'] = ionlist[f7list.index(t)]
                del i['f7']
    return soup
def f7update(path):
    file=open(path,"r",encoding='utf-8')
    r1=file.read()
    file.close()
    soup=BeautifulSoup(r1,"html.parser")
    soup=changename(soup,"button","IonButton")
    soup=changename(soup,"segmented","IonSegment")
    soup = changename(soup, "row", "IonRow")
    soup = changename(soup, "col", "IonCol")
    soup = changename(soup, "page", "IonContent")
    soup = changename(soup, "block", "p")
    soup = changename(soup, "list", "IonList")
    soup = changename(soup, "listitem", "IonItem")
    soup = changename(soup, "listinput", "IonInput")
    soup = changename(soup, "listgroup", "IonItemGroup")
    soup = changename(soup, "icon", "IonIcon")
    soup = changename(soup, "card", "IonCard")
    soup = changename(soup, "cardcontent", "IonCardContent")
    soup = changename(soup, "cardfooter", "IonCardSubtitle")
    soup = changename(soup, "cardheader", "IonCardTitle")
    soup = changename(soup, "checkbox", "IonCheckbox")
    soup = changename(soup, "radio", "IonRadio")
    soup = changename(soup, "chip", "IonChip")
    soup = changename(soup, "fab", "IonFab")
    soup = changename(soup, "fabbutton", "IonFabButton")
    soup = changename(soup, "fabbuttons", "IonFabList")
    soup = changename(soup, "panel", "IonMenu")
    soup = changename(soup, "sheet", "IonModal")
    soup = changename(soup, "navtitle", "IonTitle")
    soup = changename(soup, "toolbar", "IonToolbar")
    soup = changename(soup, "link", "a")
    soup = changename(soup, "popover", "IonPopover")
    soup = changename(soup, "preloader", "IonSpinner")
    soup = changename(soup, "progressbar", "IonProgressBar")
    soup = changename(soup, "searchbar", "IonSearchbar")
    soup = changename(soup, "tabs", "IonTabs")
    soup = changename(soup, "tab", "IonTab")
    soup=changeattr(soup,"IonButton","fill","fill","solid")
    soup = changeattr(soup, "IonButton", "outline", "fill", "outline")
    soup = changeattr(soup, "IonButton", "round", "shape", "round")
    soup = changeattr(soup, "IonButton", "big", "size", "large")
    soup = changeattr(soup, "IonButton", "small", "size", "small")
    soup = changeattr(soup, "IonButton", "active", "checked", "")
    soup = changeattr(soup, "IonFabList", "position", "side", "-")
    soup = changeattr(soup, "IonMenu", "right", "side", "end")
    soup = changeattr(soup, "IonMenu", "left", "side", "start")
    soup = changeattr(soup, "IonMenu", "cover", "type", "overlay")
    soup = changeattr(soup, "IonMenu", "reveal", "type", "reveal")
    soup = changeattr(soup, "IonProgressBar", "progress", "value", "-")
    soup = delattr(soup,"IonButton","raised")
    soup = delattr(soup, "IonMenu", "reveal")
    soup = delattr(soup, "IonMenu", "cover")
    soup = delattr(soup, "IonMenu", "themedark")
    soup = delattr(soup, "IonSegment", "raised")
    soup = barinit(soup)
    soup = gridinit(soup)
    soup = listinit(soup)
    soup = inputinit(soup)
    soup = cardinit(soup)
    soup = chipinit(soup)
    soup = fabinit(soup)
    soup = menuinit(soup)
    soup = modalinit(soup)
    soup = buttoninit(soup)
    soup = ptrinit(soup)
#    soup = sortableinit(soup)
    soup = searchinit(soup)
    soup = tabsinit(soup)
    soup = iconinit(soup)
    soup = changeattr(soup, "p", "strong", "color", "light")
    s1=ionicfilter(soup)
    return s1
path="C:\\Users\\Administrator\\Desktop\\f7-final-test\\r\\src\\pages\\color-themes.jsx"
s1=f7update(path)
print(s1)