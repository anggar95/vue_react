file_path="C:\\Users\\Administrator\\Desktop\\f7-final-test\\vue\\f7-test\\js\\route.js"
file_inp=open(file_path,"r",encoding="utf-8")
coreroute=file_inp.read().replace("[","[\n")
file_inp.close()
router=coreroute.replace("var ","").replace("=","").replace("[","").replace("]","").replace(";","")
strlist=router.split("\n")
strlist[0]=""
pathlist=[]
namelist=[]
urllist=[]
strlist = filter(None, strlist)
for i in strlist:
    if i.find("path:")>-1:
        pathlist.append(i.replace("path:","").replace(",","").strip())
    if i.find("name:")>-1:
        namelist.append(i.replace("name:","").replace(",","").replace("-","").strip())
    if i.find("url:")>-1:
        urllist.append(i.replace("url:","").replace(",","").replace("./","").replace(".html",".vue").strip())
router=("\n").join(strlist)
vueroute=""
ind=0
for i in namelist:
    j=urllist[ind]
    vueroute=vueroute+"import "+i.replace("'","").replace("\"","")+" from "+"'./pages/"+j.replace("'","").replace("\"","").strip()+"';\n"
    ind=ind+1
ind=0
vueroute=vueroute+"\n"+"export default ["+"\n"
for i in pathlist:
    j=namelist[ind]
    vueroute=vueroute+"\n{\n"
    vueroute=vueroute+"path: "+i+",\n"
    vueroute=vueroute+"component: "+j+",\n"
    vueroute=vueroute+"},"
    ind=ind+1
vueroute=vueroute+"\n"+"];"

print(vueroute)