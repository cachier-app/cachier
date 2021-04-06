
# Cachier

Cache commands with ease using **cachier**

# Installing

```
git clone https://github.com/cachier-app/cachier
cd cachier
sudo ./setup.py
```

# Basic Usage

```
Usage: cachier [options] [command]
```

## Examples

```
cachier run "ls" 
```
This will run ls and save it in the `default` cache

```
cachier ls
```
This will retrieve every ls command cached, you will be asked which one to retrieve in case there are multiple caches of same command

# Advanced Usage

Cachier uses groups. Each group is a collection of command caches, you can switch groups using the `-g` argument.

# Pentesting Use Case

If you are pentesting a network, you might want to keep track of your recon commands' output, for example, nmap, dirbuster, etc. Cachier makes it easy to store these information for later usage, it will also syntax highlight the output to make it prettier to look at!

For example you might have different groups, for different targets!

## Pentesting Use Case: Examples

### Performing the nmap scan

```bash
# Runnig an nmap scan against 10.0.198.246
cachier run "nmap 10.0.198.246 -sC -sV" -g 10.0.198.246
# Note we are in the "10.0.198.246" group

# Runnig an nmap scan against 10.0.4.1
cachier run "nmap 10.0.4.1 -sC -sV" -g 10.0.4.1
# Note we are in the "10.0.4.1" group
```

It would be hard to keep track of each output, we would have to write to different files and cat each every time we want to get the ports of the specific target, using cachier is so easy.

### Retriving the port scan

```bash
# Retriving the nmap command in the 10.0.198.246 group
cachier nmap -g 10.0.198.246

# Retriving the nmap command in the 10.0.4.1 group
cachier nmap -g 10.0.4.1
```

# Other arguments & examples

```
--debug: Enable debug mode.
--clear-cache: Clear all saved caches.
--no-highlight: Turn of syntax highlighting while printing cached data.
Example:
        cachier run ls  #For caching a command.
        cachier ls      #For showing cache of a command.
        cachier run ls --debug  #For caching a command with debug mode enabled.
        cachier --clear-cache   #For clearing all cache.
        cachier ls --no-highlight       #For showing cache of a command.
```
