import random
import string

class Mimicker:

    replacementInSecond = {',': ' ,', ';': ' ;',
                           ':': ' :', '?': ' ?',
                           '!': ' !', '.': ' . '}
    replacementInFirst = {'Prof.': 'Prof', 'Dr.': 'Dr',
                          'Mr.': 'Mr', 'Mrs.': 'Mrs',
                          'Ms.': 'Ms', '\n': ' ',
                          '"': ' ', '“': ' ',
                          '”': ' ', '(': ' ',
                          ')': ' ', '—': ' '}
    replacementOut = {' ;': ';', ' :': ':',
                      ' ,': ',', ' .': '.'}
    punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~—'
    
    def __init__(self, filename):
        self.filename = filename
        self.wordList = []
        self.firstWord = []
        self.lastWord = []
        self.permaCaps = ['I']
        self.wordDict = {}
        self.sentenceList = []
        self.clean()
        self.findFirstWords()
        self.findLastWords()
        self.findPermaCaps()
        self.makeDict()

    def clean(self):
        infile = open(self.filename)
        blockString = infile.read()
        infile.close()

        for key in self.replacementInFirst:
            blockString = blockString.replace(key, self.replacementInFirst[key])

        tempList = blockString.split()
        tempListCopy = tempList[:]
        for word in tempListCopy:
            if '.' in word[0:-1]:
                #if word[-1] not in self.punctuation:
                tempList.remove(word)
            if len(word) == 2 and word[1] == '.':
                tempList.remove(word)

        blockString = ' '.join(tempList)

        for key in self.replacementInSecond:
            blockString = blockString.replace(key, self.replacementInSecond[key])

        self.wordList = blockString.split()
        delList = []
        for i in range(2,len(self.wordList)-1):
            if self.wordList[i] in self.punctuation:
                if self.wordList[i+1] in self.punctuation:
                    delList.append(i+1)
        while len(delList) > 0:
            del self.wordList[delList.pop()]

    def findFirstWords(self):
        self.firstWord.append(self.wordList[0])
        for i in range(len(self.wordList) - 1):
            if self.wordList[i] == '.' or self.wordList[i] == '?' or self.wordList[i] == '!':
                if self.wordList[i+1] not in string.punctuation:
                    self.firstWord.append(self.wordList[i+1])

    def findLastWords(self):
        for i in range(1,len(self.wordList)):
            if self.wordList[i] == '.' or self.wordList[i] == '?' or self.wordList[i] == '!':
                self.lastWord.append(self.wordList[i-1])

    def findPermaCaps(self):
        wordSet = set(self.wordList)
        uniqueWordList = list(wordSet)
        uniqueWordList.sort()
        for word in uniqueWordList:
            if word[0].isupper():
                if word.lower() not in wordSet:
                    self.permaCaps.append(word)

    def makeDict(self):
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
        first = random.choice(self.firstWord)
        if first not in self.permaCaps:
            first = first.lower()
        retList = [first]
        i = 0
        try:
            while i < len(retList):
                nextWord = random.choice(self.wordDict[retList[i]])
                retList.append(nextWord)
                if nextWord == '.' or nextWord == '?':
                    if len(retList) > 8:
                        break
                if len(retList) > 25:
                    break
                i += 1
        except:
            pass
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
        while len(self.sentenceList) <= num:
            self.makeSentence()
        ret = ' '.join(self.sentenceList)
        self.sentenceList = []
        return ret
        

        
                            
        
