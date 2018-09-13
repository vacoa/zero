# Cannot use logging in Thonny

LEVEL = 10

def setLevel(lvl):
    global LEVEL
    LEVEL = lvl

def debug(str):
    printlevel(10,str)
    
def info(str):
    printlevel(20,str)
    
def warning(str):
    printlevel(30,str)
    
def error(str):
    printlevel(40,str)
    
def critical(str):
    printlevel(50,str)
    
def printlevel(lvl,str):
    if lvl>=LEVEL:
        print(str)