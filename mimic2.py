import random
import string

def mimic2(filename):

    #input text sample from .txt file into single string
    infile = open(filename)
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
    
    
    blockString = blockString.replace('Prof.', 'Prof')
    blockString = blockString.replace('Dr.', 'Dr')
    blockString = blockString.replace('Mr.', 'Mr')
    blockString = blockString.replace('Mrs.', 'Mrs')
    blockString = blockString.replace('Ms.', 'Ms')
    #clean block string (remove newline, space out mid punc, etc)
    blockString = blockString.replace('\n', ' ')
    blockString = blockString.replace(',', ' ,')
    blockString = blockString.replace(';', ' ;')
    blockString = blockString.replace(':', ' :')
    blockString = blockString.replace('?', ' :')
    blockString = blockString.replace('!', ' :')
    blockString = blockString.replace('.', ' . ')
    blockString = blockString.replace('"', ' ')
    blockString = blockString.replace('“', ' ')
    blockString = blockString.replace('”', ' ')
    blockString = blockString.replace('(', ' ')
    blockString = blockString.replace(')', ' ')
    #blockString = blockString.replace('-', ' ')
    blockString = blockString.replace('—', ' ')
    
    wordList = blockString.split()

    '''wordListCopy = wordList[:]
    for i in range(len(wordListCopy)):
        if len(wordListCopy[i]) == 1:
            if word.isalpha():
                if word != 'a' and word != 'I':
                    wordList.remove(word)'''

    #wordList = [word.replace('Prof', 'Prof.') for word in wordList]
    #wordList = [word.replace('Dr', 'Dr.') for word in wordList]
    wordList = [word.replace('Mr', 'Mr.') for word in wordList]
    wordList = [word.replace('Mrs', 'Mrs.') for word in wordList]
    wordList = [word.replace('Ms', 'Ms.') for word in wordList]

    #keep inventory of first words in sentences
    firstWord = [wordList[0]]
    for i in range(len(wordList) - 1):
        if wordList[i] == '.' or wordList[i] == '?':
            if wordList[i+1] not in string.punctuation:
                firstWord.append(wordList[i+1])
                
    #keep inventory of perma-initial-caps 'I' and proper nouns
    permaInitialCaps = ['I']
    wordSet = set(wordList)
    uniqueWordList = list(wordSet)
    uniqueWordList.sort()
    for word in uniqueWordList:
        if word[0].isupper():
            if word.lower() not in wordSet:
                permaInitialCaps.append(word)

    #build dictionary of words and successors
    wordDict = {}
    for i in range (len(wordList) - 1):
        key = wordList[i]
        val = wordList[i+1]
        if len(val) > 1:
            val = ''.join(c for c in val if c not in string.punctuation)
        if key not in permaInitialCaps:
            if key.isalpha():
                key = key.lower()
        if val not in permaInitialCaps:
            if val.isalpha():
                val = val.lower()
        if key not in wordDict.keys():
            wordDict[key] = [val]
        else:
            wordDict[key].append(val)

    


    #build a sentence: first word
    first = random.choice(firstWord)
    if first not in permaInitialCaps:
        first = first.lower()
    retList = [first]
    #rest of sentence
    i = 0
    try:
        while i < len(retList):
            nextWord = random.choice(wordDict[retList[i]])
            retList.append(nextWord)
            if nextWord == '.' or nextWord == '?':
                if len(retList) > 8:
                    break
            if len(retList) > 25:
                return ''
            i += 1
    except:
        return ''

    retString = ' '.join(retList)
    retString = retString.replace(' ;', ';')
    retString = retString.replace(' :', ';')
    retString = retString.replace(' ,', ',')
    retString = retString.replace(' .', '.')
    ret = ''.join(retString[0].upper() + retString[1:])

    return ret

def paragraph(filename, num):
    retStr = ''
    for i in range(num):
        retStr += mimic2(filename) + ' '
    newfile = filename[0:-4] + 'GENERATED.txt'
    outfile = open(newfile, 'a')
    outfile.write(retStr + '\n' + '\n')
    outfile.close()
    return retStr


print(paragraph('MonkeyHouseExcerpt.txt', 8))

