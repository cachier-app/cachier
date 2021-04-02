import os.path

cachierDir = '{}/.cachier'.format(os.path.expanduser("~"))

# making sure the .cachier directory is present
if not os.path.exists(cachierDir):
    print('WARN: ~/.cachier is not present, creating it now')
    os.makedirs(cachierDir)
