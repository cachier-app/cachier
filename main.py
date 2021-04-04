from logging import debug, warn
import os.path, os
import sys
import datetime
from rich.console import Console
from rich.syntax import Syntax

DEBUG = False

def log(message, type=None):
    if not DEBUG:
        return 
    if type=='info':
        log(message, extra={"markup": True})
    elif type=='debug':
        logging.debug(message, extra={"markup": True})
    elif type=='warning':
        logging.warning(message, extra={"markup": True})
    elif type=='error':
        logging.error(message, extra={"markup": True})
    else:
        log(message, extra={"markup": True})

# Working here ~ Mr. RC
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


cachierDir = '{}/.cachier'.format(os.path.expanduser("~"))

# making sure the .cachier directory is present
log(f"Checking if {cachierDir} exits...")
if not os.path.exists(cachierDir):
    
    log(f"Checking if {cachierDir} exits...")
    print('WARN: "{}" is not present, creating it now'.format(cachierDir))
    os.makedirs(cachierDir)

group = 'default'
groupDir = '{}/{}'.format(cachierDir, group)
# making sure the group directory exists in cachierDir
log(f"Checking if {groupDir} exits...")
if not os.path.exists(groupDir):
    print('WARN: "{}" is not present, creating it now'.format(groupDir))
    os.makedirs(groupDir)

log(f"Checking arguments...")
if sys.argv[1] == 'run':
    log(f"[yellow]sys.argv[1] = run")
    # run command in sys.argv[2]
    command = sys.argv[2]
    commandName = command.split(" ")[0]
    outputFile = commandName + "_" + datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    log(f"[green]Running command: {command}", 'debug')
    os.system(f"{command} | tee \"{groupDir}/{outputFile}.txt\"")
    log(f"[green]Saved the ouput of the command to {groupDir}/{outputFile}.txt", "debug")

else:
    command = sys.argv[1]
    log(f"[yellow]sys.argv[1] = {command}", 'debug')
    outputsinDir = [f for f in os.listdir(groupDir) if os.path.isfile(os.path.join(groupDir, f)) and f.startswith(command)]
    outputsLen = len(outputsinDir)
    if outputsLen == 0:
        log(f"[red]{command} was never cached but requested!", 'error')
        print("ERR: This command was never cached")
        log(f"[red]Exiting.", 'error')
        exit()
    elif outputsLen == 1:
        log(f"[green]Cache found for command {command}.")
        with open(os.path.join(groupDir, outputsinDir[0])) as f:
            log(f"[yellow]Reading cache for command {command}", "debug")
            contents = f.read()
            log(f"Setting up syntax highlighting for rich.syntax.Syntax function...")
            syntax = Syntax(contents, "python", theme="monokai", line_numbers=True)
            console = Console()
            log(f"[yellow]Printing the code...")
            console.print(syntax)
            log(f"Done without errors.")
    else:
        log(f"[red]Multiple caches found!", 'warning')
        print("WARN: Multiple caches found! Please choose one:")
        for f in outputsinDir:
            print(str(outputsinDir.index(f)) + " = " + f)
        opt = input(f"Choose: (0 to {len(outputsinDir) - 1}): ")
        try:
            opt = int(opt)
        except ValueError:
            log("[red]Non integer input from user!", "error")
            print("\n[ERR] Invalid input! [ERR]\n")
            exit()
        print("")
        try:
            with open(os.path.join(groupDir, outputsinDir[opt])) as f:
             contents = f.read()
             log(f"Setting up syntax highlighting for rich.syntax.Syntax function...")
             syntax = Syntax(contents, "bash", theme="monokai", line_numbers=True)
             console = Console()
             log(f"[yellow]Printing the code...")
             console.print(syntax)
             log(f"Done without errors.")
        except IndexError:
            log("[red]Index error!", "error")
            log("[red]User gave a number that was not in the list!", "error")
            print("\n[ERR] Invalid choice [ERR]")