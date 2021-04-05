#!/usr/bin/python3
from os import system as run
import os
from os.path import isfile

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

print("[INF] You can use the cachier command directly to run cachier. [INF]\n")

run("cachier --help")
