#!/usr/bin/env python
from pywinauto.application import Application
import time

LAST_CLASS = 0x66                                  # Exclude everything after Demon King

def main():
    # Prepare Rom and Modules paths TODO: Acquire these via user input
    romPath = r'"C:\Users\lucas\ROMs\GBA\Fire{SPACE}Emblem{SPACE}-{SPACE}The{SPACE}Sacred{SPACE}Stones{SPACE}{(}USA,{SPACE}Australia{)}.gba"'
    modulePath = r'"C:\Users\lucas\FE{SPACE}Modding\Nightmare\Game{SPACE}Boy{SPACE}Advance{SPACE}Modules\FE8{SPACE}Nightmare{SPACE}modules\Class{SPACE}&{SPACE}Character{SPACE}editors\FE8{SPACE}Class{SPACE}Editor.nmm"'

    # Open application
    app = Application(backend="uia").start(r'C:\Users\Lucas\FE Modding\Nightmare\Nightmare.exe', timeout=30)

    noFile = app.NightmareNoFileOpen                # Create dialogue for initial window
    noFile.wait('ready', timeout=30)                # Wait for window to open
    noFile.print_control_identifiers()              # Print info
    printNewlines(5)
    loadRom(noFile, romPath)                        # Load ROM whose growths will be edited
    openFile = app.NightmareFireEmblemSacredStones  # Create dialogue for new window 
    openFile.wait('ready', timeout=30)              # Make sure window is open
    openFile.print_control_identifiers()            # Print info
    printNewlines(5)
    loadModule(openFile, modulePath)                # Load module 
    openFile.print_control_identifiers()            # Print info
    printNewlines(5)

    alterClassGrowths(openFile, 'u', 40)            # Increase Enemy Growth Rates by 40%        
    time.sleep(5)
    openFile.menu_select("File -> Save Rom")        # Save changes to ROM


def loadRom(dlg, romPath):
    # Loads Rom in Nightmare
    # Assumes romPath is is passed in as raw text with properly formatted escape characters
    # i.e. r'"C:\Users\Username\Path\To\Folder\And\Rom{SPACE}With{SPACE}Spaces{SPACE}And{SPACE}{(}Parentheses{)}"'
    dlg.menu_select("File -> Open Rom")
    dlg.Open.FilenameEdit.type_keys(romPath)
    dlg.Open.OpenButton3.click()

def loadModule(dlg, modulePath):
    # Loads Module for Open Rom in Nightmare
    # Assumes modulePath is is passed in as raw text with properly formatted escape characters
    # i.e. r'"C:\Users\Username\Path\To\Folder\And\Module{SPACE}With{SPACE}Spaces{SPACE}And{SPACE}{(}Parentheses{)}"'
    dlg.menu_select("Module -> Load Modules")
    dlg.Open.FilenameEdit.type_keys(modulePath)
    dlg.Open.OpenButton3.click()

def alterClassGrowths(dlg, mode, arg):
    # Alters all class growths using specified Nightmare dialogue window
    # dlg: Dialogue/Initial Window with module loaded and on first class
    # Direction: 'u' for up/increase, 'd' for down/decrease, 's' for set
    # arg: usage depends on mode, if increase/decrease, it's the delta, if set, then its the value to set it to
    dropdown = dlg.Pane.Combobox0.Open
    match mode:
        case 'u':
            # Increase growths
            for i in range(LAST_CLASS-1):
                dropdown.click()                        # Open class dropdown
                dlg.type_keys("0")                      # Select next class
                dlg.type_keys("{TAB}")                  # Confirm 
                increaseGrowths(dlg.classNamePane, arg) # Increase Growths
                dlg.type_keys("{ENTER}")                # Save changes
        case 'd':
            # Decrease growths
            for i in range(LAST_CLASS-1):
                dropdown.click()                        # Open class dropdown
                dlg.type_keys("0")                      # Select next class
                dlg.type_keys("{TAB}")                  # Confirm 
                decreaseGrowths(dlg.classNamePane, arg) # Increase Growths
                dlg.type_keys("{ENTER}")                # Save changes
        case 's':
            # Set growths
            for i in range(LAST_CLASS-1):
                dropdown.click()                        # Open class dropdown
                dlg.type_keys("0")                      # Select next class
                dropdown.click()                        # Confirm 
                setGrowths(dlg.classNamePane, arg)      # Set Growths
                dlg.type_keys("{ENTER}")                # Save changes
            
def increaseGrowths(dlg, delta):
    # Increases all class growths by [delta]%
    # dlg = dialogue for class/unit
    increaseStatGrowth(dlg.HPGrowthEdit0, delta)       # HP
    increaseStatGrowth(dlg.STRMGCGrowthEdit0, delta)   # STR/MGC
    increaseStatGrowth(dlg.SKLGrowthEdit0, delta)      # SKL
    increaseStatGrowth(dlg.SPDGrowthEdit0, delta)      # SPD
    increaseStatGrowth(dlg.DEFGrowthEdit0, delta)      # DEF
    increaseStatGrowth(dlg.MDFGrowthEdit0, delta)      # MDF
    increaseStatGrowth(dlg.LUKGrowthEdit0, delta)      # LUK

def increaseStatGrowth(dlg_growth, delta):
    # Set growth to 127 if over 128, otherwise you get negative value
    newGrowth = int(dlg_growth.get_value()) + delta
    if(newGrowth > 127):
        newGrowth = 127
    dlg_growth.set_text(newGrowth)

def decreaseGrowths(dlg, delta):
    # Decrease all class growths by [delta]%
    # dlg = dialogue for class/unit
    # Helper function used to handle new growths potentially being < 0
    decreaseStatGrowth(dlg.HPGrowthEdit0, delta)       # HP
    decreaseStatGrowth(dlg.STRMGCGrowthEdit0, delta)   # STR/MGC
    decreaseStatGrowth(dlg.SKLGrowthEdit0, delta)      # SKL
    decreaseStatGrowth(dlg.SPDGrowthEdit0, delta)      # SPD
    decreaseStatGrowth(dlg.DEFGrowthEdit0, delta)      # DEF
    decreaseStatGrowth(dlg.MDFGrowthEdit0, delta)      # MDF
    decreaseStatGrowth(dlg.LUKGrowthEdit0, delta)      # LUK

def decreaseStatGrowth(dlg_growth, delta):
    # Set growth to 0 if difference would result in value < 0
    newGrowth = int(dlg_growth.get_value()) - delta
    if(newGrowth < 0):
        newGrowth = 0
    dlg_growth.set_text(newGrowth)

def setGrowths(dlg, growth):
    # Sets all class growths to [growth]%
    # dlg = dialogue for class/unit
    if(growth < 0):
        # Something's wrong, just fall back on 0
        growth = 0
    dlg.HPGrowthEdit0.set_text(growth)                  # HP
    dlg.STRMGCGrowthEdit0.set_text(growth)              # STR/MGC
    dlg.SKLGrowthEdit0.set_text(growth)                 # SKL
    dlg.SPDGrowthEdit0.set_text(growth)                 # SPD
    dlg.DEFGrowthEdit0.set_text(growth)                 # DEF
    dlg.MDFGrowthEdit0.set_text(growth)                 # RES
    dlg.LUKGrowthEdit0.set_text(growth)                 # LUK
    return

def printNewlines(numLines):
    # Just for debugging
    for i in range(numLines):
        print()

if __name__ == '__main__':
    main()