import os.path, os
import sys

cachierDir = '{}/.cachier'.format(os.path.expanduser("~"))
counter = 1

def uniquify(path):
    global counter
    filename, extension = os.path.splitext(path)
    while os.path.exists(path):
        path = filename + extension + "." + counter
        counter+=1
    return path

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
    command = uniquify(sys.argv[2])
    commandName = command.split(" ")[0]
    if os.path.isfile(f'{groupDir}/{command}.json'):
        os.system(f"{uniquify(f'{command}')} | tee {groupDir}/{command}.json.{str(counter)}")
    else:
        os.system(f"{command} | tee {groupDir}/{command}.json")
    print('running "' + command + '". command name is: ' + commandName)
    # save output in groupDir/{commandName}.txt
    # save commandName, command args and file path to groupDir/{commandName}.json
