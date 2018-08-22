import random

#capture some global vars from makeDict
#firstWord = 0
#lastWord = 0
#wordDict = 0

def mimic(filename):

    #input text sample from .txt file into single string
    infile = open(filename)
    blockString = infile.read()
    infile.close()

    #clean block string (remove newline, space out mid punc, etc)
    blockString = blockString.replace('\n', ' ')
    blockString = blockString.replace(',', ' ,')
    blockString = blockString.replace(';', ' ;')
    blockString = blockString.replace(':', ' :')
    if blockString[-1] == '.':
        blockString = blockString.strip()[0:-1]

    #turn string into sentence list
    sentenceList = blockString.split('. ')

    #capture lists of first and last words
    firstWord = []
    for sentence in sentenceList:
        firstWord.append(sentence.split()[0])
    lastWord = []
    for sentence in sentenceList:
        lastWord.append(sentence.split()[-1])

    #revert to string then split to word list (inefficient?)
    blockString = ' '.join(sentenceList)
    wordList = blockString.split()
    wordList.append('END')

    wordDict = {}

    #assign words to dict keys with values list of following words
    for i in range(len(wordList)-1):
        key = wordList[i]
        if key in firstWord:
            key = key.lower()
        if key not in wordDict.keys():
            wordDict[key] = []
        wordDict[key].append(wordList[i+1])

    #build a sentence using word dict and random.choice
    retList = [random.choice(firstWord)]
    i = 0
    while i < len(retList):
        nextWord = random.choice(wordDict[retList[i].lower()])
        retList.append(nextWord)
        if nextWord
        if nextWord in lastWord:
            if random.randrange(3) == 0:
                break
        i += 1
        if i > 25:
            break
    
    retString = ' '.join(retList)
    retString = retString.replace(' ;', ';')
    retString = retString.replace(' :', ';')
    retString = retString.replace(' ,', ',')

    print(retString)
    
    
    

mimic('Cthulu.txt')
