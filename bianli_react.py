import os, shutil, f7react, time
time_start=time.time()
loadpath="C:\\Users\\Administrator\\Desktop\\f7-final-test\\r\\src"
savepath="C:\\Users\\Administrator\\Desktop\\f7-final-test\\r\\ionic\\src"
for root, dirs, files in os.walk(loadpath):
    p2=root.replace(loadpath,"")
    if not os.path.exists(savepath+p2):
        os.makedirs(savepath+p2)
    for fn in files:
        if fn.find(".jsx")>-1:
            print(fn)
            r1=f7react.f7update(root+"\\"+fn)
            f1=open(savepath+p2+"\\"+fn,'w',encoding='utf-8')
            f1.write(r1)
            f1.close()
        if fn.find('route')>-1:
            r1=open(root+"\\"+fn,'r',encoding='utf-8').read()
            f1=open(savepath+p2+"\\"+fn,'w',encoding='utf-8')
            f1.write(r1)
            f1.close()
        else:
            if not fn.find(".jsx")>-1:
                shutil.copyfile(root+"\\"+fn, savepath+p2+"\\"+fn)
time_end=time.time()
t=time_end-time_start
print("更新时间为",t,"秒")