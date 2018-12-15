####################
## Enter your character set and the UI will
## generate various spacing strings for you.
## Works in RoboFont, Glyphs, and DrawBot.
####################
## Ethan Cohen, updated 12/15/18
####################

from vanilla import *
from AppKit import NSPasteboard, NSArray
from random import shuffle
from aardvarks_english import aardvarksEnglish
from aardvarks_english import combos

basicUC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
basicLC = "abcdefghijklmnopqrstuvwxyz"
basicFigures = "0123456789"

def clipboard(text):
    p = NSPasteboard.generalPasteboard()
    p.clearContents()
    a = NSArray.arrayWithObject_(text)
    p.writeObjects_(a)

####################
## functions that create spacing strings
####################

def LCSequence(charSet):
    txt = "nnnnnnnnnnnnnnnnnnnnn\nnunununununununununun\nniuiniuiniuiniuiniuin\nbqbqbqbqbqbqbqbqbqbqbq\nbdpqbdpqbdpqbdpqbdpqbdpq\nniupdniubqniupdniubqniupdniubqniu\nuinpduinbquinpduinbquinpduinbquin\nuonipodiuoniboqiuonipodiuoniboqi\nnouiqobinouiqobinouiqobinouiqobi\n"
    for x in range(len(charSet)):
        if charSet[x] in basicLC:
            txt += "nn" + charSet[x]
    txt += "nn" + "\n"
    for x in range(len(charSet)):
        if charSet[x] in basicLC:
            txt += "oo" + charSet[x]
    txt += "oo" + "\n"
    for x in range(len(charSet)):
        if charSet[x] in basicLC:
            txt += "niu" + charSet[x] + "niu"
    txt += "\n"
    return txt

def longStrings(charSet, ctrl1, ctrl2):
    txt = ""
    for x in range(len(charSet)):
        txt += ctrl1 + charSet[x]
    txt += ctrl1 + "\n"
    for x in range(len(charSet)):
        txt += ctrl2 + charSet[x]
    txt += ctrl2 + ctrl2 + "\n"
    return txt

def shortStrings(charSet, ctrl1, ctrl2):
    txt = ""
    for x in range(len(charSet)):
        txt += ctrl1 + ctrl1 + charSet[x] + ctrl1 + ctrl1 + charSet[x] + ctrl2 + ctrl2 + charSet[x] + ctrl2 + ctrl2 + "\n"
    return txt    

def betweenAll(charSet, figuresBetweenLetters=False):
    txt = ""
    controls = ""
    if figuresBetweenLetters == False:
        for x in range(len(charSet)):
            if charSet[x] in basicLC or charSet[x] in basicUC or charSet[x] in basicFigures:
                controls += charSet[x]
    else:
        for x in range(len(charSet)):
            if charSet[x] in basicLC or charSet[x] in basicUC:
                controls += charSet[x]        
            
    for x in range(len(controls)):
        for y in range(len(charSet)):
            txt += controls[x] + charSet[y]
        txt += charSet[x] + "\n"
    return txt

def withAnotherCase(charSet, otherCase):
    txt = ""
    if otherCase == lowercase:
        ctrl1 = "n"
        ctrl2 = "o"
    elif otherCase == uppercase:
        ctrl1 = "H"
        ctrl2 = "O"
    txt += shortStrings(charSet, ctrl1, ctrl2) + "\n"
    for x in range(len(charSet)):
        txt += ctrl1 + charSet[x]
    txt += ctrl1 + "\n"
    for x in range(len(charSet)):
        txt += ctrl2 + charSet[x]
    txt += ctrl2 + "\n"
    return txt

def aardvarker(uppercase, lowercase, symbols):
    charSet = uppercase + lowercase
    if "." in symbols:
        charSet += "."
    aardvarks = ""
    for combo in combos:
        if combo[0] in charSet and combo[1] in charSet:
            newvark = ""
            key = combo[0] + combo[1]
            if len(aardvarksEnglish[key]) > 1:
                shuffle(aardvarksEnglish[key])
                increment = 0
                newvark = ""
                while newvark == "" and increment < len(aardvarksEnglish[key]):
                    for word in range(len(aardvarksEnglish[key])):
                        currentWord = ""
                        for letter in range(len(aardvarksEnglish[key][word])):
                            if aardvarksEnglish[key][word][letter] in charSet:
                                currentWord = currentWord + aardvarksEnglish[key][word][letter]
                            if len(currentWord) == len(aardvarksEnglish[key][word]):
                                newvark = currentWord
                    increment += 1
            if len(newvark) <= 3 and "." in charSet:
                newvark += "."
            if len(newvark) > 1:
                aardvarks += newvark + " "
    return aardvarks


class interface(object):

    def __init__(self):

####################
## window UI
####################

        windowWidth = 400
        padding = 10
        increment = 20
        column = 150
        width = windowWidth - padding * 2
        self.w = FloatingWindow((windowWidth, increment * 40), title="Copy Spacing Strings to Clipboard")

## lowercase entry
        self.lowercase = "abcdefghijklmnopqrstuvwxyz"
        self.w.lowercaseLabel = TextBox((padding, padding, -10, 20), "Enter lowercase:")
        self.w.lowercaseEntry = EditText((column, padding, -10, 19),
                            callback=self.lowercaseEntryCallback, sizeStyle="small")
        self.w.lowercaseEntry.set(self.lowercase)

## uppercase entry
        self.uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.w.uppercaseLabel = TextBox((padding, padding + increment, -10, 20), "Enter uppercase:")
        self.w.uppercaseEntry = EditText((column, padding + increment, -10, 19),
                            callback=self.uppercaseEntryCallback, sizeStyle="small")
        self.w.uppercaseEntry.set(self.uppercase)

## figures entry
        self.figures = "0123456789$"
        self.w.figuresLabel = TextBox((padding, padding + increment * 2, -10, 20), "Enter figures:")
        self.w.figuresEntry = EditText((column, padding + increment * 2, -10, 19),
                            callback=self.figuresEntryCallback, sizeStyle="small")
        self.w.figuresEntry.set(self.figures)

## punctuation and symbols entry
        self.symbols = ".,:;!?-–—‚„“”‘’@#*()~"
        self.w.symbolsLabel = TextBox((padding, padding + increment * 3, -10, 20), "Enter punct/symbols:")
        self.w.symbolsEntry = EditText((column, padding + increment * 3, -10, 19),
                            callback=self.symbolsEntryCallback, sizeStyle="small")
        self.w.symbolsEntry.set(self.symbols)

####################
## checkbox default values
####################

        self.includeLabels = 0
        self.LC1 = 1
        self.LC2 = 1
        self.LC4 = 1
        self.UC1 = 1
        self.UC3 = 1
        self.AARD = 0
        self.FIG1 = 1
        self.FIG3 = 1
        self.FIG4 = 1
        self.FIG6 = 1
        self.SYMB1 = 1
        self.SYMB3 = 1


####################
## select/deselect all buttons
####################

        self.w.line = HorizontalLine((padding, padding + increment * 4.45, -10, 1))
        self.w.selectAll = Button((padding, padding + increment * 4.9, width * 0.49, 20), "Select All", callback=self.selectAllCallback)
        self.w.deselectAll = Button((padding + width * 0.51, padding + increment * 4.9, width * 0.49, 20), "Deselect All", callback=self.deselectAllCallback)

####################
## checkboxes
####################

## lowercase
        self.w.line1 = HorizontalLine((padding, padding + increment * 6.45, -10, 1))
        self.w.LC1 = CheckBox((padding, padding + increment * 7, width, 20), "LC Sequence", callback=self.LC1Callback, value=True)
        self.w.LC2 = CheckBox((padding, padding + increment * 8, width, 20), "LC between n and o", callback=self.LC2Callback, value=True)
        self.w.LC4 = CheckBox((padding, padding + increment * 9, width, 20), "All LC between all LC", callback=self.LC4Callback, value=True)

## uppercase
        self.w.line2 = HorizontalLine((padding, padding + increment * 10.45, -10, 1))
        self.w.UC1 = CheckBox((padding, padding + increment * 11, width, 20), "UC between H and O", callback=self.UC1Callback, value=True)
        self.w.UC3 = CheckBox((padding, padding + increment * 12, width, 20), "All UC between all UC", callback=self.UC3Callback, value=True)

## aardvark strings
        self.w.line3 = HorizontalLine((padding, padding + increment * 13.45, -10, 1))
        self.w.AARD = CheckBox((padding, padding + increment * 14, width, 20), "Aardvark Strings", callback=self.AARDCallback, value=False)

## figures
        self.w.line4 = HorizontalLine((padding, padding + increment * 15.45, -10, 1))
        self.w.FIG1 = CheckBox((padding, padding + increment * 16, width, 20), "Figures between 0 and 1", callback=self.FIG1Callback, value=True)
        self.w.FIG3 = CheckBox((padding, padding + increment * 17, width, 20), "All figures between all figures", callback=self.FIG3Callback, value=True)
        self.w.FIG4 = CheckBox((padding, padding + increment * 18, width, 20), "Figures between n and o", callback=self.FIG4Callback, value=True)
        self.w.FIG6 = CheckBox((padding, padding + increment * 19, width, 20), "Figures between H and O", callback=self.FIG6Callback, value=True)
        
## punctuation & symbols
        self.w.line5 = HorizontalLine((padding, padding + increment * 20.45, -10, 1))
        self.w.SYMB1 = CheckBox((padding, padding + increment * 21, width, 20), "Punctuation/symbols between n and o", callback=self.SYMB1Callback, value=True)
        self.w.SYMB3 = CheckBox((padding, padding + increment * 22, width, 20), "Punctuation/symbols between H and O", callback=self.SYMB3Callback, value=True)

## other
        self.w.line6 = HorizontalLine((padding, padding + increment * 23.45, -10, 1))
        self.w.includeLabels = RadioGroup((padding, padding + increment * 23.8, width, 20), ["Don't Label Strings", "Label the Strings"], callback=self.includeLabelsCallback, isVertical=False)
        self.w.includeLabels.set(0)
        self.w.txtDisplay = TextEditor((padding, padding + increment * 25, width, increment * 12.5), callback=self.txtDisplayCallback, readOnly=True)
        self.w.txtDisplay.set(self.makeTxt())
        self.w.clipboardButton = Button((padding, padding + increment * 37.9, width, 20), "Copy to Clipboard", callback=self.clipboardCallback)

        self.w.open()

####################
## callbacks
####################

## character set entry callbacks
    def lowercaseEntryCallback(self, sender):
        self.lowercase = sender.get()
        self.w.txtDisplay.set(self.makeTxt())
    def uppercaseEntryCallback(self, sender):
        self.uppercase = sender.get()
        self.w.txtDisplay.set(self.makeTxt())
    def figuresEntryCallback(self, sender):
        self.figures = sender.get()
        self.w.txtDisplay.set(self.makeTxt())
    def symbolsEntryCallback(self, sender):
        self.symbols = sender.get()
        self.w.txtDisplay.set(self.makeTxt())

## LC clipboard CheckBox callbacks
    def LC1Callback(self,sender):
        self.LC1 = sender.get()
        self.w.txtDisplay.set(self.makeTxt())
    def LC2Callback(self,sender):
        self.LC2 = sender.get()
        self.w.txtDisplay.set(self.makeTxt())
    def LC4Callback(self,sender):
        self.LC4 = sender.get()
        self.w.txtDisplay.set(self.makeTxt())

## LC clipboard CheckBox callbacks
    def UC1Callback(self,sender):
        self.UC1 = sender.get()
        self.w.txtDisplay.set(self.makeTxt())
    def UC3Callback(self,sender):
        self.UC3 = sender.get()
        self.w.txtDisplay.set(self.makeTxt())

## aardvarker callback
    def AARDCallback(self,sender):
        self.AARD = sender.get()
        self.w.txtDisplay.set(self.makeTxt())

## figures clipboard CheckBox callbacks
    def FIG1Callback(self,sender):
        self.FIG1 = sender.get()
        self.w.txtDisplay.set(self.makeTxt())
    def FIG3Callback(self,sender):
        self.FIG3 = sender.get()
        self.w.txtDisplay.set(self.makeTxt())
    def FIG4Callback(self,sender):
        self.FIG4 = sender.get()
        self.w.txtDisplay.set(self.makeTxt())
    def FIG6Callback(self,sender):
        self.FIG6 = sender.get()
        self.w.txtDisplay.set(self.makeTxt())

## punctuation and symbols clipboard CheckBox callbacks
    def SYMB1Callback(self,sender):
        self.SYMB1 = sender.get()
        self.w.txtDisplay.set(self.makeTxt())
    def SYMB3Callback(self,sender):
        self.SYMB3 = sender.get()
        self.w.txtDisplay.set(self.makeTxt())

## text display box callback
    def txtDisplayCallback(self, sender):
        pass

## include labels callback
    def includeLabelsCallback(self,sender):
        self.includeLabels = sender.get()
        self.w.txtDisplay.set(self.makeTxt())

## (de)select all callbacks
    def selectAllCallback(self, sender):
        self.LC1 = 1
        self.LC2 = 1
        self.LC4 = 1
        self.UC1 = 1
        self.UC3 = 1
        self.AARD = 1
        self.FIG1 = 1
        self.FIG3 = 1
        self.FIG4 = 1
        self.FIG6 = 1
        self.SYMB1 = 1
        self.SYMB3 = 1
        self.w.LC1.set(True)
        self.w.LC2.set(True)
        self.w.LC4.set(True)
        self.w.UC1.set(True)
        self.w.UC3.set(True)
        self.w.AARD.set(True)
        self.w.FIG1.set(True)
        self.w.FIG3.set(True)
        self.w.FIG4.set(True)
        self.w.FIG6.set(True)
        self.w.SYMB1.set(True)
        self.w.SYMB3.set(True)
        self.w.txtDisplay.set(self.makeTxt())

    def deselectAllCallback(self, sender):
        self.LC1 = 0
        self.LC2 = 0
        self.LC4 = 0
        self.UC1 = 0
        self.UC3 = 0
        self.AARD = 0
        self.FIG1 = 0
        self.FIG3 = 0
        self.FIG4 = 0
        self.FIG6 = 0
        self.SYMB1 = 0
        self.SYMB3 = 0
        self.w.LC1.set(False)
        self.w.LC2.set(False)
        self.w.LC4.set(False)
        self.w.UC1.set(False)
        self.w.UC3.set(False)
        self.w.AARD.set(False)
        self.w.FIG1.set(False)
        self.w.FIG3.set(False)
        self.w.FIG4.set(False)
        self.w.FIG6.set(False)
        self.w.SYMB1.set(False)
        self.w.SYMB3.set(False)
        self.w.txtDisplay.set(self.makeTxt())


## make txt function

    def makeTxt(self):
        txt = ""
        if self.LC1 == 1:
            if self.includeLabels == 1:
                txt += "LC Sequence\n\n"
            txt += LCSequence(self.lowercase) + "\n\n"
        if self.LC2 == 1:
            if self.includeLabels == 1:
                txt += "LC between n and o\n\n"
            txt += shortStrings(self.lowercase, "n", "o") + "\n" + longStrings(self.lowercase, "n", "o") + "\n\n"
        if self.LC4 == 1:
            if self.includeLabels == 1:
                txt += "All LC between all LC\n\n"
            txt += betweenAll(self.lowercase) + "\n\n"
        if self.UC1 == 1:
            if self.includeLabels == 1:
                txt += "UC between H and O\n\n"
            txt += shortStrings(self.uppercase, "H", "O") + "\n" + longStrings(self.uppercase, "H", "O") + "\n\n"
        if self.UC3 == 1:
            if self.includeLabels == 1:
                txt += "All UC between all UC\n\n"
            txt += betweenAll(self.uppercase) + "\n\n"
        if self.AARD == 1:
            if self.includeLabels == 1:
                txt += "Aardvark Strings\n\n"
            txt += aardvarker(self.uppercase, self.lowercase, self.symbols)
        if self.FIG1 == 1:
            if self.includeLabels == 1:
                txt += "Figures between 0 and 1\n\n"
            txt += shortStrings(self.figures, "0", "1") + "\n" + longStrings(self.figures, "0", "1") + "\n\n"
        if self.FIG3 == 1:
            if self.includeLabels == 1:
                txt += "All figures between all figures\n\n"
            txt += betweenAll(self.figures) + "\n\n"
        if self.FIG4 == 1:
            if self.includeLabels == 1:
                txt += "Figures between n and o\n\n"
            txt += shortStrings(self.figures, "n", "o") + "\n" + longStrings(self.figures, "n", "o") + "\n\n"
        if self.FIG6 == 1:
            if self.includeLabels == 1:
                txt += "Figures between H and O\n\n"
            txt += shortStrings(self.figures, "H", "O") + "\n" + longStrings(self.figures, "H", "O") + "\n\n"
        if self.SYMB1 == 1:
            if self.includeLabels == 1:
                txt += "Punctuation/symbols between n and o\n\n"
            txt += shortStrings(self.symbols, "n", "o") + "\n" + longStrings(self.symbols, "n", "o") + "\n\n"
        if self.SYMB3 == 1:
            if self.includeLabels == 1:
                txt += "Punctuation/symbols between H and O\n\n"
            txt += shortStrings(self.symbols, "H", "O") + "\n" + longStrings(self.symbols, "H", "O")
        return txt
        
## copy selection to clipboard
    def clipboardCallback(self,sender):
        clipboard(self.makeTxt())



interface()