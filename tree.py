class node:

    def __init__(self, data):
        self._data = data
        self._children = []

    def getdata(self):
        return self._data

    def getchildren(self):
        return self._children

    def add(self, node):
        self._children.append(node)

    def go(self, data):
        for child in self._children:
            if child.getdata() == data:
                return child
        return None
    def parent(self):
        return self._parent


class tree:

    def __init__(self):
        self._head = node('header')

    def linktohead(self, node):
        self._head.add(node)

    def insert(self, path, data):
        cur = self._head
        for step in path:
            if cur.go(step) == None:
                return False
            else:
                cur = cur.go(step)
        cur.add(node(data))
        return True

    def search(self, path):
        cur = self._head
        for step in path:
            if cur.go(step) == None:
                return None
            else:
                cur = cur.go(step)
        return cur


'''
define node
'''
a = node('Action')
b = node("$$('.ac-1').on('click', function ()")
b1 = node("var buttons = [")
c = node("$$('.ac-2').on('click', function ()")
c1 = node("var buttons = [")
d = node("$$('.ac-3').on('click', function ()")
d1 = node("var buttons1 = [")
d2 = node("var buttons2 = [")
e = node("$$('.ac-4').on('click', function ()")
e1 = node("var buttons1 = [")
e2 = node("var buttons2 = [")
e3 = node("var buttons3 = [")
f = node("$$('.ac-5').on('click', function ()")
f1 = node("var buttons = [")
g = node("text: 'Button1', bold: true")
h = node("text: 'Button2'")
i = node("text: 'Cancel', color: 'red'")
j = node("text: 'Do something', label: true")
k = node("text: 'Button1', bold: true")
l = node("text: 'Button2'")
m = node("text: 'Cancel', color: 'red'")
n = node("text: 'Do something', label: true")
o = node("text: 'Button1', bold: true")
p = node("text: 'Button2'")
q = node("text: 'Cancel', color: 'red'")
r = node("text: 'Share', label: true")
s = node("text: 'Mail'")
t = node("text: 'Messages'")
u = node("text: 'Social share', label: true")
v = node("text: 'Facebook'")
w = node("text: 'Twitter'")
x = node("text: 'Cancel',color: 'red'")
y = node("text: 'Button1',")
z = node("text: 'Button2',")
a1 = node("text: 'Cancel', color: 'red',")
a2 = node(" myApp.alert('Button1 clicked');")
a3 = node(" myApp.alert('Button2 clicked');")
a4 = node(" myApp.alert('Button3 clicked');")


'''
adding node to build true
'''
a.add(b)
a.add(c)
a.add(d)
a.add(e)
a.add(f)
b.add(b1)
b1.add(g)
b1.add(h)
b1.add(i)
c.add(c1)
c1.add(j)
c1.add(k)
c1.add(l)
c1.add(m)

d.add(d1)
d.add(d2)
e.add(e1)
e.add(e2)
e.add(e3)
f.add(f1)
f1.add(y)
f1.add(z)
f1.add(a1)

d1.add(n)
d1.add(o)
d1.add(p)
d2.add(q)
e1.add(r)
e1.add(s)
e1.add(t)
e2.add(u)
e2.add(v)
e2.add(w)
e3.add(x)
y.add(a2)
z.add(a3)
a1.add(a4)


tree = tree()
tree.linktohead(a)

"""
 testcase
print('Node', tree.search("ABE").getdata())
print('Node', tree.search("ABC").getdata())
print('Node', tree.search("AHM").getdata())
tree.insert("ABCD", 1)
for i in a.getchildren():
    print( a.getdata(), ' { ', i.getdata(),"}")
"""
path="C:/Users/Administrator/Desktop/test.txt"
code_file = open(path, "r", encoding='utf-8')
code = code_file.read()
code_file.close()
s1=code.split("\n")
n1=node("")
n2=[]
tree.linktohead(n1)




for s in s1:
    if (s.find('{')<0) and (s.find('}')<0):
        n2.append(s)
    else:
        if s.find('{')>-1:
            n2.append(s)
        if s.find("}")>-1:
            n1.add(node("\n".join(n2)))
            n2=[]

for i in n1.getchildren():
    if i.getdata().strip()!="":
        print( i.getdata(),"--------", i.parent())
        print("==========================")