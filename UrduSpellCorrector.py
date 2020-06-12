# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 08:41:34 2020

@author: Mehar Fatima Khan
"""
import os
from collections import Counter
import operator

with open("jang.txt","r+", encoding='utf-8') as jangFile:
    corpus = set(jangFile.readlines()[0:])
jangFile.close()

i = 0 
index = {}
for term in corpus:
    index[i] = term.split()
    i = i + 1
        
#print(countVocab)
wordIndex = []
for eachListID, eachList in index.items():
    for oneWord in eachList:
        wordIndex.append(oneWord)

countVocab = len(wordIndex)
#print(wordIndex) 
#print(countVocab)
#print(Counter(wordIndex))
unigrams = Counter(wordIndex)
#print(uWords)
#print(unigrams)

#f = open("words.txt", "w+", encoding="utf-8")
#for uniWord, wordCount in unigrams.items():
#    uniWord = str(uniWord)
#    wordCount = str(wordCount)
#    f.writelines(wordCount + "\t\t\t" + uniWord + "\n")
#f.close()

bigrams = []
bigrams = [(wordIndex[i-1], wordIndex[i]) for i in range(0, len(wordIndex))]

biwords = Counter(bigrams)

#print(biwords)
#print(bigrams)
#f = open("biwords.txt", "w+", encoding="utf-8")
#for biWord, wordCount in biwords.items():
#    biWord = str(biWord)
#    wordCount = str(wordCount)
#    f.writelines(wordCount + "\t\t\t" + biWord + "\n")
#f.close()

biwordProb = {}
for biWord, bicount in biwords.items():
    biwordProb[biWord] = biwords.get(biWord)/unigrams.get(biWord[0])
    
#print(biwordProb)
#print(len(biwordProb))

#f = open("biwordProbabilities.txt", "w+", encoding="utf-8")
#for biWords, probabilities in biwordProb.items():
#    biWords = str(biWords)
#    probabilities = str(probabilities)
#    f.writelines(biWords + "\t\t\t" + probabilities + "\n")
#f.close()

with open("jang_errors.txt","r+", encoding='utf-8') as jangErrorFile:
    errorCorpus = list(jangErrorFile.readlines()[0:])
jangErrorFile.close()

j = 1
indexError = {}
for term in errorCorpus:
    indexError[j] = term.split()
    j = j + 1

#print(indexError)
with open("wordlist.txt","r+", encoding='utf-8') as wordListFile:
    wordList = set((wordListFile.readlines()[0:]))
wordListFile.close()

#print(wordList)
#print(len(wordList))

mWords = []
for word in wordList:
    mWords.append(word.strip())
    
myWords = Counter(mWords)
#print(myWords)
#print(mWords)
#print(len(mWords))

k = 1
hashErrors = {}
nn = []
for rowID, errWords in indexError.items():
    m = 1
    for oneW in errWords:
        if oneW not in mWords:
            hashErrors[k] = (rowID,m,oneW)
            nn.append(oneW)
            k = k + 1
        m = m + 1
        
#print(hashErrors)
#print(len(hashErrors))
#print((Counter(nn)))

def candidates(word): 
    return ((knownInDictionary(editDistanceOf1(word)) and knownInDictionary(editDistanceOf2(word))) or [word] or knownInDictionary([word]))

def knownInDictionary(words): 
    return set(w for w in words if w in myWords)

def editDistanceOf1(word):
    urduLetters=u"آ ا ب پ ت ٹ ث ج چ ح خ د ڈ ذ ر ڑ ز ژ س ش ص ض ط ظ ع غ ف ق ک گ ل م ن و ہ ھ ء ی ئ ے"
    splitWord     = [(word[:x], word[x:])    for x in range(len(word) + 1)]
    deletion    = [LEFT + RIGHT[1:]               for LEFT, RIGHT in splitWord if RIGHT]
    transposition = [LEFT + RIGHT[1] + RIGHT[0] + RIGHT[2:] for LEFT, RIGHT in splitWord if len(RIGHT)>1]
    replacement   = [LEFT + c + RIGHT[1:]           for LEFT, RIGHT in splitWord if RIGHT for c in urduLetters]
    insertion    = [LEFT + c + RIGHT              for LEFT, RIGHT in splitWord for c in urduLetters]
    return set(deletion + transposition + replacement + insertion)

def editDistanceOf2(word): 
    return set(edit2 for edit1 in editDistanceOf1(word) for edit2 in editDistanceOf1(edit1))
 
#print(candidates('تلب'))

allCandidates = []
testDict = []
test = []
for hashIndex, hashValue in hashErrors.items():
    rowValue = hashValue[0]
    columnValue = hashValue[1]
    sentence = indexError[rowValue]
    allCandidates = candidates(hashValue[2])
    
#        print(sentence[columnValue-1]) original
#        print(sentence[columnValue-2]) prev
#        print(sentence[columnValue]) next
    if (sentence[columnValue-2] not in wordIndex):
        wordIndex.append(sentence[columnValue-2])
    if (sentence[columnValue] not in wordIndex):
        wordIndex.append(sentence[columnValue])
        
    for allThePossibilities in allCandidates:
        if allThePossibilities not in wordIndex:
            wordIndex.append(allThePossibilities)    
        test1 = (sentence[columnValue - 2],allThePossibilities)
        test2 = (allThePossibilities,sentence[columnValue])
        test.append(test1)
        test.append(test2)
unigrams = Counter(wordIndex)
testDict = Counter(test)

#print(len(testDict))
#print(testDict)
newCounter = biwords + testDict
#print(newCounter)
for errBiWord, theirCount in testDict.items():
    if errBiWord not in bigrams:
        biwordProb[errBiWord] = 0
        #print(theirCount)
        #biwords[errBiWord] = theirCount
                 
biwordProb = {}
for biWord, bicount in newCounter.items():
#    print(biWord[0])
#    print(unigrams.get(biWord[0]))
    biwordProb[biWord] = (((newCounter.get(biWord)) + 1)/((unigrams.get(biWord[0])) + countVocab))
    
#f = open("biwordProbabilities.txt", "w+", encoding="utf-8")
#for biWords, probabilities in biwordProb.items():
#    biWords = str(biWords)
#    probabilities = str(probabilities)
#    f.writelines(biWords + "\t\t\t" + probabilities + "\n")
#f.close()

with open("jang_nonerrors.txt","r+", encoding='utf-8') as jangNonErrorFile:
    nonerrorCorpus = list(jangNonErrorFile.readlines()[0:])
jangNonErrorFile.close()
p = 1
indexNonError = {}
indexAccurateLoc = {}
for eachSentence in nonerrorCorpus:
    indexNonError[p] = eachSentence.split()
    s = 1
    for eachTerm in indexNonError[p]:
        indexes = (p,s)
        indexAccurateLoc[indexes] = eachTerm
        s = s + 1
    p = p + 1
#print(indexNonError)
#print(indexAccurateLoc)
storeCandidateProb = {}
checkProb = {}
check = {}
g = 0
q = 0
for hashIndex, hashValue in hashErrors.items():
    rowValue = hashValue[0]
    columnValue = hashValue[1]
    #print(columnValue)
    sentence = indexError[rowValue]
    allCandidates = candidates(hashValue[2]) 
    storeCandidateProb = {}
    for allThePossibilities in allCandidates:
        test1 = (sentence[columnValue - 2],allThePossibilities)
        test2 = (allThePossibilities,sentence[columnValue])
        createIndex = (allThePossibilities,hashValue[2],rowValue,columnValue-1)
        storeCandidateProb[allThePossibilities] = (biwordProb.get(test1) * biwordProb.get(test2))
        checkProb[createIndex] = (biwordProb.get(test1) * biwordProb.get(test2))
        q  = q + 1
    
    sorted_l = sorted(storeCandidateProb.items(), key=operator.itemgetter(1),reverse=True)
    #print(l)
    makeIndex = (rowValue,columnValue)
    l=sorted_l[0:10]
    for val in l:
        keyOfCandidate = (val[0],hashValue[2], rowValue, columnValue-1)
        g = g + 1
        
        #if val[0] in indexNonError[rowValue]:
      #  print(indexAccurateLoc[makeIndex])
        if (val[0] == indexAccurateLoc[makeIndex]):
            check[keyOfCandidate] = (storeCandidateProb.get(val[0]),"YES")
            
        #elif (val[0] not in indexNonError[rowValue]):
        elif (val[0] != indexAccurateLoc[makeIndex]):
            check[keyOfCandidate] = (storeCandidateProb.get(val[0]),"NO")
            

#l=list(storeCandidateProb.items())
#print(l)
#sorted_l = sorted(storeCandidateProb.items(), key=operator.itemgetter(1),reverse=True)
#print(sorted_l)

#f = open("candidateProbabilities.txt", "w+", encoding="utf-8")
#for keys, probabilities in check.items():
#    keys = (keys[0],keys[1])
#    keys = str(keys)
#    probabilities = str(probabilities)
#    f.writelines(keys + "\t" + probabilities + "\n")
#f.close()
#
#f = open("allProbabilities.txt", "w+", encoding="utf-8")
#for keys, probabilities in checkProb.items():
#    keys = str(keys)
#    probabilities = str(probabilities)
#    f.writelines(keys + "\t\t\t" + probabilities + "\n")
#f.close()
