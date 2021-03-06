from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import seed
from random import shuffle
import tkinter as tk
import random

#Command to run when clicking the Randomize Button
def randomize():
    #Arrays for Finalized Setting Values
    finalBLocker = []
    finalTNS = []
    finalLevels = levelEntrances[:]

    #Start Spoiler Log Generation
    log = open("spoilerlog.txt","w+")

    #Write Settings to Spoiler Log
    log.write("Randomizer Settings" + "\n")
    log.write("-------------------" + "\n")
    log.write("Level Progression Randomized: " + str(varLevelProgression.get()) + "\n")
    if str(varLevelProgression.get()) == "True":
        log.write("Game Length: " + str(dropdownLength.get()) + "\n")
        log.write("Seed: " + str(textboxSeed.get()) + "\n")
    log.write("All Kongs Unlocked: " + str(varKongs.get()) + "\n")
    log.write("All Moves Unlocked: " + str(varMoves.get()) + "\n")
    log.write("Tag Anywhere Enabled: " + str(varTagAnywhere.get()) + "\n")
    log.write("Shorter Hideout Helm: " + str(varShorterHelm.get()) + "\n")
    log.write("Quality of Life Changes: " + str(varQOL.get()) + "\n")
    log.write("\n")

    #Fill Arrays with chosen game length values
    if str(dropdownLength.get()) == "Vanilla":
        finalBLocker = vanillaBLocker[:]
        finalTNS = vanillaTNS[:]
    elif str(dropdownLength.get()) == "Shorter":
        finalBLocker = shorterBLocker[:]
        finalTNS = shorterTNS[:]

    #Shuffle Level Progression and Write to Spoiler Log
    if str(varLevelProgression.get()) == "True":
        seed(textboxSeed.get())
        shuffle(finalLevels)
        log.write("Level Order: " + "\n")
        for x in finalLevels:
            log.write(str(finalLevels.index(x) + 1) + ". " + x + " ")
            log.write("(B Locker: " + str(finalBLocker[finalLevels.index(x)]) + " GB, ")
            log.write("Troff n Scoff: " + str(finalTNS[finalLevels.index(x)]) + " bananas)")
            log.write("\n")
        log.write("8. Hideout Helm ")
        log.write("(B Locker: " + str(finalBLocker[7]) + " GB)")
    log.close()

    messagebox.showinfo("DK64 Level Progression Randomizer", "Randomized successfully! Spoiler log written to spoilerlog.txt")

    root.destroy()

#Command to disable the randomizer sub-options if the Level Progression Randomizer is not selected
def randoEnable():
    dropdownLength.config(state="readonly" if varLevelProgression.get() else DISABLED)
    textboxSeed.config(state=NORMAL if varLevelProgression.get() else DISABLED)

#Command to generate a random 6 digit number
def randomSeed():
    genNum = random.randrange(1, 10**6)
    genSixDigits = str(genNum).zfill(6)
    textboxSeed.insert(0, genSixDigits)

#Generate the window
root = tk.Tk()
root.title("DK64 Level Progression Randomizer")
root.geometry("250x320")
root.resizable(False, False)
root.wm_attributes('-topmost', 'true')
root.wm_attributes('-toolwindow', 'true')
frame1 = Frame(root)
frame1.pack()
frame2 = Frame(root)
frame2.pack()
frame3 = Frame(root)
frame3.pack()

#Create a ToolTip function since TKinter doesn't do this natively
#Source: https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter
class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 250   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_attributes('-topmost', 'true')
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

#Create an Entry function for 6 digit numbers only
class NumEntry(ttk.Entry):
    def __init__(self, master = None, **kwargs):
        self.var = tk.StringVar(master)
        self.var.trace('w', self.validate)
        ttk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.get, self.set = self.var.get, self.var.set
    def validate(self, *args):
        value = self.get()
        if not value.isdigit():
            self.set(''.join(x for x in value if x.isdigit()))
        if len(value) > 6:
            self.set(value[:6])

#Interaction Variables
varLevelProgression = BooleanVar()
varKongs = BooleanVar()
varMoves = BooleanVar()
varTagAnywhere = BooleanVar()
varShorterHelm = BooleanVar()
varQOL = BooleanVar()

#Option Arrays
levelEntrances = ["Jungle Japes", "Angry Aztec", "Frantic Factory", "Gloomy Galleon", "Fungi Forest", "Crystal Caves", "Creepy Castle"]

gameLengthOptions = ["Vanilla", "Shorter"]

vanillaBLocker= [1, 5, 15, 30, 50, 65, 80, 100]
vanillaTNS = [60, 120, 200, 250, 300, 350, 400]

shorterBLocker = [1, 3, 10, 20, 35, 50, 65, 80]
shorterTNS = [50, 75, 100, 125, 150, 200, 250]

#Randomize Level Progression Checkbox
checkLevelProgression = Checkbutton(frame1, text = "Randomize Level Progression", variable = varLevelProgression, command = randoEnable)
checkLevelProgression.pack(padx = 5, pady = 5)
checkLevelProgression.select()
checkLevelProgression_toolTip = CreateToolTip(checkLevelProgression, 
"This option will randomize the level lobby entrances. " + "\n" +
"The level will match the B Locker and Troff n Scoff requirements of the slot that it falls in. " + "\n" +
"Hideout Helm will always be the final level. ")

#Game Length Dropdown
dropdownLength = ttk.Combobox(frame1, values = gameLengthOptions, width = 10, state = "readonly")
dropdownLength.pack(padx = 5, pady = 5)
dropdownLength.current(0)
dropdownLength_toolTip = CreateToolTip(dropdownLength, 
"Select the length of the game generated. " + "\n" + "\n" +
"Vanilla B Locker Progression: 1-5-15-30-50-65-80-100 " + "\n" +
"Vanilla Troff n Scoff Progression: 60-120-200-250-300-350-400 " + "\n" + "\n" +
"Shorter B Locker Progression: 1-3-10-20-35-50-65-80 " + "\n" +
"Shorter Troff n Scoff Progression: 50-75-100-125-150-200-250 ")

#Seed Textbox
textboxSeed = NumEntry(frame2, width = 8, justify = "center")
textboxSeed.insert(0, str(random.randrange(1, 10**6)).zfill(6))
textboxSeed.pack(padx = 5, pady = 5, side=LEFT)
textboxSeed_toolTip = CreateToolTip(textboxSeed,
"You can either manually enter a 6 digit number or click the button to the right to pick one for you. " 
"This program will generate the game based off the number entered. ")

#Pick a Random Seed Number Button
buttonSeed = Button(frame2, text = "Random Seed", command = randomSeed)
buttonSeed.pack(padx = 5, pady = 5, side=LEFT)
buttonSeed_toolTip = CreateToolTip(buttonSeed,
"Click this button to randomly generate a 6 digit number to base the seed on.")

#Unlock All Kongs Checkbox
checkKongs = Checkbutton(frame3, text = "Unlock All Kongs", variable = varKongs)
checkKongs.pack(padx = 5, pady = 5)
checkKongs.select()
checkKongs_toolTip = CreateToolTip(checkKongs, 
"This option will make all 5 kongs available from the start without freeing them. " + "\n" +
"The golden bananas awarded when freeing specific kongs still must be collected even with this option on. ")

#Unlock All Moves Checkbox
checkMoves = Checkbutton(frame3, text = "Unlock All Moves", variable = varMoves)
checkMoves.pack(padx = 5, pady = 5)
checkMoves_toolTip = CreateToolTip(checkMoves,
"This option will make all moves available from the start without purchasing them. " + "\n" +
"Includes all Cranky, Funky and Candy purchasables. " + "\n" +
"Does not include access to JetPac in Cranky; you will still need 15 banana medals. ")

#Enable Tag Anywhere Checkbox
checkTagAnywhere = Checkbutton(frame3, text = "Enable Tag Anywhere", variable = varTagAnywhere)
checkTagAnywhere.pack(padx = 5, pady = 5)
checkTagAnywhere_toolTip = CreateToolTip(checkTagAnywhere,
"This option will allow you to switch kongs almost anywhere using DPad left or DPad right. " + "\n" +
"You will still need to unlock the kong you want if Unlock All Kongs isn't enabled. " + "\n" +
"You cannot switch kongs in rooms or areas that would otherwise break the puzzle. ")

#Shorter Hideout Helm Checkbox
checkShorterHelm = Checkbutton(frame3, text = "Shorter Hideout Helm", variable = varShorterHelm)
checkShorterHelm.pack(padx = 5, pady = 5)
checkShorterHelm_toolTip = CreateToolTip(checkShorterHelm,
"This option will shorten the time it takes to beat Hideout Helm with the following changes: " + "\n" +
"- You will spawn in the Blast o Matic room. " + "\n" +
"- Opens the roman numeral doors to each Kong's room. " + "\n" +
"- The gates in front of the music pads are gone. " + "\n" +
"- The 4 crown door is open. " + "\n" +
"- The Rareware/Nintendo Coin door is open. ")

#Quality of Life Changes Checkbox
checkQOL = Checkbutton(frame3, text = "Quality of Life Changes", variable = varQOL)
checkQOL.pack(padx = 5, pady = 5)
checkQOL_toolTip = CreateToolTip(checkQOL,
"This option enables the following quality of life changes to the game: " + "\n" +
"- Removes first time text. " + "\n" +
"- Removes first time boss cutscenes. " + "\n" +
"- Shorter Snide blueprint turn-in cutscenes. " + "\n" +
"- Shorter K Lumsy key turn-in cutscenes. " + "\n" +
"- Remove DK Rap from the startup sequence. " + "\n" +
"- Story Skip option in the main menu set to On by default" + "\n" +
"- Fast start: Training Barrels complete, start with Simian Slam and spawn in DK Isles. ")
 
#Generate Button
buttonGenerate = Button(frame3, text = "Generate Game", command = randomize)
buttonGenerate.pack(padx = 5, pady = 5)

#Initialize the GUI
root.mainloop()
