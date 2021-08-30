import json
path="C:/Users/Administrator/Desktop/test.txt"
code_file = open(path, "r", encoding='utf-8')
code = code_file.read()
code_file.close()


myApp.alert('Here goes alert text', 'Custom Title!', function () {
        myApp.alert('Button clicked!')