import random
import string

class mimicker:

    replacement = {'Prof': 'Prof', 'Dr.': 'Dr',
                   'Mr.': 'Mr', 'Mrs.': 'Mrs',
                   'Ms.': 'Ms', '\n': ' ',
                   ',': ' ,', ';': ' :',
                   ':': ' :', '?': ' ?',
                   '!': ' !', '.': ' . ',
                   '"': ' ', '“': ' ',
                   '”': ' ', '(': ' ',
                   ')': ' ', '—': ' '}
    
    def __init__(self, filename):
        self.filename = filename

    def clean(self):
        infile = open(self.filename)
        blockString = infile.read()
        infile.close()

        tempList = blockString.split()
        tempListCopy = tempList[:]
        for word in tempListCopy:
            if '.' in word[0:-1]:
                tempList.remove(word)
            if len(word) == 2 and word[1] == '.':
                tempList.remove(word)

        blockString = ' '.join(tempList)

        for key in self.replacement:
            blockstring = blockstring.replace(key, self.replacement[key])

        

        
                            
        
