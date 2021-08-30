import requests,bs4,re,pymysql
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

#------------------------------------------------读取页面----------------------------------------------------------#
fname="c:/2.txt"
html_code=open(fname,"r",encoding='utf-8')
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
h1=open(fname,"w",encoding="utf-8")
h1.write(s2)
#print(s2)
h1.close()
soup=bs4.BeautifulSoup(s2,"html.parser")
#-----------------------------------------JS APPNAME--------------------------------------------------------------#
a=str(soup)
pattern=r".*?\s*=\s*new\s*Framework7"
m=re.findall(pattern,a)
m=''.join(m)
m=re.sub("=\s*new\s*Framework7","",m)
appname=m.replace("var ","").strip()
print("Appname is: "+appname)

#-----------------------------------------APP初始化----------------------------------------------------------------#
a=str(soup)
pattern=r"=\s*new\s*Framework7+\(*\{.*"
m=re.search(pattern,a,flags=re.DOTALL).group()
str1=m.split("\n")
m=""
opener=0
close=0
ind=0
for i in str1:
    m=m+"\n"+i
    ind=ind+1
    opener = opener+i.count("{")
    opener = opener-i.count("}")
    close=close+i.count("}")
    if opener==0:
        break
closestr=""
while ind<len(str1):
    closestr=closestr+"\n"+str1[ind]
    ind=ind+1
appparam=m
m=m.replace("  "," ")
m=re.sub(r"//.*","",m)
m=re.sub(r"/\*(.*?)\*/","",m,flags=re.DOTALL)
m=m.replace(": ",":")
attrname=re.findall(r".*:",m)
attrval=re.findall(r":.*?[\n]",m,flags=re.DOTALL)
attrn=[]
attrv=[]
for n in attrname:
    n=n.replace(":","").strip()
    attrn.append(n)
for v in attrval:
    v=v.replace(",","")
    v=v.replace(":","").strip()
    attrv.append(v)
attrcount = len(attrn)
i=0
ind=m.find(attrn[0]+":"+attrv[0])
funclist=[]
while i<attrcount:
   if attrn[i] in oldappparam:
       j = oldappparam.index(attrn[i])
       if appparampar[j]=="-":
            pattern = attrn[i] + ":" + attrv[i]+","
            new = newappparam[j]+":"+attrv[i]
            funclist.append(new+","+"\n")
            m = re.sub(pattern,"", m, flags=re.DOTALL)
            pattern = attrn[i] + ":" + attrv[i]
            m = re.sub(pattern, "", m, flags=re.DOTALL)
   else:
       new = attrn[i] + ":" + attrv[i]
       funclist.append(new + "," + "\n")
       pattern = attrn[i] + ":" + attrv[i] + ","
       m = re.sub(pattern, "", m, flags=re.DOTALL)
       pattern = attrn[i] + ":" + attrv[i]
       m = re.sub(pattern, "", m, flags=re.DOTALL)
   i = i + 1
i=0
while i<attrcount:
    if attrn[i] in oldappparam:
        j = oldappparam.index(attrn[i])
        if appparampar[j]!="-":
           new = appparampar[j]+":{"+"\n"
           for child in attrn:
               for old in oldappparam:
                   if child not in oldappparam:
                        continue
                   o=oldappparam.index(child)
                   n=attrn.index(child)
                   if (o>-1) and (appparampar[o]==appparampar[j]):
                        if (old!=attrn[i]):
                            new = new + newappparam[o]+":"+attrv[n]+","+"\n"
                            pattern = attrn[n] + ":" + attrv[n]
                            m = re.sub(pattern, "", m, flags=re.DOTALL)
                            pattern = attrn[n] + ":" + attrv[n] + ","
                            m = re.sub(pattern, "", m, flags=re.DOTALL)
                            break
           new=new[:-2]+"\n"+"},"+"\n"
           if new not in funclist:
                funclist.append(new)
           pattern = attrn[i] + ":" + attrv[i]
           m = re.sub(pattern,"", m, flags=re.DOTALL)
           pattern = attrn[i] + ":" + attrv[i]+","
           m = re.sub(pattern, "", m, flags=re.DOTALL)
    i = i+1
leng=len(funclist)
func="".join(funclist)
m = m[:ind]+func+m[ind:]
j=m.split("\n")
i=0
k=[]
while i<len(j):
    if (j[i].strip() != ",") and (j[i].strip() != ""):
        k.append(j[i])
    i=i+1
m="\n".join(k)
m=m[:-5]+m[-4:]
pattern=r"=\s*new\s*Framework7+\(*\{(.*?)*<"
a=re.sub(pattern,m+closestr,a,flags=re.DOTALL)
soup=a
print("初始化完成")

#--------------------------------------------JSMethod--------------------------------------------------------------#
a=str(soup)
methodlist=[]
methodname=[]
methodpar=[]
methodval=[]
for method in oldjsmethod:
    j=oldjsmethod.index(method)
    if method in a:
        if jsmethodpar[j]=="app":
            pattern=r".*=*\s+"+appname+method
            pattern=pattern.replace("(","\(")
            if not re.match(pattern,a,re.DOTALL):
                continue
            m=re.search(pattern,a).group()
            methodlist.append(m)
            name=m.replace("var ","")
            name=name.replace(appname+method,"")
            name=name.replace("=","")
            name=name.replace(" ","")
            replacestr = "var " + name + " = "
            methodname.append(name)
            methodval.append(appname+newjsmethod[j])
            par=re.search(r"\..*\.",newjsmethod[j]).group()
            par=par.replace(".","")
            methodpar.append(par)
            chkstr = replacestr.replace("var","")
            chkstr = chkstr.replace("=","")
            if chkstr.strip()=="":
                replacestr=""
            replacestr = replacestr+appname+newjsmethod[j]
            a = re.sub(pattern,replacestr,a)
        elif jsmethodpar[j]=="-":
            a = re.sub(oldjsmethod[j],newjsmethod[j],a,re.DOTALL)
for method in oldjsmethod:
    j=oldjsmethod.index(method)
    if a.find(method)>-1:
        if jsmethodpar[j]!="app" and jsmethodpar[j]!="":
            for list1 in methodlist:
               if list1.find(method):
                   ind=methodlist.index(list1)
                   break
            par = methodname[ind]
            pattern = par+method
            pattern = pattern.replace("(","\(")
            pattern = pattern.replace(")","\)")
            a = re.sub(pattern, par + newjsmethod[j], a)
    """
    i=0
    while i<len(methodlist):
        print(methodlist[i])
        print(methodname[i])
        print(methodpar[i])
        i=i+1
    """
soup=a
print("Method完成")
#--------------------------------------------JSPARAM---------------------------------------------------------------#
a=str(soup)
m=""
for method in methodval:
   ind=methodval.index(method)
   pattern=method+"*\s*\{*(.*?)*\}*"
   pattern=pattern.replace("(","\(")
   pattern=pattern.replace(")","\)")
   m=re.search(pattern,a,re.DOTALL)
   if re.match(pattern,a,re.DOTALL):
       pattern = method + "*\s*\{*(.*?)*\}"
       pattern = pattern.replace("(", "\(")
       pattern = pattern.replace(")", "\)")
       m=re.search(pattern,m.group(),flags=re.DOTALL)
       m=m.group()
       k=m
       par=methodpar[ind]
       sql="SELECT * FROM f7jsparam WHERE (version='v2') AND (parent='"+par+"')"
       cur.execute(sql)
       for r in cur:
            if m.find(r[1])>-1:
                 m=m.replace(r[1]+":",r[2]+":")
                 k=k.replace("(","\(")
                 k=k.replace(")","\)")
                 a=re.sub(k,m,a,re.DOTALL)
a=a.replace("  "," ")
a=a.replace(": ",":")
a=a.replace("theme:true","theme:md")
a=a.replace("theme:false","theme:ios")
a=a.replace("openIn:true","openIn:popover")
a=a.replace("openIn:false","openIn:auto")
a=a.replace("pushStateAnimate:true","pushStateAnimate:false")
a=a.replace("pushStateAnimate:false","pushStateAnimate:true")
soup=a
print("Param完成")
#--------------------------------------------JSEVENTS--------------------------------------------------------------#
a=str(soup)
for event in oldjsevent:
    if a.find(event)>-1:
        newevent=newjsevent[oldjsevent.index(event)]
        a=a.replace(event,newevent)
soup=a
print("event完成")
#-------------------------------------------"ON:"EVENT-------------------------------------------------------------#
a=str(soup)
funcbody=[]
methodbody=[]
methodevent=[]
methodoncount=[]
methodnoevent=[]
for i in newjsmethod:
        p=i.replace("(","\(")
        p=p.replace(")","\)")
        f0=re.search(p+".*\}",a,flags=re.DOTALL)
        if f0!=None:
            f0=f0.group()
            str0=f0.split("\n")
            opener=0
            m = ""
            for i in str0:
                if i.strip()=="":
                    str0.remove(i)
            for i in str0:
                m=m+"\n"+i
                opener=opener+i.count("{")
                opener = opener - i.count("}")
                if opener==0:
                    break
            for j in oldonevent:
                if m.find(j)>-1:
                    if j not in methodevent:
                        methodevent.append(j)
            for j in oldonevent:
                if (m.find(j)>-1) and (m not in methodbody):
                    methodbody.append(m)
for i in methodbody:
        oncount = 0
        onevent=[]
        for j in methodevent:
            b=re.search(j+".*\}",i,flags=re.DOTALL)
            if (b!=None):
                b=b.group()
                m=""
                opener=0
                str0=b.split("\n")
                for s in str0:
                    m = m + "\n" + s
                    opener = opener + s.count("{")
                    opener = opener - s.count("}")
                    if open == 0:
                        break
                onevent.append(m)
        oncount=len(onevent)
        methodoncount.append(oncount)
        num=0
        ss=""
        while (num<oncount):
            for j in oldonevent:
                if (onevent[num].find(j)>-1):
                    k=onevent[num]
                    ind=oldonevent.index(j)
                    j=j.replace("(","\(")
                    j=j.replace(")","\)")
                    onevent[num]=re.sub(j,newonevent[ind],onevent[num],re.DOTALL)
                    a=a.replace(k,onevent[num])
            ss=ss+onevent[num]+"\n"
            num=num+1
        num=0
        noevent = ""
        while (num<oncount-1):
            first=onevent[num]
            first=first.replace("(","\(")
            first=first.replace(")","\)")
            next=onevent[num+1]
            next=next.replace("(","\(")
            next=next.replace(")","\)")
            n=re.search(first+".*"+next,a,flags=re.DOTALL)
            if n!=None:
                n=n.group()
                if n.strip()!="":
                    a = a.replace(n, onevent[num] + onevent[num + 1])
                    noevent=noevent+n.replace(onevent[num],"")
                    noevent=noevent.replace(onevent[num+1],"")
            num=num+1
        if len(onevent)>1:
            n=len(onevent)-1
            firstbody=onevent[0]
            lastbody=onevent[n]
            a=a.replace(firstbody,"\non:{"+firstbody)
            a=a.replace(lastbody,lastbody+"\n}")
            if noevent.strip()!="":
                a=a.replace(lastbody+"\n}",lastbody+"\n}"+noevent)
soup=a
print("on Event完成")
#--------------------------------------------JSPAGEDOM-------------------------------------------------------------#
a=str(soup)
v1page=['.onPageBeforeInit(','.onPageInit(','.onPageReinit(','.onPageBeforeAnimation(',
        '.onPageAfterAnimation(','.onPageBeforeRemove(','.onPageBack(','.onPageAfterBack(']
v2page=["$$(document).on('page:mounted',","$$(document).on('page:init',",
        "$$(document).on('page:reinit',","$$(document).on('page:beforein',",
        "$$(document).on('page:afterin',","$$(document).on('page:beforeremove',",
        "$$(document).on('page:beforeout',","$$(document).on('page:afterout',"]
for v in v1page:
        i = v1page.index(v)
        v=appname+v
        a=a.replace(v,v2page[i])
soup=a
print("pagedom完成")
#----------------------------------------------完成----------------------------------------------------------------#
print(soup)
a=str(soup)
cur1.close()
cur.close()
conn.close()
#h1=open(fname,"w",encoding="utf-8")
#h1.write(a)
#h1.close()
print("完成")