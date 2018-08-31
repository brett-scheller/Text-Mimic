import random
import textwrap

class Mimicker:

    #table to replace out difficult punctuation with empty string or space
    replacementInFirst = {'Prof.': 'Prof', 'Dr.': 'Dr',
                          'Mr.': 'Mr', 'Mrs.': 'Mrs',
                          'Ms.': 'Ms', '\n': ' ',
                          '"': ' ', '“': ' ',
                          '”': ' ', '(': ' ',
                          ')': ' ', '—': ' ',
                          '...': '.'}
    #table to replace to put space before significant punctuation 
    replacementInSecond = {',': ' ,', ';': ' ;',
                           ':': ' :', '?': ' ?',
                           '!': ' !', '.': ' . '}
    #table to replace out space after sig. punc. at very end
    replacementOut = {' ;': ';', ' :': ':',
                      ' ,': ',', ' .': '.'}
    #custom list of punctuation (does not include hyphen, includes dash)
    punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~—'

    #list of sentence-ending punctuation (not used in current version)
    #endPunc = '.?!'

    def __init__(self, filename):

        #initialize variables
        self.filename = filename
        
        #personal style to initialize empties, not necessary in general
        self.wordList = []
        self.firstWord = []
        self.lastWord = []
        self.permaCaps = []
        self.wordDict = {}
        self.sentenceList = []

        #call methods to generate data structures
        self.clean()
        self.findFirstWords()
        self.findLastWords()
        self.findPermaCaps()
        self.makeDict()

    #import file, clean text, generate wordList: ordered list of words in text
    def clean(self):

        #import txt file, throw exception if bad input
        try:
            infile = open(self.filename)
            blockString = infile.read()
            infile.close()
        except:
            print('I/O Error: Could not find or read file. Must be .txt')

        #use first replacement table
        for key in self.replacementInFirst:
            blockString = blockString.replace(key, self.replacementInFirst[key])

        #remove words with '.' in beginning or middle (like '.03' or 'I.L.')
        #remove single char words that end in '.' (like in 'J. R. R. Tolkein')
        tempList = blockString.split()
        tempListCopy = tempList[:]
        for word in tempListCopy:
            if '.' in word[0:-1]:
                tempList.remove(word)
            if len(word) == 2 and word[1] == '.':
                tempList.remove(word)
        blockString = ' '.join(tempList)

        #use second replacement table
        for key in self.replacementInSecond:
            blockString = blockString.replace(key, self.replacementInSecond[key])

        #split block string into list of words
        #note: these punctuation marks . , : ; ? ! are treated as words!
        self.wordList = blockString.split()
                  
        #remove accidental successive punctuations, only up to one between two words
        delList = []
        for i in range(2,len(self.wordList)-1):
            if self.wordList[i] in self.punctuation:
                if self.wordList[i+1] in self.punctuation:
                    delList.append(i+1)
        while len(delList) > 0:
            del self.wordList[delList.pop()]

        #self.wordList is a list of every word in sample text, in order

    def findFirstWords(self):
        #generate list self.firstWord of first word in each sentence
        self.firstWord.append(self.wordList[0])
        for i in range(len(self.wordList) - 1):
            if self.wordList[i] == '.' or self.wordList[i] == '?' or self.wordList[i] == '!':
                if self.wordList[i+1] not in self.punctuation:
                    self.firstWord.append(self.wordList[i+1])

    def findLastWords(self):
        #generate list self.lastWord of last word in each sentence
        for i in range(1,len(self.wordList)):
            if self.wordList[i] == '.' or self.wordList[i] == '?' or self.wordList[i] == '!':
                self.lastWord.append(self.wordList[i-1])

    def findPermaCaps(self):
        #generate list self.permaCaps of words that always appear capitalized
        #work for initial caps and total caps
        wordSet = set(self.wordList)
        uniqueWordList = list(wordSet)
        uniqueWordList.sort()
        for word in uniqueWordList:
            if word[0].isupper():
                if word.lower() not in wordSet:
                    self.permaCaps.append(word)

    def makeDict(self):
        #make each unique word a key in the dictionary wordDict
        #make each key's value a list
        #replete list with each word that follows that key anywhere in text
        for i in range (len(self.wordList) - 1):
            key = self.wordList[i]
            val = self.wordList[i+1]
            if len(val) > 1:
                val = ''.join(c for c in val if c not in self.punctuation)
            if key not in self.permaCaps:
                if key.isalpha():
                    key = key.lower()
            if val not in self.permaCaps:
                if val.isalpha():
                    val = val.lower()
            if key not in self.wordDict.keys():
                self.wordDict[key] = [val]
            else:
                self.wordDict[key].append(val)

    def makeSentence(self):
        #choose random element of list of first words
        #choose random member of that words value list in wordDict
        #continue until hitting end punctuation or 25 words
        #exception handling for dictionary errors: exit
        #if last word not valid, exit
        #if valid, use replacement table out
        #ensure period at end and capitalization at start
        #push sentence onto sentenceList
        first = random.choice(self.firstWord)
        if first not in self.permaCaps:
            first = first.lower()
        retList = [first]
        i = 0
        try:
            while i < len(retList):
                nextWord = random.choice(self.wordDict[retList[i]])
                retList.append(nextWord)
                if nextWord == '.' or nextWord == '?' or nextWord == '!':
                    if len(retList) > 2:
                        break
                    else:
                        return
                if len(retList) > 25:
                    break
                i += 1
        except:
            return
        if retList[-1] not in self.lastWord:
            return
        retString = ' '.join(retList)
        for key in self.replacementOut:
            retString = retString.replace(key, self.replacementOut[key])
        retString = retString.strip()
        if retString[-1] != '.':
            retString += '.'
        if retString[-2] in self.punctuation:
            retString = retString[0:-2] + retString[-1]
        if retString[0].islower():
            retString = retString[0].upper() + retString[1:]
        self.sentenceList.append(retString)

    def makeParagraph(self, num = 5):
        #call self.makeSentence until sentenceList has length num
        #join into single string, reset var, and return paragraph
        while len(self.sentenceList) < num:
            self.makeSentence()
        ret = ' '.join(self.sentenceList)
        self.sentenceList = []
        return ret
