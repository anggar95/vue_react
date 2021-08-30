import os,re,collections,tkinter.messagebox

def generateroute(p):
    pathlist = []
    urllist = []
    namelist = []
    route = "var routes = [\n"
    for root, dirs, files in os.walk(p):
        for fn in files:
            if os.path.splitext(fn)[-1] == ".html":
                root = root.replace("\\", "/")
                p1 = root[len(p):]
                route = route + "{" + "\n"
                path = "path: '/" + os.path.splitext(fn)[0] + "/',"
                pathlist.append(os.path.splitext(fn)[0])
                route = route + path + "\n"
                f = open(root + "/" + fn, "r", encoding="utf-8")
                line = f.read()
                f.close()
                line = line.replace("'", "\"")
                line = line.replace("data-page", "data-name")
                a = re.findall(r"data-name=\"([^\s\'\"\<\>]*?)\"", line, flags=re.DOTALL)
                if a:
                    if len(a) < 2:
                        dataname = a[0]
                        if dataname.strip() != "":
                            route = route + "name: '" + dataname + "',\n"
                            namelist.append(dataname)
                    else:
                        m = re.search(r"view-main.*>", line, flags=re.DOTALL)
                        if m:
                            m = m.group()
                            dataname = re.search(r"data-name=\"([^\s\'\"\<\>]*?)\"", m, flags=re.DOTALL)
                            if dataname:
                                dataname = dataname.group()
                                if dataname.strip() != "":
                                    dataname = dataname.replace("\"", "")
                                    dataname = dataname.replace("data-name=", "")
                                    route = route + "name: '" + dataname + "',\n"
                                    namelist.append(dataname)
                else:
                    namelist.append(" ")
                if p1.strip() != "":
                    url = "." + p1 + "/" + fn
                    urllist.append(url)
                    url = "url: '" + url + "',"
                else:
                    url = "./" + fn
                    urllist.append(url)
                    url = "url: '" + url + "',"
                route = route + url
                route = route + "\n" + "},\n"
    route = route + "];"
    """
    dups = collections.defaultdict(list)
    for i, e in enumerate(pathlist):
        dups[e].append(i)
    for k, v in sorted(dups.items()):
        if len(v) >= 2:
            tkinter.messagebox.showwarning("path值重复", '警告，有重复的path值')
            for i in v:
                duplval = "path: '" + pathlist[i] + "'\nname: '"
                duplval = duplval + namelist[i] + "'\nurl: '"
                duplval = duplval + urllist[i] + "'"
                tkinter.messagebox.showwarning("path值重复", duplval)
    """
    return route


#p="C:\\Users\\Administrator\\Desktop\\f7-final-test\\v2-test\\f7-test"
