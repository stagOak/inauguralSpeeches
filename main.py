# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 13:35:50 2017

@author: steveMorin
"""

def removePunc(aList, punct):
    # word_tokenize includes punctuation - get rid of these tokens
    periodIndex = []
    for i in range(0, len(aList)):
        if aList[i] in punct:
            #print(i, tokens[i])
            periodIndex.append(i)
    listMultiDelete(aList, periodIndex)
    return(aList)

def listMultiDelete(aList, indexes):
    # delete multiple elements from a list
    indexes = sorted(indexes, reverse = True)        
    for index in indexes:
        del aList[index]
        
def splitPeriodPairsAndAddToList(aList):
    addList = []
    removeList = []
    for i in range(0, len(aList)):
        if '.' in aList[i]:
            removeList.append(i)
            #print(aList[i])
            splitList = aList[i].split('.')
            #print(splitList)
            for word in splitList:
                addList.append(word)
    listMultiDelete(aList, removeList)
    return(aList + addList)  

def removeCommasAtEnd(aString):
    aList = aString.lower().split()
    addList = []
    removeList = []
    for i in range(0, len(aList)):
        if (',' in aList[i]):
            index = aList[i].index(',')
            numChar = len(aList[i])
            if(index == numChar-1):
                removeList.append(i)
                #print(aList[i])
                splitList = aList[i].split(',')
                #print(splitList)
                addList.append(splitList[0])
    listMultiDelete(aList, removeList)
    str1 = ' '.join(aList + addList)
    #print(str1)
    return(str1)

def getTokens(text, punct):
    # this function makes tokens
    tokens = word_tokenize(text.lower())
    # remove punctuation left by word_tokenizer
    tokens = removePunc(tokens, punct)
    # fix another word_tokenizer artifact
    tokens = splitPeriodPairsAndAddToList(tokens)
    return tokens

def query(aQuery, dictionary):
    # create query document and convert to tf-idf
    print('\nquery:\n')
    
    # remove commas from query
    #print('query as is:\n', aQuery)
    #print('\n')
    aQuery = removeCommasAtEnd(aQuery)
    print('query after comma removal:\n', aQuery)
    print('\n')
    
    # split the query into words
    queryDoc2 = aQuery.lower().split()
    print(queryDoc2)
    print('\n')

    # create a bag of words from query and print it out
    queryDocBOW2 = dictionary.doc2bow(queryDoc2)
    print(queryDocBOW2)
    for i in range(0, len(queryDocBOW2)):
        if i != len(queryDocBOW2)-1:
            print(dictionary[queryDocBOW2[i][0]], ', ', end = '', sep = '')
        else:
            print(dictionary[queryDocBOW2[i][0]])
    print('\n')    
   
    # run query bag of words thru tf-idf model and print results
    queryDoc_tF_iDF2 = tF_iDF[queryDocBOW2]
    print(queryDoc_tF_iDF2)
    for i in range(0, len(queryDoc_tF_iDF2)):
        if i != len(queryDocBOW2)-1:
            print(dictionary[queryDoc_tF_iDF2[i][0]], ', ', end = '', sep = '')
        else:
            print(dictionary[queryDoc_tF_iDF2[i][0]])
    print('\n')               
        
    # show array of document similarities to query and print it out
    sim2 = sims[queryDoc_tF_iDF2]
    #print('sim2 = ', sim2)
    print('query results:')
    for i in range(0, len(sim2)):
        print('    ', rawDocsNames[i], '=', sim2[i])
    
    # plot the results of inquiry
    tickRep = np.asarray([0, 1, 2, 5, 6, 9])
    subSim2Rep = [sim2[0], sim2[1], sim2[2], sim2[5], sim2[6], sim2[9]]
    tickDem = np.asarray([3, 4, 7, 8])
    subSim2Dem = [sim2[3], sim2[4], sim2[7], sim2[8]]
    fig,ax = plt.subplots()
    numTicks = np.asarray(list(range(len(rawDocsNames))))
    #ax.bar(numTicks, sim2, width = 0.8, color = 'r')
    ax.bar(tickRep, subSim2Rep, width = 0.8, color = 'r')
    ax.bar(tickDem, subSim2Dem, width = 0.8, color = 'b')
    ax.set_xticks(numTicks)
    ax.set_xticklabels(rawDocsNames, rotation = 45, ha = 'right')  
    plt.show()

# main
import gensim
from nltk.tokenize import word_tokenize

import os
import matplotlib.pyplot as plt
import numpy as np
#import sys
#sys.exit()

# get ready to deal with tokenizer artifacts
import string
punct = set(string.punctuation)
# punct.update('–-', '”', '’', '–-', '')

# start with a list of text documents (a list of lists where each document in 
# the collection of documents is a list itself) to be considered
with open('reagan1981_rep.txt', 'r') as myfile:
    reagan1981_rep = myfile.read().replace('\n', '')
with open('reagan1985_rep.txt', 'r') as myfile:
    reagan1985_rep = myfile.read().replace('\n', '')
with open('bush1989_rep.txt', 'r') as myfile:
    bush1989_rep = myfile.read().replace('\n', '')
with open('clinton1993_dem.txt', 'r') as myfile:
    clinton1993_dem = myfile.read().replace('\n', '')
with open('clinton1997_dem.txt', 'r') as myfile:
    clinton1997_dem = myfile.read().replace('\n', '') 
with open('bush2001_rep.txt', 'r') as myfile:
    bush2001_rep = myfile.read().replace('\n', '')
with open('bush2005_rep.txt', 'r') as myfile:
    bush2005_rep = myfile.read().replace('\n', '')                                                
with open('obama2009_dem.txt', 'r') as myfile:
    obama2009_dem = myfile.read().replace('\n', '')
with open('obama2013_dem.txt', 'r') as myfile:
    obama2013_dem = myfile.read().replace('\n', '')
with open('trump2017_rep.txt', 'r') as myfile:
    trump2017_rep = myfile.read().replace('\n', '')
rawDocs = [reagan1981_rep, reagan1985_rep, bush1989_rep, clinton1993_dem, 
           clinton1997_dem, bush2001_rep, bush2005_rep, obama2009_dem, 
           obama2013_dem, trump2017_rep]
rawDocsNames = ['reagan1981_rep', 'reagan1985_rep', 'bush1989_rep', 
                'clinton1993_dem', 'clinton1997_dem', 'bush2001_rep', 
                'bush2005_rep', 'obama2009_dem', 'obama2013_dem', 
                'trump2017_rep']

# convert the list of text documents into a list of tokenized documents
genDocs = [getTokens(text, punct) for text in rawDocs]
#print(genDocs)

# create a dictionary from the list of tokenized documents (a dictionary maps 
# every token in the list of tokenized documents into a number (index))
dictionary = gensim.corpora.Dictionary(genDocs)
num_words = len(dictionary)
print("Num words in dictionary: {}".format(num_words))
#i = 0
#for idx,word in dictionary.items():
#    i = i + 1
#    if i > 100:
#        break
#    else:
#        print(idx,word)

# create a corpus (a corpus is a list of bags of words)
# a bag of words is the term frequency (tf) of tf-idf. each document in the list
# of tokenized documents is converted into an ordered list of two-element tuples
# where the first element is the dictionary term index and the second element is
# the frequency with which that term occurs in that document. it is called a 
# "bag of words" because the order of words in the original doument is lost
corpus = [dictionary.doc2bow(genDoc) for genDoc in genDocs]
#print(corpus)

# create tf-idf model from corpus. num_nnz is the number of tokens
tF_iDF = gensim.models.TfidfModel(corpus)
print(tF_iDF)

# show document in text form, as tokens, bag of words, and tf-idf.
# Vectors are normalized so they sum to 1
print(rawDocs[0][0:50])
print(genDocs[0][0:5])
print(corpus[0][0:5])
print(tF_iDF[corpus][0][0:5])

# create similarity measure object in tf-idf space
# first arg is temp external storage
curPath = os.getcwd()
sims = gensim.similarities.Similarity(curPath, tF_iDF[corpus], num_features = 
                                      len(dictionary))
print(sims)

# some queries against the dictionary of inauguration speeches

theQuery0 = "I love love love the the Chief Justice and his minions"
query(theQuery0, dictionary)

theQuery1 = "I love the United States of America."
query(theQuery1, dictionary)

theQuery2 = "I am the master of the universe."
query(theQuery2, dictionary)

theQuery3 = "I want to go to war."
query(theQuery3, dictionary)

theQuery4 = "muslim muslims"
query(theQuery4, dictionary)

theQuery5 = "terror terrorist radical radicalized"
query(theQuery5, dictionary)

theQuery6 = """hate, abhorrence, 
    abomination, 
    anathema, 
    animosity, 
    animus, 
    antagonism, 
    antipathy, 
    aversion, 
    black beast, 
    bother, 
    bugbear, 
    bête noire, 
    detestation, 
    disgust, 
    enmity, 
    execration, 
    frost, 
    grievance,
    gripe, 
    hatred, 
    horror, 
    hostility, 
    ill will, 
    irritant, 
    loathing, 
    malevolence, 
    malignity, 
    mislike, 
    nasty look, 
    no love lost, 
    nuisance, 
    objection, 
    odium, 
    pain, 
    rancor, 
    rankling, 
    repugnance, 
    repulsion, 
    resentment, 
    revenge, 
    revulsion, 
    scorn, 
    spite, 
    trouble,
    venom"""
query(theQuery6, dictionary)

theQuery7 = """love, adulation, 
    affection, 
    allegiance, 
    amity, 
    amorousness, 
    amour, 
    appreciation, 
    ardency, 
    ardor, 
    attachment, 
    case, 
    cherishing, 
    crush, 
    delight, 
    devotedness, 
    devotion, 
    emotion, 
    enchantment, 
    enjoyment, 
    fervor, 
    fidelity, 
    flame, 
    fondness, 
    friendship, 
    hankering, 
    idolatry, 
    inclination, 
    infatuation, 
    involvement, 
    like, 
    lust, 
    mad for, 
    partiality, 
    passion, 
    piety, 
    rapture, 
    regard, 
    relish, 
    respect, 
    sentiment, 
    soft spot, 
    taste, 
    tenderness, 
    weakness, 
    worship, 
    yearning,
    zeal"""
query(theQuery7, dictionary)

theQuery8 = """peace, accord, 
    amity, 
    armistice, 
    cessation, 
    conciliation, 
    concord, 
    friendship, 
    love, 
    neutrality, 
    order, 
    pacification, 
    pacifism, 
    reconciliation, 
    treaty, 
    truce, 
    unanimity, 
    union,
    unity"""
query(theQuery8, dictionary)

theQuery9 = """war, battle, 
    bloodshed, 
    cold war, 
    combat, 
    conflict, 
    contention, 
    contest, 
    enmity, 
    fighting, 
    hostilities, 
    hostility, 
    police action, 
    strife, 
    strike, 
    struggle,
    warfare"""
query(theQuery9, dictionary)

theQuery10 = """prosperity, abundance, 
    accomplishment, 
    advantage, 
    arrival, 
    bed of roses, 
    benefit, 
    boom, 
    clover, 
    do, 
    ease, 
    easy street, 
    exorbitance, 
    expansion, 
    flying colors, 
    fortune, 
    good, 
    good times, 
    gravy train, 
    growth, 
    high on the hog, 
    increase, 
    inflation, 
    interest, 
    life of luxury, 
    luxury, 
    opulence, 
    plenteousness, 
    plenty, 
    prosperousness, 
    riches, 
    success, 
    successfulness, 
    the good life, 
    thriving, 
    velvet, 
    victory, 
    wealth, 
    welfare,
    well-being"""
query(theQuery10, dictionary)

theQuery11 = """justice, amends, 
    appeal, 
    authority, 
    authorization, 
    charter, 
    code, 
    compensation, 
    consideration, 
    constitutionality, 
    correction, 
    credo, 
    creed, 
    decree, 
    due process, 
    equity, 
    evenness, 
    fair play, 
    fair treatment, 
    hearing, 
    honesty, 
    impartiality, 
    integrity, 
    judicatory, 
    judicature, 
    justness, 
    law, 
    legal process, 
    legality, 
    legalization, 
    legitimacy, 
    litigation, 
    penalty, 
    reasonableness, 
    recompense, 
    rectitude, 
    redress, 
    reparation, 
    review, 
    right, 
    rule, 
    sanction, 
    sentence, 
    square deal,
    truth"""
query(theQuery11, dictionary)

theQuery12 = """immigration, colonization, 
    crossing, 
    defection, 
    departure, 
    displacement, 
    exile, 
    exodus, 
    expatriation, 
    homesteading, 
    journey, 
    leaving, 
    march, 
    migration, 
    movement, 
    moving, 
    peregrination, 
    reestablishment, 
    relocation, 
    removal, 
    resettlement, 
    settling, 
    shift, 
    transmigration, 
    transplanting, 
    travel, 
    trek, 
    uprooting, 
    voyage,
    wandering"""
query(theQuery12, dictionary)

theQuery13 = """racism, apartheid, 
    bias, 
    bigotry, 
    discrimination, 
    illiberality, 
    one-sidedness, 
    partiality, 
    racialism, 
    sectarianism, 
    segregation,
    unfairness"""
query(theQuery13, dictionary)