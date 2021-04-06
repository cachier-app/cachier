#!/usr/bin/python3

import os.path, os
import sys
import datetime
from rich.console import Console
from rich.syntax import Syntax
from json import dump, load
import logging
from rich.logging import RichHandler
from requests import get

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")
version = 1.0

class Logger:
    def __init__(self, debugEnabled=False):
        self.debug = debugEnabled

    def logme(self, message, type=None):
        if type=='info':
            logging.info(message, extra={"markup": True})
        elif type=='debug':
            logging.debug(message, extra={"markup": True})
        elif type=='warning':
            logging.warning(message, extra={"markup": True})
        elif type=='error':
            logging.error(message, extra={"markup": True})
        else:
            logging.info(message, extra={"markup": True})


    def debuglog(self, message, logType="INFO"):
        if not self.debug:
            return
        logging.debug(f"{message} ({logType.upper()})", extra={"markup": True})

DEBUG = False
HIGHLIGHTING = True
group = 'default'
cachierDir = '{}/.cachier'.format(os.path.expanduser("~"))
available_args = ["--debug", "--clear-cache", "--no-highlight", "-g", "run", "--update"]

logger = Logger(DEBUG)
logme = logger.logme
debuglog = logger.debuglog

def help():
    print("Usage: cachier [options] [command]")
    print("run <command>: Command to run and cache.")
    print("<command>: Show cache of <command>.")
    print("--debug: Enable debug mode.")
    print("--clear-cache: Clear all saved caches.")
    print("--no-highlight: Turn of syntax highlighting while printing cached data.")
    print("--update: Update the tool.")
    print("Example:")
    print("\tcachier run ls \t#For caching a command.")
    print("\tcachier ls \t#For showing cache of a command.")
    print("\tcachier run ls --debug \t#For caching a command with debug mode enabled.")
    print("\tcachier --clear-cache \t#For clearing all cache.")
    print("\tcachier ls --no-highlight \t#For showing cache of a command.")
    print("\tcachier --update")
    exit()
    
def update():
    current_ver = get("https://raw.githubusercontent.com/cachier-app/cachier/main/.version").text
    try:
        if float(current_ver)!=version:
            print("[INF] An update is available. [INF]")
            os.system(f"cd {open(cachierDir+'/install_dir').read()}; git pull; ./setup.py")
            os.system("clear")
            print("[INF] The tool has been updated. Now you can rerun the tool to get started. [INF]")
            exit()
        elif float(current_ver)==version:
            print("[INF] The tool is already up-to-date. [INF]")
            exit(0)
    except FileNotFoundError:
        print("[ERR] Looks like you've not installed the tool with setup.py [ERR]")
        print("[INF] To update the tool, you should run the setup.py again from the directory where you cloned cachier. [INF]")
        exit(0)

def clear_cache():
    global cachierDir
    dir = cachierDir+'/default'
    debuglog(f"Getting all the files from {dir}")
    for file in os.scandir(dir):
        debuglog(f"Removing file {file.path}", "debug")
        os.remove(file.path)
        debuglog(f"Removed file {file.path}")
    logme("Cache for all commands was cleared successfully.")
    debuglog("Cache cleared succesfully.")
    exit(0)

def create_json(command, filename, args=None):
    json_struct = {
        "command": "",
        "args": "",
        "filename": ""
    }
    json_struct["command"]=command
    json_struct["args"]=args
    json_struct["filename"] = filename
    debuglog(f"Work done successfully. Returning...", 'debug')
    return json_struct

def writejson(json: dict):
    debuglog(f"Opening file: {json['filename']} in write mode.", 'debug')
    file = open(json["filename"], "w")
    dump(json, file)
    debuglog(f"Successfully dumped json into {json['filename']}.")
    file.close()

def get_json_data(command):
    json_files = []
    data_dict = {}
    debuglog(f"Getting all files from {groupDir}")
    for i in os.listdir(f"{groupDir}"):
        debuglog(f"Getting only json files for the {command} command")
        if i.endswith(".json") and i.startswith(command):
            debuglog(f"json i = {i}")
            json_files.append(f"{groupDir}/{i}")

    for file in json_files:
        with open(file) as file:
            data = load(file)
            fname = " ".join(data["args"])
            data_dict[data["filename"]] = fname

    return data_dict

def highlight_code(contents):
    if not HIGHLIGHTING:
        print(contents)
        return
    debuglog(f"Setting up syntax highlighting for rich.syntax.Syntax function...")
    syntax = Syntax(contents, "bash", theme="monokai", line_numbers=True)
    console = Console()
    debuglog(f"[yellow]Printing the code...")
    console.print(syntax)
    debuglog(f"Done without errors.")

# this will never run
#debuglog("Checking the length of arguments")
if len(sys.argv)<2:
    debuglog("Length of arguments are less than 2.")
    debuglog("Calling help function")
    help()

if len(sys.argv)==1 and sys.argv[1]=="run":
    debuglog("User doesn't supplied argument with run command.")
    print("[ERR] run command is missing an argument. [ERR]")
    help()

for i in sys.argv:
    if i.startswith("-") and i not in available_args:
        help()
    if i=="--update":
        update()
    if "--debug" in i:
        logger.debug = True
    if i=='--clear-cache':
        debuglog("Cache clearing requested.")
        debuglog("Calling clear_cache function.", "debug")
        clear_cache()
    if i=="--no-highlight":
        HIGHLIGHTING=False
    if i=="-g":
        n = sys.argv.index("-g")
        group = "".join(sys.argv[n+1:n+2:])
    if i=="-h" and sys.argv[sys.argv.index(i)-1]!="run":
        help()
    if i=="--help" and sys.argv[sys.argv.index(i)-1]!="run":
        help()

groupDir = '{}/{}'.format(cachierDir, group)
# making sure the group directory exists in cachierDir
debuglog(f"Checking if {groupDir} exits...")
if not os.path.exists(groupDir):
    logme('"{}" is not present, creating it now'.format(groupDir), 'warning')
    os.makedirs(groupDir)

debuglog(f"Checking arguments...")
if sys.argv[1] == 'run':
    debuglog(f"[yellow]sys.argv[1] = run", "debug")
    # run command in sys.argv[2]
    command = sys.argv[2]
    commandName = command.split(" ")[0]
    args = command.split( )[1::]
    current_time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    debuglog(f"[green]Current time: {current_time}", 'info')
    outputFile = commandName + "_" + current_time
    debuglog(f"[green]Running command: {command}", 'debug')
    os.system(f"{command} | tee \"{groupDir}/{outputFile}.txt\"")
    debuglog(f"[green]Calling create_json function...", 'debug')
    infojson = create_json(commandName, f"{groupDir}/{outputFile}.json", args=args)
    debuglog("Calling writejson function...")
    writejson(infojson)
    debuglog(f"[green]Saved the output of the command to {groupDir}/{outputFile}.txt", "debug")
else:
    command = sys.argv[1]
    debuglog(f"[yellow]sys.argv[1] = {command}", 'debug')
    outputsinDir = [f for f in os.listdir(groupDir) if os.path.isfile(os.path.join(groupDir, f)) and f.startswith(command) and f.endswith('.txt')]
    outputsLen = len(outputsinDir)
    if outputsLen == 0 and command not in available_args:
        debuglog(f"[red]{command} was never cached but requested!", 'error')
        logme("This command was never cached", 'error')
        debuglog(f"[red]Exiting.", 'error')
        exit()
    elif outputsLen == 1 and command not in available_args:
        debuglog(f"[green]Cache found for command {command}.")
        with open(os.path.join(groupDir, outputsinDir[0])) as f:
            debuglog(f"[yellow]Reading cache for command {command}", "debug")
            contents = f.read()
            highlight_code(contents)
    elif outputsLen<=2 and command not in available_args:
        debuglog(f"[red]Multiple caches found!", 'warning')
        logme("Multiple caches found! Please choose one:", 'warning')
        debuglog("Requesting json data for the command...")
        data = get_json_data(command)
        debuglog("Getting all the keys from json data")
        data_keys = list(data.keys())
        n = 0
        new_dict = dict()
        for key in data_keys:
            new_dict[data_keys[n].replace("json", "txt")] = data[data_keys[n]]
            n+=1
        
        for f in outputsinDir:
            cArguments = new_dict[f'{groupDir}/{f}']
            cArgumentsString = ""
            if cArguments.strip():
                cArgumentsString = f" ({new_dict[f'{groupDir}/{f}']})"

            print(str(outputsinDir.index(f)) + " = " + f + cArgumentsString)
        try:
            opt = input(f"Choose: (0 to {len(outputsinDir) - 1}): ")
        except KeyboardInterrupt:
            print("")
            logme("[red]Keyboard interrupt detected.", "warning")
            logme("Exiting...", "info")
            exit(0)
        try:
            opt = int(opt)
        except ValueError:
            debuglog("[red]Non integer input from user!", "error")
            logme("Invalid input!", 'error')
            exit()
        print("")
        try:
            with open(os.path.join(groupDir, outputsinDir[opt])) as f:
             contents = f.read()
             highlight_code(contents)             
        except IndexError:
            debuglog("[red]Index error!", "error")
            debuglog("[red]User gave a number that was not in the list!", "error")
            logme("Invalid choice", 'error')

