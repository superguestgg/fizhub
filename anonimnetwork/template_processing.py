import os# , re
walk_templates_before = os.walk("templatesBeforeProcessing")

root_after = "templates/anonimnetwork"
#pattern = "[+]{3}(P?<word>\w+)[-]{3}"
#print(re.search(pattern, line))


def read_templates_for_proc(path):
    templates_for_proc = dict()
    walk_templates_for = os.walk(path)
    for root, dirs, files in walk_templates_for:
        print(root, dirs, files)
        for file_name in files:
            if "." in file_name:
                if file_name.split(".")[-1] == "html":
                    templates_for_proc[file_name.split(".")[0]]\
                        = open(root + "/" + file_name, "r", encoding="utf8").readlines()
    return templates_for_proc


templates_for = read_templates_for_proc("templatesForProcessing")


for root, dirs, files in walk_templates_before:
    print(root, dirs, files)
    for file_name in files:
        if "." in file_name:
            if file_name.split(".")[-1] == "html":
                with open(root+"/" + file_name, "r", encoding="utf8") as file_before,\
                     open(root_after+"/" + file_name, "w", encoding="utf8") as file_after:
                    for line in file_before:
                        if "+++" in line:
                            template_for_name = line.split("+++")[1].split("---")[0]
                            file_after.write(line.split("+++")[0]
                                 + "\n".join(templates_for[template_for_name])
                                 + line.split("---")[1])
                        else:
                            file_after.write(line)