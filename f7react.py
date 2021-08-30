import re,pymysql,bs4,tkinter.messagebox
from bs4 import BeautifulSoup
from xml.sax.saxutils import unescape
def changename(soup,old,new):
    docs=soup.find_all(old)
    if docs:
        for d in docs:
            d.name=new
    return soup
def methods(s1,docs):
    eventlist='@accordion:beforeopen @accordion:open @accordion:opened @accordion:beforeclose @accordion:close @accordion:closed @actions:open @actions:opened @actions:close @actions:closed @click @dblclick @change @input:clear @textarea:resize @input:empty @input:notempty @mousedown @mouseup @mouseenter @mouseover @mouseleave @mouseout @mousemove @wheel @select @delete @focus @focusin @blur @focusout @beforeinput @input @submit @send @keypress @keyup @keydown @compositionstart @compositionupdate @compositionend @tab:show @tab:hide @sortable:enable @sortable:disable @sortable:sort @virtual:itembeforeinsert @virtual:itemsbeforeinsert @virtual:itemsafterinsert @virtual:beforeclear @swipeout @swipeout:open @swipeout:opened @swipeout:close @swipeout:closed @swipeout:delete @swipeout:deleted @swipeout:overswipeenter @swipeout:overswipeexit @listindex:select @loginscreen:open @loginscreen:opened @loginscreen:close @loginscreen:closed @attachment:click @attachment:delete @click:name @click:text @click:avatar @click:header @click:footer @click:bubble @back-click @click:back @page:mounted @page:init @page:reinit @page:beforein @page:afterin @page:beforeout @page:afterout @page:beforeunmount @page:beforeremove @ptr:pullstart @ptr:pullmove @ptr:pullend @ptr:refresh @ptr:done @infinite @panel:open @panel:opened @panel:close @panel:closed @panel:backdrop-click @panel:swipe @panel:swipeopen @panel:breakpoint @photobrowser:open @photobrowser:opened @photobrowser:close @photobrowser:closed @photobrowser:swipetoclose @popover:open @popover:opened @popover:close @popover:closed @popup:open @popup:opened @popup:close @popup:closed @range:change @range:changed @searchbar:search @searchbar:clear @searchbar:enable @searchbar:disable @click:clear @click:disable @sheet:open @sheet:opened @sheet:close @sheet:closed @sheet:stepopen @sheet:stepclose @sheet:stepprogress @stepper:change @stepper:minusclick @stepper:plusclick @toggle:change @view:init @swipeback:move @swipeback:beforechange @swipeback:afterchange @swipeback:beforereset @swipeback:afterreset @card:beforeopen @card:open @card:opened @card:close @card:closed @calendar:change @colorpicker:change @menu:opened @menu:closed @navbar:hide @navbar:show @navbar:collapse @navbar:expand @treeview:open @treeview:close @treeview:loadchildren'.split(' ')
    newlist='onAccordionBeforeOpen onAccordionOpen onAccordionOpened onAccordionBeforeClose onAccordionClose onAccordionClosed onActionsOpen onActionsOpened onActionsClose onActionsClosed onClick onDblclick OnChange onInputClear onTextareaResize onInputEmpty onInputNotempty OnMousedown onMouseup onMouseenter onMouseover onMouseleave onMouseout onMousemove onWheel onSelect onDelete onFocus onFocusin onBlur onFocusout onBeforeinput onInput onSubmit onSend onKeypress onKeyup onKeydown onCompostionstart onCompositionupdate onCompositionend onTabShow onTabHide onSortableEnable onSortableDisable onSortableSort onVirtualItemBeforeInsert onVirtualItemsBeforeInsert onVirtualItemsAfterInsert onVirtualBeforeClear onSwipeout onSwipeoutOpen onSwipeoutOpened onSwipeoutClose onSwipeoutClosed onSwipeoutDelete onSwipeoutDeleted onSwipeoutOverswipeEnter onSwipeoutOverswipeExit onListindexSelect onLoginscreenOpen onLoginscreenOpened onLoginscreenClose onLoginscreenClosed onAttachmentClick onAttachmentDelete onClickName onClickText onClickAvatar onClickHeader onClickFooter onClickBubble onBackClick onClickBack onPageMounted onPageInit onPageReinit onPageBeforeIn onPageAfterIn onPageBeforeOut onPageAfterOut onPageBeforeUnmount onPageBeforeRemove onPtrPullStart onPtrPullMove onPtrPullEnd onPrtRefresh onPrtDone onInfinite onPanelOpen onPanelOpened onPanelClose onPanelClosed onPanelBackdropClick onPanelSwipe onPanelSwipeOpen onPanelBreakpoint onPhotoBrowserOpen onPhotoBrowserOpened onPhotoBrowserClose onPhotoBrowserClosed onPhotoBrowserSwipeToClose onPopoverOpen onPopoverOpened onPopoverClose onPopoverClosed onPopupOpen onPopupOpened onPopupClose onPopupClosed onRangeChange onRangeChanged onSearchbarSearch onSearchbarClear onSearchbarEnable onSearchbarDisable onClcikClear onClickDisable onSheetOpen onSheetOpened onSheetClose onSheetClosed onSheetStepStepOpen onSheetStepClose onSheetStepProgress onStepperChange onStepperMinusClick onStepperPlusClick onToggleChange onViewInit onSwipebackMove onSwipeBackBeforeChange onSwipeBackAfterChange onSwipeBackBeforeReset onSwipeBackAfterReset onCardBeforeOpen onCardOpen onCardOpened onCardClose onCardClosed onCalendarChange onColorPickerChange onMenuOpened onMenuClosed onNavbarHide onNavbarShow onNavbarCollapse onNavbarExpand onTreeviewOpen onTreeviewClose onTreeviewLoadChildren'.split(' ')
    namelist = "App View Views Page Link Accordion AccordionItem AccordionToggle AccordionContent Badge Block BlockTitle BlockHeader BlockFooter Checkbox List ListItem ListInput Toggle Range ListGroup ListLabel ListButton Button ButtonsSegmented Segmented Tabs Tab Card CardHeader CardContent CardFooter Chip Fab FabButtons FabButton FabSpeedDial FabActions FabAction Icon FormLabel FormInput Row Col SwipeoutActions SwipeoutButton Searchbar Message Messages Messagebar Actions ActionsGroup ActionsLabel ActionsButton LoginScreen LoginScreenTitle PickerModal Popover Popup Navbar NavRight NavLeft NavTitle Toolbar Subnavbar Panel Preloader Progressbar Sheet Statusbar Swiper SwiperSlide Template7Template Timeline TimelineItem TimelineItemChild TimelineYear TimelineMonth".split(" ")
    varlist = []
    ind=0
    data=""
    mount=""
    for i in docs.find_all():
        m=0
        for j in eventlist:
            if j in i.attrs:
                #m = eventlist.index(j)
                n=newlist[m]
                i.attrs[n]="{this."+i.attrs[j]+".bind(this)}"
                del i[j]
            m=m+1
    strlist=s1.split('\n')
    for i in strlist:
        if i.find('data()')>-1:
            if strlist[ind].find('{')>-1 or strlist[ind+1].find('{')>-1:
                begin = strlist[ind]
                j = ind
                opener = begin.count('{')
                closer = begin.count('}')
                m = ""
                if begin.find('{') > -1:
                    j = j + 1
                    while j < len(strlist):
                        opener = opener + strlist[j].count('{')
                        closer = closer + strlist[j].count('}')
                        m = m + strlist[j] + "\n"
                        if opener == (closer):
                            if m[-2].find(",") > -1:
                                m = m[:-2]
                            break
                        j = j + 1
                data = m.replace('return', 'this.state = ')
                break
        ind=ind+1
    ind=0
    for i in strlist:
        if i.find('mounted()')>-1:
            if strlist[ind].find('{')>-1 or strlist[ind+1].find('{')>-1:
                strlist[ind]=strlist[ind].replace('mounted()','componentDidMount()')
                begin = strlist[ind]
                j = ind
                opener = begin.count('{')
                closer = begin.count('}')
                m = ""
                if begin.find('{') > -1:
                    while j < len(strlist):
                        opener = opener + strlist[j].count('{')
                        closer = closer + strlist[j].count('}')
                        m = m + strlist[j] + "\n"
                        if opener == (closer + 1):
                            if m[-2].find(",") > -1:
                                m = m[:-2]
                            break
                        j = j + 1
                mount = m
                break
        ind=ind+1
    m = ""
    ind=0
    funccount=0
    funclist=[]
    for i in strlist:
        if i.find('methods')>-1 and i.find(':')>-1:
            ind=strlist.index(i)
            begin = strlist[ind]
            j = ind
            opener = begin.count('{')
            closer = begin.count('}')
            if begin.find('{') > -1:
                j = j + 1
                while j < len(strlist):
                    if strlist[j].find('{') > -1:
                        opener = opener + 1
                    if strlist[j].find('}') > -1:
                        closer = closer + 1
                    m = m + strlist[j] + "\n"
                    if opener == (closer + 1):
                        if m[-2] == ",":
                            m = m[:-2]
                        if m not in funclist:
                            funclist.append(m)
                        m = ""
                        funccount = funccount + 1
                    j = j + 1
            break

    for i in docs.find_all():
        if i.name in namelist:
            if i.name not in varlist:
                varlist.append(i.name)
    header = "import React from 'react';\nimport {" + (", ").join(varlist) + "} from 'framework7-react';\n\n"
    header=header+"export default class extends React.Component {\nconstructor() {\nsuper();\n"+data+"\n}\nrender() {\nreturn (\n"
    temp=docs.find("template")
    if temp:
        temp.unwrap()
    script=docs.find("script")
    if script:
        script.clear()
        script.unwrap()
    s1=header+str(docs)+"\n);\n}\n"
    if mount.strip()!="":
        s1=s1+"\n"+mount
    for i in funclist:
        s1=s1+"\n"+i
    s1=s1+"\n}"
    s1=s1.replace('"{this.',"{this.").replace('.bind(this)}"',".bind(this)}").replace('=""',"")
    s1 = s1.replace('"{{', "{{").replace('}}"', "}}")
    s1 = s1.replace("=\"\"", "")
    s1 = s1.replace("=\"{true}\"", "={true}").replace("=\"{false}\"", "={false}")
    s1 = s1.replace(":clearButton=\"true\"", "clearButton={true}").replace(":clearButton=\"false\"","clearButton={false}")
    strlist = s1.split("\n")
    strlist = filter(None, strlist)
    s1 = "\n".join(strlist)
#    print(s1)
    return s1
def reactinit(soup):
    parname=[]
    parval=[]
    for docs in soup.find_all():
        attr = docs.attrs
        for i in attr:
            j = i.strip()
            if j != "":
                if j[0] == ":":
                    val = docs.attrs[i]
                    docs.attrs[j[1:]] = "{" + val + "}"
                    parname.append(j[1:])
                    parval.append(val)
                    del docs[i]
    s1 = str(soup)
    for i in parname:
        old="\"{"+parval[parname.index(i)]+"}\""
        new="{"+parval[parname.index(i)]+"}"
        s1=s1.replace(old,new)
        print(old,new)
    return s1
def reactfilter(soup):
    namelist="App View Views Page Link Accordion AccordionItem AccordionToggle AccordionContent Badge Block BlockTitle BlockHeader BlockFooter Checkbox List ListItem ListInput Toggle Range ListGroup ListLabel ListButton LoginScreenTitle Button ButtonsSegmented Segmented Tabs Tab Card CardHeader CardContent CardFooter Chip Fab FabButtons FabButton FabSpeedDial FabActions FabAction Icon FormLabel FormInput Row Col SwipeoutActions SwipeoutButton Searchbar Message Messages Messagebar Actions ActionsGroup ActionsLabel ActionsButton LoginScreen PickerModal Popover Popup Navbar NavRight NavLeft NavTitle Toolbar Subnavbar Panel Preloader Progressbar Sheet Statusbar Swiper SwiperSlide Template7Template Timeline TimelineItem TimelineItemChild TimelineYear TimelineMonth".split(" ")
    varlist=[]
    for docs in soup.find_all():
        if "class" in docs.attrs:
            docs.attrs['className']=docs.attrs['class']
            del docs['class']
        if "style" in docs.attrs:
            style=docs.attrs['style'].split(";")
            finval=""
            for i in style:
                if i.find(":")>-1:
                    elem=i.split(":")
                    if len(elem)>2:
                        h=elem[0]
                        n=i.replace(':',"",1).replace(h,"")
                    else:
                        n=elem[1]
                    if elem[0]=="background-color":
                        elem[0]="backgroundColor"
                    if elem[0]=="vertical-align":
                        elem[0]="verticalAlign"
                    if elem[0]=="background-image":
                        elem[0]="background"
                    elem[0]=elem[0].replace("background-color","backgroundColor").replace("vertical-align","verticalAlign").replace("background-image","background")
                    elem[0]=elem[0].replace("margin-left","marginLeft").replace("margin-right","marginRight").replace("margin-top","margin-top").replace("margin-bottom","marginBottom")

                    val=elem[0].strip()+":'"+n.strip()+"'"
                    finval=finval+val+","
            if finval!="":
                docs.attrs['style']="{{"+finval[:-1]+"}}"
    s1 = str(soup)

    s1 = s1.replace('"{{',"{{").replace('}}"',"}}")
    s1 = s1.replace("=\"\"","")
    s1 = s1.replace("=\"{{{true}}}\"","={true}").replace("=\"{{{false}}}\"","={false}")
    s1=s1.replace('"{{{',"{").replace('}}}"',"}")
    s1 = s1.replace(":clearButton=\"true\"","clearButton={true}").replace(":clearButton=\"false\"","clearButton={false}")
    #s1 = s1.replace("=\"\\{-","={").replace("-\\}\"","}")
    strlist = s1.split("\n")
    strlist = filter(None, strlist)
    s1 = "\n".join(strlist)
    if not soup.find("script"):
        for i in soup.find_all():
            if i.name in namelist:
                if i.name not in varlist:
                    varlist.append(i.name)
        header="import React from 'react';\nimport {"+(", ").join(varlist)+"} from 'framework7-react';\n\nexport default () => (\n"+s1.replace("<template>","").replace("</template>","")+"\n);"
        s1=header
    else:
        docs=soup.find("template")
        docs=str(docs)
        script=reactinit(soup).replace(docs+"\n","").replace(docs,"")
        if script.find("export default")>-1:
            script=script.replace("export default","")
        script=methods(script,soup)
        s1=script
    return s1
def classout(soup,elem,clsname,attrname):
    for docs in soup.find_all(elem,attrs={'class':clsname}):
        cls=docs.attrs['class']
        cls.remove(clsname)
        if len(cls)<1:
            del docs['class']
        docs.attrs[attrname]=""
    return soup
def attrinit(soup,elem,attrname):
    for docs in soup.find_all(elem):
        if attrname in docs.attrs:
            val = docs.attrs[attrname]
            docs.attrs[val]=""
            del docs[attrname]
    return soup
def changeattrname(soup,elem,old,new):
    for docs in soup.find_all(elem):
        if old in docs.attrs:
            docs.attrs[new]=docs.attrs[old]
            del docs[old]
    return soup
def f7update(path):
    code_file = open(path, "r", encoding='utf-8')
    code = code_file.read()
    code_file.close()
    soup = BeautifulSoup(code, "html.parser")
    soup = changename(soup, "f7-app", "App")
    soup = changename(soup, "f7-view", "View")
    soup = changename(soup, "f7-views", "Views")
    soup = changename(soup, "f7-page", "Page")
    soup = changename(soup, "f7-pages", "Pages")
    soup = changename(soup, "f7-link", "Link")
    soup = changename(soup, "f7-accordion", "Accordion")
    soup = changename(soup, "f7-accordion-item", "AccordionItem")
    soup = changename(soup, "f7-accordion-toggle", "AccordionToggle")
    soup = changename(soup, "f7-accordion-content", "AccordionContent")
    soup = changename(soup, "f7-badge", "Badge")
    soup = changename(soup, "f7-block", "Block")
    soup = changename(soup, "f7-block-title", "BlockTitle")
    soup = changename(soup, "f7-block-header", "BlockHeader")
    soup = changename(soup, "f7-block-footer", "BlockFooter")
    soup = changename(soup, "f7-checkbox", "Checkbox")
    soup = changename(soup, "f7-list", "List")
    soup = changename(soup, "f7-button", "Button")
    soup = changename(soup, "f7-buttons", "ButtonsSegmented")
    soup = changename(soup, "f7-segmented","Segmented")
    soup = changename(soup, "f7-tabs", "Tabs")
    soup = changename(soup, "f7-tab", "Tab")
    soup = changename(soup, "f7-card", "Card")
    soup = changename(soup, "f7-card-header", "CardHeader")
    soup = changename(soup, "f7-card-content", "CardContent")
    soup = changename(soup, "f7-card-footer", "CardFooter")
    soup = changename(soup, "f7-chip", "Chip")
    soup = changename(soup, "f7-fab", "Fab")
    soup = changename(soup, "f7-fab-buttons", "FabButtons")
    soup = changename(soup, "f7-fab-button", "FabButton")
    soup = changename(soup, "f7-fab-speed-dial", "FabSpeedDial")
    soup = changename(soup, "f7-fab-actions", "FabActions")
    soup = changename(soup, "f7-fab-action", "FabAction")
    soup = changename(soup, "f7-icon", "Icon")
    soup = changename(soup, "f7-list-item", "ListItem")
    soup = changename(soup,"f7-list-input","ListInput")
    soup = changename(soup, "f7-label", "FormLabel")
    soup = changename(soup, "f7-input", "FormInput")
    soup = changename(soup, "f7-grid", "Row")
    soup = changename(soup, "f7-row", "Row")
    soup = changename(soup, "f7-col", "Col")
    soup = changename(soup, "f7-list-group", "ListGroup")
    soup = changename(soup, "f7-list-label", "ListLabel")
    soup = changename(soup, "f7-list-button", "ListButton")
    soup = changename(soup, "f7-swipeout-actions", "SwipeoutActions")
    soup = changename(soup, "f7-swipeout-button", "SwipeoutButton")
    soup = changename(soup, "f7-searchbar", "Searchbar")
    soup = changename(soup, "f7-message", "Message")
    soup = changename(soup, "f7-messages", "Messages")
    soup = changename(soup, "f7-messagebar", "Messagebar")
    soup = changename(soup, "f7-actions", "Actions")
    soup = changename(soup, "f7-actions-group", "ActionsGroup")
    soup = changename(soup, "f7-actions-label", "ActionsLabel")
    soup = changename(soup, "f7-actions-button", "ActionsButton")
    soup = changename(soup, "f7-login-screen", "LoginScreen")
    soup = changename(soup, "f7-login-screen-title", "LoginScreenTitle")
    soup = changename(soup, "f7-picker-modal", "PickerModal")
    soup = changename(soup, "f7-popover", "Popover")
    soup = changename(soup, "f7-popup", "Popup")
    soup = changename(soup, "f7-navbar", "Navbar")
    soup = changename(soup, "f7-nav-right", "NavRight")
    soup = changename(soup, "f7-nav-left", "NavLeft")
    soup = changename(soup, "f7-nav-title", "NavTitle")
    soup = changename(soup, "f7-toolbar", "Toolbar")
    soup = changename(soup, "f7-subnavbar", "Subnavbar")
    soup = changename(soup, "f7-panel", "Panel")
    soup = changename(soup, "f7-preloader", "Preloader")
    soup = changename(soup, "f7-progressbar", "Progressbar")
    soup = changename(soup, "f7-statusbar", "Statusbar")
    soup = changename(soup, "f7-swiper", "Swiper")
    soup = changename(soup, "f7-swiper-slide", "SwiperSlide")
    soup = changename(soup, "t7-template", "Template7Template")
    soup = changename(soup, "f7-timeline", "Timeline")
    soup = changename(soup, "f7-timeline-item", "TimelineItem")
    soup = changename(soup, "f7-timeline-item-child", "TimelineItemChild")
    soup = changename(soup, "f7-timeline-year", "TimelineYear")
    soup = changename(soup, "f7-timeline-month", "TimelineMonth")
    soup = changename(soup,"f7-sheet","Sheet")
    soup = changename(soup, "f7-range", "Range")
    soup = changename(soup, "f7-toggle", "Toggle")
    soup = classout(soup,"Panel","theme-dark","themeDark")
    soup = classout(soup, "Panel", "panel-reveal", "reveal")
    soup = classout(soup, "Panel", "panel-right", "right")
    soup = changeattrname(soup,"Navbar","back-link","backLink")
    soup = changeattrname(soup,"Navbar","back-link-url","backLinkUrl")
    soup = changeattrname(soup, "NavLeft", "back-link", "backLink")
    soup = changeattrname(soup, "NavLeft", "back-link-url", "backLinkUrl")
    soup = changeattrname(soup, "Toolbar", ":bottom-md", ":bottomMd")
    soup = changeattrname(soup, "Link", "tab-link", "tabLink")
    soup = changeattrname(soup, "Link", "tab-link-active", "tabLinkActive")
    soup = changeattrname(soup, "Link", "icon-only", "iconOnly")

    soup = changeattrname(soup, "Link","icon-f7","iconF7")
    soup = changeattrname(soup, "Link","panel-open","panelOpen")
    soup = changeattrname(soup,"Link","panel-close","panelClose")
    soup = changeattrname(soup, "Link", "actions-open", "actionsOpen")
    soup = changeattrname(soup, "Link", "actions-close", "actionsClose")
    soup = changeattrname(soup, "Link", "popup-open", "popupOpen")
    soup = changeattrname(soup, "Link", "popup-close", "popupClose")
    soup = changeattrname(soup, "Link", "popover-open", "popoverOpen")
    soup = changeattrname(soup, "Link", "popover-close", "popoverClose")
    soup = changeattrname(soup, "Link", "sheet-open", "sheetOpen")
    soup = changeattrname(soup, "Link", "sheet-close", "sheetClose")
    soup = changeattrname(soup, "Link", "login-screen-open", "loginScreenOpen")
    soup = changeattrname(soup, "Link", "login-screen-close", "loginScreenClose")
    soup = changeattrname(soup, "Link", "sortable-enable","sortableEnable")
    soup = changeattrname(soup, "Link", "sortable-disable", "sortableDisable")
    soup = changeattrname(soup, "Link", "sortable-toggle", "sortableToggle")
    soup = changeattrname(soup, "Link", "searchbar-enable","searchbarEnable")
    soup = changeattrname(soup, "Link", "searchbar-disable", "searchbarDisable")
    soup = changeattrname(soup, "Link", "searchbar-toggle", "searchbarToggle")
    soup = changeattrname(soup,"Link","searchbar-clear","searchbarClear")
    soup = changeattrname(soup, "Button", "tab-link", "tabLink")
    soup = changeattrname(soup, "Button", "tab-link-active", "tabLinkActive")

    soup = changeattrname(soup, "Button","panel-open","panelOpen")
    soup = changeattrname(soup,"Button","panel-close","panelClose")
    soup = changeattrname(soup, "Button", "actions-open", "actionsOpen")
    soup = changeattrname(soup, "Button", "actions-close", "actionsClose")
    soup = changeattrname(soup, "Button", "popup-open", "popupOpen")
    soup = changeattrname(soup, "Button", "popup-close", "popupClose")
    soup = changeattrname(soup, "Button", "popover-open", "popoverOpen")
    soup = changeattrname(soup, "Button", "popover-close", "popoverClose")
    soup = changeattrname(soup, "Button", "sheet-open", "sheetOpen")
    soup = changeattrname(soup, "Button", "sheet-close", "sheetClose")
    soup = changeattrname(soup, "Button", "login-screen-open", "loginScreenOpen")
    soup = changeattrname(soup, "Button", "login-screen-close", "loginScreenClose")
    soup = changeattrname(soup, "Button", "sortable-enable","sortableEnable")
    soup = changeattrname(soup, "Button", "sortable-disable", "sortableDisable")
    soup = changeattrname(soup, "Button", "sortable-toggle", "sortableToggle")
    soup = changeattrname(soup, "Button", "searchbar-enable","searchbarEnable")
    soup = changeattrname(soup, "Button", "searchbar-disable", "searchbarDisable")
    soup = changeattrname(soup, "Button", "searchbar-toggle", "searchbarToggle")
    soup = changeattrname(soup,"Button","searchbar-clear","searchbarClear")
    soup = changeattrname(soup, "Button", "data-popover", "popoverOpen")
    soup = changeattrname(soup,"List","inline-labels","inlineLabels")
    soup = changeattrname(soup, "List", "accordion-list", "accordionList")
    soup = changeattrname(soup, "List", "media-list", "mediaList")
    soup = changeattrname(soup, "List", "links-list", "linksList")
    soup = changeattrname(soup, "List", "simple-list", "simpleList")
    soup = changeattrname(soup, "List", "sortable-enabled", "sortableEnabled")
    soup = changeattrname(soup, "List", "contacts-list", "contactsList")
    soup = changeattrname(soup, "List", "form-store-data", "formStoreData")
    soup = changeattrname(soup, "List", "virtual-list", "virtualList")
    soup = changeattrname(soup, "List", "no-hairlines", "noHairlines")
    soup = changeattrname(soup, "List", "no-hairlines-md", "noHairlinesMd")
    soup = changeattrname(soup, "List", "no-hairlines-ios", "noHairlinesIos")
    soup = changeattrname(soup, "ListItem", "group-title", "groupTitle")
    soup = changeattrname(soup, "ListItem", "smart-select", "smartSelect")
    soup = changeattrname(soup, "ListItem", "accordion-item", "accordionItem")
    soup = changeattrname(soup, "ListItem", "badge-color", "badgeColor")
    soup = changeattrname(soup, "Chip", "media-bg-color", "mediaBgColor")
    soup = changeattrname(soup, "Chip", "media-text-color", "mediaTextColor")
    soup = changeattrname(soup, "Chip", "@click", "onClick")
    soup = changeattrname(soup, "Chip", "@delete", "onDelete")
    soup = changeattrname(soup, "Checkbox", "checkbox","")
    soup = changeattrname(soup, "Col", "tablet-width", "tabletWidth")
    soup = changeattrname(soup, "Col", "desktop-width", "desktopWidth")
    soup = changeattrname(soup, "Row", "no-gap", "noGap")
    soup = changeattrname(soup, "SwipeoutButton", "confirm-text", "confirmText")
    soup = changeattrname(soup, "Searchbar", ":clear-button", ":clearButton")
    soup = changeattrname(soup, "Searchbar", "disable-link-text", "disableButtonText")
    soup = changeattrname(soup, "Searchbar", "search-container", "searchContainer")
    soup = changeattrname(soup, "Searchbar", "search-in", "searchIn")
    soup = changeattrname(soup, "Tab", "tab-active", "tabActive")

    soup = changeattrname(soup, "Page", "data-distance", "infiniteDistance")
    soup = changeattrname(soup, "Page", "login-screen", "loginScreen")
    soup = changeattrname(soup, "Page", "no-swipeback", "noSwipeback")
    soup = changeattrname(soup, "Page", "with-subnavbar", "withSubnavbar")
    soup = changeattrname(soup, "Page", "no-navbar", "noNavbar")
    soup = changeattrname(soup, "Page", "no-toolbar", "noToolbar")
    soup = changeattrname(soup, "Page", "hide-bars-on-scroll", "hideBarsOnScroll")
    soup = changeattrname(soup, "Page", "hide-navbar-on-scroll", "hideNavbarOnScroll")
    soup = changeattrname(soup, "Page", "hide-toolbar-on-scroll", "hideToolbarOnScroll")
    soup = changeattrname(soup, "Page", "ptr-distance", "ptrDistance")
    soup = changeattrname(soup, "Page", "ptr-preloader", "ptrPreloader")
    soup = changeattrname(soup, "Page", "infinite-preloader", "infinitePreloader")
    soup = changeattrname(soup, "Page", "infinite-top", "infiniteTop")
    soup = changeattrname(soup, "Page", "data-distance", "infiniteDistance")
    soup = changeattrname(soup, "Page", "infinite-distance", "infiniteDistance")
    soup = changeattrname(soup, "Page", "tab-active", "tabActive")
    soup = changeattrname(soup, "Page", "@ptr:refresh",":onPtrRefresh")

    soup = changeattrname(soup,"View",":ios-dynamic-navbar",":iosDynamicNavbar")
    soup = attrinit(soup,"Panel","side")
    s1 = reactfilter(soup)
    return s1
#path="C:\\Users\\Administrator\\Desktop\\f7-final-test\\vue\\f7-test\\src\\pages\\grid.vue"
#path="C:\\Users\\Administrator\\Desktop\\bianli\\untitled\\F7_files\\vue\\src\\app.vue"
#s1=f7update(path)
#print(s1)