import os.path, os
import sys
import datetime

from rich.console import Console
from rich.syntax import Syntax


cachierDir = '{}/.cachier'.format(os.path.expanduser("~"))

# making sure the .cachier directory is present
if not os.path.exists(cachierDir):
    print('WARN: "{}" is not present, creating it now'.format(cachierDir))
    os.makedirs(cachierDir)

group = 'default'
groupDir = '{}/{}'.format(cachierDir, group)

# making sure the group directory exists in cachierDir
if not os.path.exists(groupDir):
    print('WARN: "{}" is not present, creating it now'.format(groupDir))
    os.makedirs(groupDir)

if sys.argv[1] == 'run':
    # run command in sys.argv[2]
    command = sys.argv[2]
    commandName = command.split(" ")[0]
    outputFile = commandName + "_" + datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    os.system(f"{command} | tee \"{groupDir}/{outputFile}.txt\"")
    #print('running "' + command + '". command name is: ' + commandName)
    # save output in groupDir/{commandName}.txt
    # save commandName, command args and file path to groupDir/{commandName}.json
else:
    command = sys.argv[1]
    outputsinDir = [f for f in os.listdir(groupDir) if os.path.isfile(os.path.join(groupDir, f)) and f.startswith(command)]
    outputsLen = len(outputsinDir)
    if outputsLen == 0:
        print("ERR: This command was never cached")
    elif outputsLen == 1:
        with open(os.path.join(groupDir, outputsinDir[0])) as f:
            contents = f.read()
            syntax = Syntax(contents, "python", theme="monokai", line_numbers=True)
            console = Console()
            console.print(syntax)
    else:
        print("WARN: Multiple commands were ran! Please choose one:")
        for f in outputsinDir:
            print(str(outputsinDir.index(f)) + " = " + f)
        opt = input(f"Choose: (0 to {len(outputsinDir) - 1}): ")
        opt = int(opt)
        print("")
        with open(os.path.join(groupDir, outputsinDir[opt])) as f:
            contents = f.read()
            syntax = Syntax(contents, "python", theme="monokai", line_numbers=True)
            console = Console()
            console.print(syntax)



