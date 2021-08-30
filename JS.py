import re,pymysql
def jstrans(fname):
    #-----------------------------------------------------数据库-------------------------------------------------------#
    conn = pymysql.connect(user='root', passwd='',host='localhost', db='f7update')
    cur = conn.cursor()
    cur1 = conn.cursor()
    oldappparam=[]
    newappparam=[]
    appparampar=[]
    cur.execute("SELECT * FROM f7jsappparam WHERE version='v2'")
    for r in cur:
        oldappparam.append(r[1])
        newappparam.append(r[2])
        appparampar.append(r[4])
    oldjsparam=[]
    newjsparam=[]
    jsparampar=[]
    cur.execute("SELECT * FROM f7jsparam WHERE version='v2' ORDER BY parent")
    for r in cur:
        oldjsparam.append(r[1])
        newjsparam.append(r[2])
        jsparampar.append(r[4])
    oldjsmethod=[]
    newjsmethod=[]
    jsmethodpar=[]
    jsmethodcur=[]
    cur.execute("SELECT * FROM f7jsmethod WHERE version='v2'")
    for r in cur:
        oldjsmethod.append(r[1])
        newjsmethod.append(r[2])
        jsmethodpar.append(r[4])
        jsmethodcur.append(r[5])
    oldjsevent=[]
    newjsevent=[]
    cur.execute("SELECT * FROM f7jsevents WHERE version='v2'")
    for r in cur:
        oldjsevent.append(r[1])
        newjsevent.append(r[2])
    oldonevent=[]
    newonevent=[]
    oneventpar=[]
    cur.execute("SELECT * FROM f7onevent WHERE version='v2'")
    for r in cur:
        oldonevent.append(r[1])
        newonevent.append(r[2])
        oneventpar.append(r[4])
    oldlist=[]
    newlist=[]
    cur.execute("SELECT * FROM f7rename WHERE version='v1'")
    for r in cur:
        oldlist.append(r[1])
    cur.execute("SELECT * FROM f7rename WHERE version='v2'")
    for r in cur:
        newlist.append(r[1])
    def paramchange(m,oldp,newp):
        pattern=oldp+"\s*:"
        m=re.sub(pattern,newp+":",m)
        return m
    def specparam(m,oldp,oldv,newv):
        pattern = oldp + "\s*:\s*"+oldv
        m=re.sub(pattern,oldp+": "+newv,m)
        return m
    def funcwrap (m,param):
        pattern = param+":.*"
        find=re.search(pattern,m,flags=re.DOTALL)
        if find:
            find=find.group()
            find=funccloser(find)
            oldfind=find[1:]
            newfind="on:{\n"+oldfind+"\n}"
            if m.find(newfind)<0:
                m=m.replace(oldfind,newfind)
        return m
    def paramwrap(m,param,parent):
        pattern = param + "\s*:\s*(.*),"
        fullparam = re.search(pattern, m)
        if fullparam:
            fullparam = fullparam.group()
        else:
            fullparam = ""
        if m.find(parent+":{")<0:
            if fullparam.strip()!="":
                par=parent+":{\n"+fullparam+"\n},"
                m=m.replace(fullparam,par)
        else:
            par=parent+":{\n"
            if fullparam.strip() != "":
                m=m.replace(fullparam,"")
                m=m.replace(par,par+fullparam+"\n")
        return m

    def getvar(m,pattern):
        varlist=[]
        m1 = re.findall(pattern, m)
        if m1:
            for i in m1:
                varlist.append(i.strip())
        return varlist
    def autocompleteinit(h):
        strlist = h.split("\n")
        ind = 0
        for i in strlist:
            strlist[ind] = strlist[ind].replace("  ", " ").replace(" ,", ",")
            strlist[ind] = strlist[ind].replace(" :",":")
            ind=ind+1
        ind=0
        for i in strlist:
            if i.find("source") > -1:
                if i.find("function") > -1 and i.find("autocomplete") > -1:
                    strlist[ind] = strlist[ind].replace("autocomplete,", "")
                    if i.find("{")>-1:
                        strlist[ind]=strlist[ind].replace("{","{\nvar autocomplete=this;",1)
                    else:
                        strlist[ind+1] = strlist[ind+1].replace("{", "{\nvar autocomplete=this;", 1)
                if strlist[ind + 1].find("function") > -1 and strlist[ind + 1].find("autocomplete") > -1:
                    strlist[ind + 1] = strlist[ind + 1].replace("autocomplete,", "")
                    if strlist[ind + 1].find("{")>-1:
                        strlist[ind + 1] = strlist[ind + 1].replace("{","{\nvar autocomplete=this;",1)
                    else:
                        strlist[ind+2] = strlist[ind+2].replace("{", "{\nvar autocomplete=this;", 1)
            if i.find("openerEl")>-1:
                if i.find("$$(")>-1 and i.find(")")>-1:
                    strlist[ind]=strlist[ind].replace("$$(","",1).replace(")","",1)
                else:
                    strlist[ind + 1] = strlist[ind + 1].replace("$$(","",1).replace(")","",1)
            if i.find("function") > -1 and i.find("autocomplete") > -1:
                strlist[ind] = strlist[ind].replace("function (autocomplete,", "function (").replace("function(autocomplete,", "function (")
            ind = ind + 1
        ind = 0
        for i in strlist:
            strlist[ind] = strlist[ind].replace("query.toLowerCase", "query.toString().toLowerCase")
            strlist[ind] = strlist[ind].replace("autocomplete.hidePreloader", "autocomplete.preloaderHide").replace("autocomplete.showPreloader", "autocomplete.preloaderShow")
            strlist[ind] = strlist[ind].replace("backOnSelect", "closeOnSelect")
            strlist[ind] = strlist[ind].replace("( ","(")
            if i.find("opener:")>-1:
                strlist[ind]=strlist[ind].replace("opener:","openerEl:")
            ind = ind + 1


        h = "\n".join(strlist)
        return h
    def valfilter(varval):
        j = -1
        for i in varval:
            j = j + 1
            if i.count("(") > 1:
                ind = i.find("(")
                i = i[:ind]
            varval[j] = appname + i + "("
        return varval
    def methodfilter(h):
        i = 0
        len1 = len(varname)
        while (i < len1):
            old = "var\s*" + varname[i] + "\s*=\s*" + varval[i]
            new = "var " + varname[i] + " = " + newval[i]
            old = old.replace("(", "\(")
            old = old.replace(")", "\)")
            new = new.replace("(", "\(")
            new = new.replace(")", "\)")
            h = re.sub(old, new, h, flags=re.DOTALL)
            h = h.replace("\(", "(")
            h = h.replace("\)", ")")
            i = i + 1
        return h
    def jsfilter(m):
        c=m.split("\n")
        m=""
        for i in c:
            if i.strip()!="":
                m=m+"\n"+i
        return m
    def funccloser(m):
        str1 = m.split("\n")
        m = ""
        opener = 0
        for i in str1:
            m = m + "\n" + i
            opener = opener + i.count("{")
            opener = opener - i.count("}")
            if opener == 0:
                break
        return m
    def jshtml(h):
        m = re.findall("\'(.*)\'", h)
        if m:
            for i in m:
                for j in oldlist:
                    if j in i:
                        old = "." + oldlist[oldlist.index(j)]
                        new = "." + newlist[oldlist.index(j)]
                        pattern = i
                        i = i.replace(old, new)
                        pattern = pattern.replace("(", "\(").replace(")", "\)")
                        h = re.sub(pattern, i, h)
        m = re.findall("\"(.*)\"", h)
        if m:
            for i in m:
                for j in oldlist:
                    if j in i:
                        old = "." + oldlist[oldlist.index(j)]
                        new = "." + newlist[oldlist.index(j)]
                        pattern = i
                        i = i.replace(old, new)
                        pattern = pattern.replace("(", "\(").replace(")", "\)")
                        h = re.sub(pattern, i, h)
        h=h.replace("pull-to-refresh-content","ptr-content")
        return h
    def errorfilter(h):
        h=h.replace("ElElEl","El")
        h = h.replace("ElEl", "El")
        h=h.replace("input:","inputEl:")
        strlist = h.split("\n")
        a = ""
        for line in strlist:
            data = line.strip()
            if len(data) != 0:
                a = a + data + "\n"
        h = a
        h = h.replace("(page.container).find","")
        return h
    def onfunc(h,paramparlist):
        k = 0
        for i in newparamlist:
            for j in oldonevent:
                ind = oldonevent.index(j)
                jsevent = oneventpar[ind]
                if (i.find(j) > -1) and (jsevent == paramparlist[k]):
                    pattern = j + ".*\{.*\}"
                    m = re.findall(pattern, h, re.DOTALL)
                    if m:
                        for n in m:
                            onevent = funccloser(n)
                            if (onevent[-1] == ","):
                                onevent = onevent[:-1]
                            if (onevent[0].strip() == ""):
                                onevent = onevent[1:]
                            old = onevent  # .replace("(","\(").replace(")","\)")
                            onevent = onevent.replace(j, newonevent[oldonevent.index(j)])
                            onevent = "on:{\n" + onevent + "\n}"
                            if (h.find(old) > -1):
                                h = h.replace(old, onevent)
            newparamlist[k] = i
            k = k + 1
        return h
    def pickerinit(h):
        pattern = ".*"+appname+".picker.create\(.*\);"
        m = re.findall(pattern, h)
        ind = 0
        if m:
            for i in m:
                old = i
                if len(m) > 1:
                    ind = ind + 1
                else:
                    ind = ""
                s1 = "var picker" + str(ind) + "=" + i.strip()
                p = appname+".picker.create\((.*)\);"
                k = re.findall(p, i)
                k = ("").join(k)
                i = i.replace(i, s1)
                i = i.replace(k, "{\ninputEl: " + k + "\n}")
                i = i.replace(i, i + "\npicker" + str(ind) + ".open();")
                h = h.replace(old, i)
        #formatValue: function (p, values, displayValues)
        strlist=h.split("\n")
        ind=0
        for i in strlist:
            if i.find("formatValue:")>-1 and i.find("function")>-1:
                strlist[ind] = strlist[ind].replace("(p, ","(")
            ind=ind+1
        h="\n".join(strlist)
        return h
    def actioninit(h):
        pattern = ".*"+appname+".actions.create\(.*\);"
        m = re.findall(pattern, h)
        ind = 0
        if m:
            for i in m:
                old = i
                if len(m) > 1:
                    ind = ind + 1
                else:
                    ind = ""
                s1 = "var act" + str(ind) + "=" + i.strip()
                p = appname+".actions.create\((.*)\);"
                k = re.findall(p, i)
                k = ("").join(k)
                newk = k
                if k.find("this") > -1:
                    newk = k.replace("this", "").strip()
                    if newk[0] == ",":
                        newk = newk[1:].strip()
                    newk = newk + ",\n" + "forceToPopover: true"
                i = i.replace(i, s1)
                i = i.replace(k, "{\nbuttons: " + newk + "\n}")
                i = i.replace(i, i + "\nact" + str(ind) + ".open();")
                h = h.replace(old, i)
        return h
    def find_repeat(source,elmt): # The source may be a list or string.
        elmt_index=[]
        s_index = 0;e_index = len(source)
        while(s_index < e_index):
            try:
                temp = source.index(elmt,s_index,e_index)
                elmt_index.append(temp)
                s_index = temp + 1
            except ValueError:
                break
        return elmt_index
    def findnotification(h):
        pattern = appname+".notification.create\s*\(\s*\{.*"
        m = re.search(pattern, h, re.DOTALL)
        if m:
            m=m.group()
            m=funccloser(m)[1:]
        return m
    def virtuallistinit(h):
        pattern = "virtualList.create\s*\((.*)\{"
        m = re.findall(pattern, h)
        if m:
            for i in m:
                j = re.search("'(.*)'", i)
                if j:
                    j = j.group()
                else:
                    j = re.search("\"(.*)\"", i).group()
                h = h.replace("(" + i + "{", "({\nel: " + j+",")
        return h
    def messageinit(h):
        strlist=h.split("\n")
        ind=0
        v=""
        for i in strlist:
            if i.find("messages.create('")>-1 and i.find(")")>-1:
                s1="firstMessageRule: function (message, previousMessage, nextMessage) {\n"
                s1=s1+"if (message.isTitle) return false;\n"
                s1=s1+"if (!previousMessage || previousMessage.type !== message.type || previousMessage.name !== message.name) return true;\nreturn false;\n},\n"
                s1=s1+"lastMessageRule: function (message, previousMessage, nextMessage) {\n"
                s1=s1+"if (message.isTitle) return false;\n"
                s1=s1+"if (!nextMessage || nextMessage.type !== message.type || nextMessage.name !== message.name) return true;\nreturn false;\n},\n"
                s1=s1+"tailMessageRule: function (message, previousMessage, nextMessage) {\n"
                s1=s1+"if (message.isTitle) return false;\n"
                s1=s1+"if (!nextMessage || nextMessage.type !== message.type || nextMessage.name !== message.name) return true;\nreturn false;\n}\n"
                strlist[ind] = strlist[ind].replace("messages.create('","messages.create({\nel:'").replace("')","',"+s1+"})")
            if i.find("messagebar.create('") > -1 and i.find(")") > -1:
                var=re.findall("(.*)=\s*messagebar.create",i)
                if var:
                    for v in var:
                        v=v.replace("var ","").strip()
                        break
                strlist[ind] = strlist[ind].replace("messagebar.create('", "messagebar.create({\nel:'").replace("')", "'})")
            if i.find(v+".value()")>-1:
                strlist[ind] = strlist[ind].replace(v+".value()",v+".getValue().replace(/\\n/g, '<br>').trim()")
            ind=ind+1
        ind=0
        for i in strlist:
            if i.find(".addMessage(")>-1:
                j=ind
                while j<len(strlist):
                    if strlist[j].find("}")>-1:
                        break
                    if strlist[j].find("day:")>-1:
                        strlist[j]=strlist[j].replace("day:","title:")
                    j=j+1
            ind=ind+1
        ind=0
        for i in strlist:
            if i.find(".addMessage(") > -1:
                s1="senddate=!conversationStarted ? 'Today' :'';\n"
                s1=s1+"sendtime=!conversationStarted ? (new Date()).getHours() + ':' + (new Date()).getMinutes() :''\n"
                s1=s1+"title=senddate+\", <span>\"+sendtime+\"</span>\";\n"
                s1=s1+"myMessages.addMessage({\nisTitle: true,\ntype:'sent',\ntext:title\n});\n"
                strlist[ind]=s1+strlist[ind]
                break
            ind=ind+1
        h="\n".join(strlist)
        return h
    def notificationinit(h):
        indexlist=[]
        ind = 0
        indexlist=find_repeat(h,appname+".notification.create")
        for i in indexlist:
            breakout=len(indexlist)
            breakout=0.5*breakout-1
            if ind>breakout:
                break
            ind = ind + 1
            i=find_repeat(h,appname+".notification.create")[ind]
            #len1=i-len("myApp.notification.create")
            m=findnotification(h[i:])
            oldm=m
            newm=oldm.replace(oldm,"var notification"+str(ind)+"="+oldm)
            newm=paramchange(newm,"message","text")
            newm=paramchange(newm,"media","icon")
            newm=paramchange(newm,"onClose","close")
            newm=funcwrap(newm,"close")
            newm=newm.replace(newm,newm+"\nnotification"+str(ind)+".open();")
            h=h.replace(oldm,newm)
        h=h.replace(appname+".notification.create({", appname+".notification.create({\n" + "closeButton:true,")
        return h
    def swiperinit(h):
        h = paramchange(h, "nextButton", "nextEl")
        h = paramwrap(h, "nextEl", "navigation")
        h = paramchange(h, "prevButton", "prevEl")
        h = paramwrap(h, "prevEl", "navigation")
        var = re.findall("(.*)=\s*" + appname + ".swiper.create", h)
        if var:
            for i in var:
                i = i.replace("var", "").strip()
                old = i + ".params.control"
                new = i + ".controller.control"
                h = h.replace(old, new)

        return h

#----------------------------------------------读取页面-------------------------------------------------------------#
    html_code=open(fname,"r",encoding='utf-8')
    h=html_code.read()
    html_code.close()
    a=h.split("\n")
    h=""
    for i in a:
        h=h+"\n"+i
    pattern=r".*?\s*=\s*new\s*Framework7"
    m=re.search(pattern,h)
    if m:
        m=m.group()
        h=re.sub(pattern+"\s*\(\s*\{",m+"({\n"+"root: '#app',\n"+"routes: routes,",h)
        m=re.sub("=\s*new\s*Framework7","",m)
        appname=m.replace("var ","").strip()
    #--------------------------------------------APPparam---------------------------------------------------------------#
    pattern=appname+"\s*=\s*new\s*Framework7+\(*\{.*"
    m=re.search(pattern,h,flags=re.DOTALL)
    if m:
        m=m.group()
        str1 = m.split("\n")
        m = ""
        opener = 0
        close = 0
        ind = 0
        for i in str1:
            m = m + "\n" + i
            ind = ind + 1
            opener = opener + i.count("{")
            opener = opener - i.count("}")
            close = close + i.count("}")
            if opener == 0:
                break
        closestr = ""
        while ind < len(str1):
            closestr = closestr + "\n" + str1[ind]
            ind = ind + 1
        f7old=m
        for i in oldappparam:
            ind=oldappparam.index(i)
            if appparampar[ind].strip()!="" and appparampar[ind].strip()!="-":
                m=paramwrap(m,oldappparam[ind],appparampar[ind])
            m=paramchange(m,i,newappparam[ind])
        m=specparam(m,"theme","true","md")
        m = specparam(m, "theme", "false", "ios")
        m = specparam(m, "openIn", "true", "popover")
        m = specparam(m, "openIn", "false", "auto")
        m = specparam(m, "pushStateAnimate", "true", "false")
        m = specparam(m, "pushStateAnimate", "false", "true")

        h=re.sub(appname+"\s*=\s*new\s*Framework7+\(*\{(.*?)*<",m[1:]+closestr,h,flags=re.DOTALL)
        h=jsfilter(h)
    #------------------------------------------------JSMethod(APP)----------------------------------------------------#
    varname=[]
    varval=[]
    newval=[]
    oldmethod=[]
    newmethod=[]
    varname=getvar(h,"(.*)=\s*"+appname+".*\(")
    varval=getvar(h,".*=\s*"+appname+"(.*)\(")
    j = -1
    for i in varval:
        j = j + 1
        if i.count("(") > 1:
            ind = i.find("(")
            i = i[:ind]
        varval[j] = appname + i + "("




#    varval=valfilter(getvar(h,".*=\s*"+appname+"(.*)\("))
    ind=-1
    for i in varname:
        ind=ind+1
        i=i.replace("var","").strip()
        varname[ind]=i
    for i in varval:
        newval.append(i)
    ind=0
    for i in oldjsmethod:
        if jsmethodpar[ind]=="app":
            oldmethod.append(appname+i)
        ind=ind+1
    ind=0
    for i in newjsmethod:
        if jsmethodpar[ind]=="app":
            newmethod.append(appname+i)
        ind=ind+1
    ind=-1
    for i in varval:
        ind=ind+1
        if i in oldmethod:
            j=oldmethod.index(i)
            newval[ind]=newmethod[j]
    h=methodfilter(h)

    #-----------------------------------------------------JSMethod(DOM7)--------------------------------------------------#
    pattern=r".*?\s*=\s*Dom7"
    m=re.search(pattern,h)
    if m:
        m=m.group()
        m=re.sub("=\s*Dom7","",m)
        dom7name=m.replace("var ","").strip()
    ind=-1
    oldnoparent=[]
    newnoparent=[]
    for i in jsmethodpar:
        ind=ind+1
        if i=="DOM7":
            oldnoparent.append(dom7name+oldjsmethod[ind])
            newnoparent.append(appname+newjsmethod[ind])
    ind=-1
    for i in oldnoparent:
        ind=ind+1
        h=h.replace(oldnoparent[ind],newnoparent[ind])
    #-----------------------------------------------------JSGetParentName-------------------------------------------------#
    varparname=[]
    varparval=[]
    ind=-1
    for i in jsmethodcur:
        ind=ind+1
        if i!="-":
            n=newjsmethod[ind].replace("(","\(")
            pattern="(.*)=\s*"+appname+n
            m1=re.findall(pattern, h)
            if m1:
                for j in m1:
                    varparname.append(j.replace("var","").strip())
                    varparval.append(i)
    #------------------------------------------------JSMethod(Components)-------------------------------------------------#
    ind=-1
    for i in jsmethodcur:
        ind=ind+1
        if i=="-":
            if oldjsmethod[ind]!=".closeModal(":
                if jsmethodpar[ind]=="app":
                    par=appname
                    h = h.replace(par+oldjsmethod[ind], par+newjsmethod[ind])
                else:
                    for j in varparval:
                        if j==jsmethodpar[ind]:
                            par=jsmethodpar[ind]
                            h = h.replace(par+oldjsmethod[ind], par+newjsmethod[ind])
        else:
            if oldjsmethod[ind]!=".closeModal(":
                if jsmethodpar[ind]=="app":
                    par=appname
                    h = h.replace(par+oldjsmethod[ind], par+newjsmethod[ind])
                else:
                    for j in varparval:
                        if j==jsmethodpar[ind]:
                            par=jsmethodpar[ind]
                            h = h.replace(par+oldjsmethod[ind], par+newjsmethod[ind])
    pattern=r"closeModal\((.*)\)"
    m=re.findall(pattern,h)
    modalval=[]
    modaltype=[]
    modals="popup popover actions loginScreen picker".split(" ")
    if m:
        for i in m:
            if i.find(",")>-1:
                ind=i.index(",")
                i=i[:ind-1]
            modalval.append(i)
    for i in modalval:
        for j in modals:
            if h.find(appname+"."+j+".create("+i)>-1:
                h=re.sub(r"closeModal\(\s*"+i,j+".close("+i,h)
    for i in modalval:
        if i.find("popup")>-1:
            modaltype.append("popup")
        elif i.find("popover")>-1:
            modaltype.append("popover")
        elif i.find("picker")>-1:
            modaltype.append("picker")
        else:
            modaltype.append("loginScreen")
    ind=0
    for i in modalval:
        h=re.sub(r"closeModal\(\s*"+i,modaltype[ind]+".close("+i,h)
        ind=ind+1
    #--------------------------------------------------JSParam------------------------------------------------------------#
    parampar=[]
    paramparlist=[]
    oldparamlist=[]
    newparamlist=[]
    for i in varparname:
        for js in jsparampar:
            pattern=i+"\s*=\s.*"+js+".*\(\s*\{"
            m=re.findall(pattern,h,re.DOTALL)
            if m:
                for j in m:
                    j=funccloser(j)
                    j=j[1:]
                    if j.find("{")>-1 and j.find("}")>-1:
                        if not js in oldparamlist:
                            oldparamlist.append(j)
                            paramparlist.append(js)
    for i in oldparamlist:
        newparamlist.append(i)
    k=0
    for i in newparamlist:
        for j in oldjsparam:
            ind=oldjsparam.index(j)
            jsparam=jsparampar[ind]
            if (i.find(j+":")>-1) and (jsparam==paramparlist[k]):
                i=i.replace(j+":",newjsparam[ind]+":")
            i = specparam(i, "openIn", "true", "popover")
            i = specparam(i, "openIn", "false", "auto")
            i = specparam(i, "pushStateAnimate", "true", "false")
            i = specparam(i, "pushStateAnimate", "false", "true")
            i = specparam(i, "lazyLoading","true","{ enabled:true }")
            i= paramchange(i, "lazyLoading","lazy")
            i = paramwrap(i,"lazy", "swiper")
            i = paramchange(i, "container", "containerEl")


            newparamlist[k]=i
        k=k+1
    ind = 0
    for i in oldparamlist:
        if h.find(i) > -1:
            h = h.replace(i, newparamlist[ind])
        ind = ind + 1
    h=onfunc(h,paramparlist)

    for event in oldjsevent:
        if h.find(event)>-1:
            newevent=newjsevent[oldjsevent.index(event)]
            h=h.replace(event,newevent)
    pattern=".on\s*\(\s*'refresh'"
    h=re.sub(pattern,".on('ptr:refresh'",h)
    v1page=['.onPageBeforeInit(','.onPageInit(','.onPageReinit(','.onPageBeforeAnimation(',
            '.onPageAfterAnimation(','.onPageBeforeRemove(','.onPageBack(','.onPageAfterBack(']
    v2page=["$$(document).on('page:mounted'","$$(document).on('page:init',",
            "$$(document).on('page:reinit',","$$(document).on('page:beforein',",
            "$$(document).on('page:afterin',","$$(document).on('page:beforeremove',",
            "$$(document).on('page:beforeout',","$$(document).on('page:afterout',"]

    for i in v1page:
        ind=v1page.index(i)
        i=appname+i
        if h.find(i)>-1:
            pattern=i.replace("(","\(")+"(.*),"
            m=re.findall(pattern,h)
            for j in m:
                k=j.split(" ")
                newj=""
                if len(k) > 1:
                    for s1 in k:
                        s1=s1.replace("\'","")
                        newj=newj+", .page[data-name=\""+s1+"\"]"
                    newj=newj[1:]
                else:
                    newj=".page[data-name="+j+"]"
                newj="\'"+newj.replace("\'","\"")+"\'"
                val=v2page[ind]+" "+newj
                pattern=i+j
                pattern=pattern.replace("(","\(").replace(")","\)")
                h=re.sub(pattern,val,h,re.DOTALL)
    h=jshtml(h)
    #---------------------------------------------------------------------------------------------------------------------#
    h=errorfilter(h)
    h=pickerinit(h)
    h=actioninit(h)
    h=notificationinit(h)
    h=autocompleteinit(h)
    h=virtuallistinit(h)
    h=messageinit(h)
    h=swiperinit(h)
    return h
#h=jstrans("C:\\Users\\Administrator\\Desktop\\f7-final-test\\v1\\js\\kitchen-sink.js")
#file=open("C:\\Users\\Administrator\\Desktop\\f7-final-test\\v2-test\\f7-test\\js\\kitchen-sink.js","r")
#h=file.read()
#file.close()
#print(h)