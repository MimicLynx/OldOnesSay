RESET  = '\033[0m'
BOLD   = '\033[1m'
DIM    = '\033[2m'

def fg(n):
    return f'\033[38;5;{n}m'

# Palette
GOLD    = fg(220)   # warm gold — borders, titles
DGOLD   = fg(136)   # dark gold — ornaments
PURPLE  = fg(55)    # deep purple
LPUR    = fg(93)    # bright purple
MPUR    = fg(57)    # medium purple
GREEN   = fg(64)    # dark green
LGRN    = fg(76)    # sickly bright green
MGRN    = fg(70)    # medium green
DGRN    = fg(22)    # very dark green
WHITE   = fg(255)   # white
GREY    = fg(245)   # medium grey
DGREY   = fg(238)   # dark grey
LGREY   = fg(250)   # light grey
YELLOW  = fg(226)   # bright yellow
DYEL    = fg(178)   # dark yellow
TEAL    = fg(37)    # teal
LTEAL   = fg(51)    # light teal
BLUE    = fg(27)    # blue
DBLUE   = fg(18)    # dark blue
LBLUE   = fg(81)    # light blue
RED     = fg(124)   # dark red
ORANGE  = fg(208)   # orange
DRED    = fg(88)    # very dark red
MAROON  = fg(52)    # maroon
SEAFOAM = fg(30)    # dark seafoam
