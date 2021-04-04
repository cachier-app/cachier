import os.path, os
import sys
import datetime
from rich.console import Console
from rich.syntax import Syntax
from json import dump, load

import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")

DEBUG = False
cachierDir = '{}/.cachier'.format(os.path.expanduser("~"))

def logme(message, type=None):
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


def debuglog(message, logType="INFO"):
    if not DEBUG:
        return 
    logging.debug(f"{message} ({logType.upper()})", extra={"markup": True})


# Working here ~ Mr. RC
def help():
    print("Usage: cachier [options] [command]")
    print("run <command>: Command to run and cache.")
    print("<command>: Show cache of <command>.")
    print("--debug: Enable debug mode.")
    print("--clear-cache: Clear all saved caches.")
    print("Example:")
    print("\tcachier run ls \t#For caching a command.")
    print("\tcachier ls \t#For showing cache of a command.")
    print("\tcachier run ls --debug \t#For caching a command with debug mode enabled.")
    print("\tcachier --clear-cache \t#For clearing all cache.")
    exit()

def clear_cache():
    global cachierDir
    dir = cachierDir+'/default'
    debuglog(f"Getting all the files from {dir}")
    for file in os.scandir(dir):
        debuglog("Removing file {file.path}", "debug")
        os.remove(file.path)
        debuglog("Removed file {file.path}")
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
    debuglog(f"Successfully dumped json into {file}.")
    file.close()

def get_json_data(command):
    json_files = []
    data_dict = {}
    for i in os.listdir(f"{groupDir}"):
        if i.endswith(".json") and i.startswith(command):
            json_files.append(f"{groupDir}/{i}")
    
    for file in json_files:
        with open(file) as file:
            data = load(file)
            data_dict[data["filename"]] = data_dict["".join(data["args"])]
    
    return data_dict


debuglog("Checking the length of arguments")
if len(sys.argv)<2:
    debuglog("Length of arguments are less than 2.")
    debuglog("Calling help function")
    help()

for i in sys.argv:
    if "--debug" in i:
        DEBUG = True
    elif i=='--clear-cache':
        debuglog("Cache clearing requested.")
        debuglog("Calling clear_cache function.", "debug")
        clear_cache()
    if "-h" in i:
        help()

# making sure the .cachier directory is present
debuglog(f"Checking if {cachierDir} exits...")
if not os.path.exists(cachierDir):
    debuglog(f"Checking if {cachierDir} exits...")
    logme('"{}" is not present, creating it now'.format(cachierDir), 'warning')
    os.makedirs(cachierDir)

group = 'default'
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
    get_json_data(commandName)
    debuglog(f"[green]Saved the output of the command to {groupDir}/{outputFile}.txt", "debug")
else:
    command = sys.argv[1]
    debuglog(f"[yellow]sys.argv[1] = {command}", 'debug')
    outputsinDir = [f for f in os.listdir(groupDir) if os.path.isfile(os.path.join(groupDir, f)) and f.startswith(command) and f.endswith('.txt')]
    outputsLen = len(outputsinDir)
    if outputsLen == 0:
        debuglog(f"[red]{command} was never cached but requested!", 'error')
        logme("This command was never cached", 'error')
        debuglog(f"[red]Exiting.", 'error')
        exit()
    elif outputsLen == 1:
        debuglog(f"[green]Cache found for command {command}.")
        with open(os.path.join(groupDir, outputsinDir[0])) as f:
            debuglog(f"[yellow]Reading cache for command {command}", "debug")
            contents = f.read()
            debuglog(f"Setting up syntax highlighting for rich.syntax.Syntax function...")
            syntax = Syntax(contents, "python", theme="monokai", line_numbers=True)
            console = Console()
            debuglog(f"[yellow]Printing the code...")
            console.print(syntax)
            debuglog(f"Done without errors.")
    else:
        debuglog(f"[red]Multiple caches found!", 'warning')
        logme("Multiple caches found! Please choose one:", 'warning')
        for f in outputsinDir:
            print(str(outputsinDir.index(f)) + " = " + f)
        opt = input(f"Choose: (0 to {len(outputsinDir) - 1}): ")
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
             debuglog(f"Setting up syntax highlighting for rich.syntax.Syntax function...")
             syntax = Syntax(contents, "bash", theme="monokai", line_numbers=True)
             console = Console()
             debuglog(f"[yellow]Printing the code...")
             console.print(syntax)
             debuglog(f"Done without errors.")
        except IndexError:
            debuglog("[red]Index error!", "error")
            debuglog("[red]User gave a number that was not in the list!", "error")
            logme("Invalid choice", 'error')
