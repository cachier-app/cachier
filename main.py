from logging import debug, warn
import os.path, os
import sys
import datetime
from rich.console import Console
from rich.syntax import Syntax

DEBUG = False
cachierDir = '{}/.cachier'.format(os.path.expanduser("~"))

def logme(message, type=None):
    if not DEBUG:
        return 
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

# Working here ~ Mr. RC
def clear_cache():
    global cachierDir
    dir = cachierDir+'/default'
    logme(f"Getting all the files from {dir}")
    for file in os.scandir(dir):
        logme("Removing file {file.path}", "debug")
        os.remove(file.path)
        logme("Removed file {file.path}")
    print("[INF] Cache for all commands was cleared successfully. [INF]")
    logme("Cache cleared succesfully.")
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
    return json_struct

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

logme("Checking the length of arguments")
if len(sys.argv)<2:
    logme("Calling help function")
    help()

for i in sys.argv:
    if "--debug" in i:
        DEBUG = True
        import logging
        from rich.logging import RichHandler

        FORMAT = "%(message)s"
        logging.basicConfig(
            level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
        )
        log = logging.getLogger("rich")
    elif i=='--clear-cache':
        logme("Cache clearing requested.")
        logme("Calling clear_cache function.", "debug")
        clear_cache()
    if "-h" in i:
        help()

# making sure the .cachier directory is present
logme(f"Checking if {cachierDir} exits...")
if not os.path.exists(cachierDir):
    
    logme(f"Checking if {cachierDir} exits...")
    print('WARN: "{}" is not present, creating it now'.format(cachierDir))
    os.makedirs(cachierDir)

group = 'default'
groupDir = '{}/{}'.format(cachierDir, group)
# making sure the group directory exists in cachierDir
logme(f"Checking if {groupDir} exits...")
if not os.path.exists(groupDir):
    print('WARN: "{}" is not present, creating it now'.format(groupDir))
    os.makedirs(groupDir)

logme(f"Checking arguments...")
if sys.argv[1] == 'run':
    logme(f"[yellow]sys.argv[1] = run", "debug")
    # run command in sys.argv[2]
    command = sys.argv[2]
    commandName = command.split(" ")[0]
    args = command.split( )[1::]
    current_time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    outputFile = commandName + "_" + current_time
    logme(f"[green]Running command: {command}", 'debug')
    os.system(f"{command} | tee \"{groupDir}/{outputFile}.txt\"")
    print(create_json(commandName, f"{cachierDir}/{outputFile}.json", args=args))
    logme(f"[green]Saved the output of the command to {groupDir}/{outputFile}.txt", "debug")
else:
    command = sys.argv[1]
    logme(f"[yellow]sys.argv[1] = {command}", 'debug')
    outputsinDir = [f for f in os.listdir(groupDir) if os.path.isfile(os.path.join(groupDir, f)) and f.startswith(command)]
    outputsLen = len(outputsinDir)
    if outputsLen == 0:
        logme(f"[red]{command} was never cached but requested!", 'error')
        print("ERR: This command was never cached")
        logme(f"[red]Exiting.", 'error')
        exit()
    elif outputsLen == 1:
        logme(f"[green]Cache found for command {command}.")
        with open(os.path.join(groupDir, outputsinDir[0])) as f:
            logme(f"[yellow]Reading cache for command {command}", "debug")
            contents = f.read()
            logme(f"Setting up syntax highlighting for rich.syntax.Syntax function...")
            syntax = Syntax(contents, "python", theme="monokai", line_numbers=True)
            console = Console()
            logme(f"[yellow]Printing the code...")
            console.print(syntax)
            logme(f"Done without errors.")
    else:
        logme(f"[red]Multiple caches found!", 'warning')
        print("WARN: Multiple caches found! Please choose one:")
        for f in outputsinDir:
            print(str(outputsinDir.index(f)) + " = " + f)
        opt = input(f"Choose: (0 to {len(outputsinDir) - 1}): ")
        try:
            opt = int(opt)
        except ValueError:
            logme("[red]Non integer input from user!", "error")
            print("\n[ERR] Invalid input! [ERR]\n")
            exit()
        print("")
        try:
            with open(os.path.join(groupDir, outputsinDir[opt])) as f:
             contents = f.read()
             logme(f"Setting up syntax highlighting for rich.syntax.Syntax function...")
             syntax = Syntax(contents, "bash", theme="monokai", line_numbers=True)
             console = Console()
             logme(f"[yellow]Printing the code...")
             console.print(syntax)
             logme(f"Done without errors.")
        except IndexError:
            logme("[red]Index error!", "error")
            logme("[red]User gave a number that was not in the list!", "error")
            print("[ERR] Invalid choice [ERR]")