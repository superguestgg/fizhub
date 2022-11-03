file=open("models.py", "r")

symbols = "QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuiopasdfghjklzxcv_-)(().=bnm,./;'[]{}:<>?йфячыцувсмакепитрнгоьблшщдю.жзхъэ1234567890"+'"'
now=""
classes_names = []
classes = []
c=0
attributes=[]
classname=""
for line in file:

    if line.count("import")>0:
        c+=1
        continue
    t=0
    for symbol in line:
        if symbol in symbols:
            t=1
            break
    if t==0:
        c+=1
        continue
    if now=="" or now=="def":
        if line[0:3]=="def":
            print("def")
            now="def"
        elif line[0:5]=="class":
            print("class")
            now="class"
            attributes=[]
            classname = line.replace("(", " ").split()[1]
        continue
    elif now=="class":
        if line[0:5] == "class":
            classes.append(attributes)
            classes_names.append(classname)
            #----------
            now = "class"
            classname = line.replace("(", " ").split()[1]
            attributes = []
            continue
        if line[0:3] == "def":
            now = "classdef"
        else:
            line2=""
            for symbol in line:
                if symbol in symbols:
                    line2 += symbol
            #line2=line2.split("=")
            if line2.count("=")>0:
                line2 = [line2[0:line2.index("=")], line2[line2.index("=")+1:]]

            #if len(line2)>2:
            #    line2=[line2[0], "=".join(line2[1:-1])]
            attributes.append(line2)

classes.append(attributes)
classes_names.append(classname)
print(c)
print(classes)
for i in range (len(classes_names)):
    classes_names[i]=classes_names[i].replace("models.Model):","")
print(classes_names)
print(len(classes_names), len(classes))
