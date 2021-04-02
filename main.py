import json
import os.path, os
import sys
import datetime
from rich.console import Console
from rich.syntax import Syntax

DEBUG = False

# Working here ~ Mr. RC
def create_json(command, args=None, filename):
    json_struct = {
        "command": "",
        "args": tuple(),
        "filename": ""
    }
    json_struct["command"]=command
    if args:
        for i in args:
            json_struct["args"][i]=args[i]
    else:
        json_struct["args"][0]=None
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
if DEBUG:
    logging.info(f"Checking if {cachierDir} exits...")
if not os.path.exists(cachierDir):
    if DEBUG:    
        logging.info(f"Checking if {cachierDir} exits...")
    print('WARN: "{}" is not present, creating it now'.format(cachierDir))
    os.makedirs(cachierDir)

group = 'default'
groupDir = '{}/{}'.format(cachierDir, group)
# making sure the group directory exists in cachierDir
if DEBUG:
    logging.info(f"Checking if {groupDir} exits...")
if not os.path.exists(groupDir):
    print('WARN: "{}" is not present, creating it now'.format(groupDir))
    os.makedirs(groupDir)

if DEBUG:
    logging.info(f"Checking arguments...")
if sys.argv[1] == 'run':
    if DEBUG:
        logging.debug(f"[yellow]sys.argv[1] = run", extra={"markup": True})
    # run command in sys.argv[2]
    command = sys.argv[2]
    commandName = command.split(" ")[0]
    outputFile = commandName + "_" + datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    if DEBUG:
        logging.debug(f"[green]Running command: {command}", extra={"markup": True})
    os.system(f"{command} | tee \"{groupDir}/{outputFile}.txt\"")
    if DEBUG:
        logging.debug(f"[green]Saved the ouput of the command to {groupDir}/{outputFile}.txt", extra={"markup": True})
    #print('running "' + command + '". command name is: ' + commandName)
    # save output in groupDir/{commandName}.txt
    # save commandName, command args and file path to groupDir/{commandName}.json
else:
    command = sys.argv[1]
    if DEBUG:
        logging.debug(f"[yellow]sys.argv[1] = {command}", extra={"markup": True})
    outputsinDir = [f for f in os.listdir(groupDir) if os.path.isfile(os.path.join(groupDir, f)) and f.startswith(command)]
    outputsLen = len(outputsinDir)
    if outputsLen == 0:
        if DEBUG:
            logging.error(f"[red]{command} was never cached but requested!", extra={"markup": True})
        print("ERR: This command was never cached")
        if DEBUG:
            logging.warning(f"[red]Exiting.", extra={"markup": True})
        exit()
    elif outputsLen == 1:
        if DEBUG:
            logging.info(f"[green]Cache found for command {command}.", extra={"markup": True})
        with open(os.path.join(groupDir, outputsinDir[0])) as f:
            if DEBUG:
                logging.debug(f"[yellow]Reading cache for command {command}", extra={"markup": True})
            contents = f.read()
            if DEBUG:
                logging.info(f"Setting up syntax highlighting for rich.syntax.Syntax function...", extra={"markup": True})
            syntax = Syntax(contents, "python", theme="monokai", line_numbers=True)
            console = Console()
            if DEBUG:
                logging.info(f"[yellow]Printing the code...", extra={"markup": True})
            console.print(syntax)
            if DEBUG:
                logging.info(f"Done without errors.", extra={"markup": True})
    else:
        if DEBUG:
            logging.warning(f"[red]Multiple commands ran!", extra={"markup": True})
        print("WARN: Multiple commands were ran! Please choose one:")
        for f in outputsinDir:
            print(str(outputsinDir.index(f)) + " = " + f)
        opt = input(f"Choose: (0 to {len(outputsinDir) - 1}): ")
        opt = int(opt)
        print("")
        with open(os.path.join(groupDir, outputsinDir[opt])) as f:
             contents = f.read()
             if DEBUG:
                 logging.info(f"Setting up syntax highlighting for rich.syntax.Syntax function...", extra={"markup": True})
             syntax = Syntax(contents, "python", theme="monokai", line_numbers=True)
             console = Console()
             if DEBUG:
                 logging.info(f"[yellow]Printing the code...", extra={"markup": True})
             console.print(syntax)
             if DEBUG:
                 logging.info(f"Done without errors.", extra={"markup": True})
