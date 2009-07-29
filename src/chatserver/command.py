import re
import logging as log
log.basicConfig(level=log.DEBUG)

COMMAND_GRAMMAR = {
    "LOGIN": re.compile(r"^\s*(\w+)$"),
    "LOGOUT": re.compile(r"^$"),
    "JOIN": re.compile(r"^\s*#(\w+)$"),
    "PART": re.compile(r"^\s*#(\w+)$"),
    "MSG": re.compile(r"^\s*(#?)(\w+) .+$")
}
 
SERVER_COMMANDS = ["GOTROOMMSG",
                   "GOTUSERMSG"]

COMMANDS = COMMAND_GRAMMAR.keys() + SERVER_COMMANDS              

def ParseCommand(rawCmd):
    rawCmd = rawCmd.strip()
    command = rawCmd.split(" ")[0].upper().strip()
    parameters = rawCmd[len(command):].strip()
    return command, parameters

def ValidateCommand(rawCmd):
    try:
        command, parameters = ParseCommand(rawCmd)
    except:
        raise
    
    if not COMMAND_GRAMMAR.has_key(command):
        return False
    elif re.match(COMMAND_GRAMMAR[command], parameters) is None:
        return False
    else:
        return True