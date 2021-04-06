#!/usr/bin/python3
from os import system as run
import os
from os.path import isfile

cachierDir = '{}/.cachier'.format(os.path.expanduser("~"))
version = 1.0

# making sure the .cachier directory is present
if not os.path.exists(cachierDir):
    os.makedirs(cachierDir)

print("[INF] Installing requirements [INF]")

if isfile("/usr/bin/pip3"):
    run("pip3 install -r requirements.txt")
else:
    run("pip3 install -r requirements.txt")

print("[INF] Copying file to /usr/bin/cachier [INF]")

if os.name=="posix":
    run("cp main.py /usr/bin/cachier")
else:
    print("[ERR] Not able to move the file to /usr/bin because you're not on a linux machine. [ERR]")
    print("[WRN] Exitting... [WRN]")
    exit()

# writing current directory into a file so that we can cd to the directory when updating the tool
installfile = open(f"{cachierDir}/install_dir", "w")
installfile.write(os.getcwd())
installfile.close()

print("[INF] You can use the cachier command directly to run cachier. [INF]\n")

run("cachier --help")
