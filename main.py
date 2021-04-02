import os.path
import sys

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
    print('running "' + command + '". command name is: ' + commandName)
    # save output in groupDir/{commandName}.txt
    # save commandName, command args and file path to groupDir/{commandName}.json
