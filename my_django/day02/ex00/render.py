#!/usr/bin/python3

import os
import sys
import re
import settings

def main():
    if (len(sys.argv) != 2):
        print("Error: wrong amount of arguments")
        return
    path = sys.argv[1]
    regex = re.compile(".*\.template")
    if not regex.match(path):
        return print("Error: wrong extension")
    if not os.path.isfile(path):
        return print("Error: file does not exist : {}".format(path))
    file = open(path, "r")
    template = "".join(file.readlines())
    file.close()
    result = template.format(
        name=settings.name, surname=settings.surname, title=settings.title,
        age=settings.age, profession=settings.profession)
    regex = re.compile("(\.template)")
    path_new = "".join([path[0:regex.search(path).start()], ".html"])
    file = open(path_new, "w")
    file.write(result)
    file.close()

if __name__ == '__main__':
    main()
