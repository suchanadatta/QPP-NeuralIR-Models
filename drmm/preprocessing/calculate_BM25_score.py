#!/usr/bin/env python
import sys
from math import log, sqrt

ALPHA = 1
BETA = 0.75
GAMMA = 0.15

if len(sys.argv) < 3:
    print('Needs 2 arguments - see comments for info ...')
    exit(0)

arg_corpus_file = sys.argv[1]
arg_topics_file = sys.argv[2]


def read_file(file):
    fp = open(file)
    output = dict()
    for line in fp.readlines():
        # id, text = line.strip().split('\t')
        parts = line.split(' ', 1)
        id = parts[0]
        text = parts[1]
        output[id] = text
        # print(output)
    return output


def example_list2dict(input):
    output = dict()
    for word in input.split():
        if output.get(word) is None:
            output[word] = 0
        output[word] += 1
    return output


def cal_idf(doc_dict):
    doc_num = len(doc_dict)
    idf = dict()
    for doc_id in doc_dict:
        doc_text = list(set(doc_dict[doc_id].split()))
        for word in doc_text:
            if idf.get(word) is None:
                idf[word] = 0
            idf[word] += 1
    for word in idf:
        idf[word] = log((doc_num - idf[word] + 0.5) / (idf[word] + 0.5))
    return idf


def bm25(query, doc, idf, avg_doc_len=374):
    k1 = 1.2
    k2 = 1
    b = 0.75
    score = 0.0
    for word in query:
        if doc.get(word) is None:
            continue
        W_i = idf[word]
        f_i = doc[word]
        qf_i = query[word]
        doc_len = sum(doc.values())
        K = k1 * (1 - b + b * doc_len / avg_doc_len)
        R1 = f_i * (k1 + 1) / (f_i + K)
        R2 = qf_i * (k2 + 1) / (qf_i + k2)
        R = R1 * R2
        score += W_i * R
    return score


def GetScore(query, doc_name, doc_dict, idf):
    query = example_list2dict(query)
    doc = example_list2dict(doc_dict[doc_name])
    score = bm25(query, doc, idf)
    return score


def generateInvertedIndex():
    invertedIndex = {}
    tokenDict = {}
    doc_dict = open('./data/doc.txt')
    for line in doc_dict.readlines():
        doc_id, text = line.strip().split('\t')
        doc_text = text.split()
        length = len(doc_text)
        tokenDict[doc_id] = length
        for word in text.split():
            if word not in invertedIndex.keys():
                docIDCount = {doc_id : 1}
                invertedIndex[word] = docIDCount
            elif doc_id in invertedIndex[word].keys():
                invertedIndex[word][doc_id] += 1
            else:
                docIDCount = {doc_id : 1}
                invertedIndex[word].update(docIDCount)
    return invertedIndex


def queryFrequency(query, invertedIndex):
    queryFreq = {}
    for term in query.split():
        if term in queryFreq.keys():
            queryFreq[term] += 1
        else:
            queryFreq[term] = 1
    for term in invertedIndex:
        if term not in queryFreq.keys():
            queryFreq[term] = 0
    #print(queryFreq)
    return queryFreq


def calculateDocsCount(doc, docIndex):
    doc_dict = open('./data/doc.txt')
    for line in doc_dict.readlines():
        doc_id, text = line.strip().split('\t')
        if doc_id == doc:
            for term in text.split():
                if term in docIndex.keys():
                    docIndex[term] += 1
                else:
                    docIndex[term] = 1
    return docIndex


def findDocs(k, sortedBM25Score, invertedIndex, relevancy):
    relIndex = {}
    nonRelIndex = {}
    if relevancy == "Relevant":
        for i in range(0, k):
            doc,doc_score = sortedBM25Score[i]
            relIndex = calculateDocsCount(doc, relIndex)
        for term in invertedIndex:
            if term not in relIndex.keys():
                relIndex[term] = 0
        return relIndex
    elif relevancy == "Non-Relevant":
        for i in range(k+1,len(sortedBM25Score)):
            doc,doc_score = sortedBM25Score[i]
            nonRelIndex = calculateDocsCount(doc, nonRelIndex)
        for term in invertedIndex:
            if term not in nonRelIndex.keys():
                nonRelIndex[term] = 0
        return nonRelIndex

def findRelDocMagnitude(docIndex):
    mag = 0
    for term in docIndex:
        mag += float(docIndex[term]**2)
        mag = float(sqrt(mag))
    return mag

def findNonRelDocMagnitude(docIndex):
    mag = 0
    for term in docIndex:
        mag += float(docIndex[term]**2)
    mag = float(sqrt(mag))
    return mag


def findRocchioScore(term, queryFreq, relDocMag, relIndex, nonRelMag, nonRelIndex):
    Q1 = ALPHA * queryFreq[term]
    Q2 = (BETA/relDocMag) * relIndex[term]
    Q3 = (GAMMA/nonRelMag) * nonRelIndex[term]
    rocchioScore = ALPHA * queryFreq[term] + (BETA/relDocMag) * relIndex[term] - (GAMMA/nonRelMag) * nonRelIndex[term]
    return rocchioScore


def findNewQuery(query, k, sortedBM25Score, invertedIndex):
    queryFreq = queryFrequency(query, invertedIndex)
    relIndex = findDocs(k, sortedBM25Score, invertedIndex, "Relevant")
    relDocMag = findRelDocMagnitude(relIndex)
    nonRelIndex = findDocs(k, sortedBM25Score, invertedIndex, "Non-Relevant")
    nonRelMag = findNonRelDocMagnitude(nonRelIndex)
    updatedQuery = {}
    newQuery = query
    for term in invertedIndex:
        updatedQuery[term] = findRocchioScore(term, queryFreq, relDocMag, relIndex, nonRelMag, nonRelIndex)
    sortedUpdatedQuery = sorted(updatedQuery.items(), key=lambda x:x[1], reverse=True)
    if len(sortedUpdatedQuery)<5:
        loopRange = len(sortedUpdatedQuery)
    else:
        loopRange = 5
    for i in range(loopRange):
        term,frequency = sortedUpdatedQuery[i]
        #print("term, frequency", term, frequency)
        if term not in query:
            newQuery +=  " "
            newQuery +=  term
    return newQuery
#invertedIndex = generateInvertedIndex()
#print(invertedIndex)


def pseudoRelevanceFeedbackScores(sortedBM25Score, query,queryID):
    global feedbackFlag
    feedbackFlag += 1
    k = 10
    #reducedIndex = getReduceIndex(query, invertedIndex)
    #print(reducedIndex)
    newQuery = findNewQuery(query, k, sortedBM25Score, invertedIndex)
    print(query)
    print(newQuery)
    PseudoRelevanceScoreList = RankDoc(newQuery,queryID)
    return PseudoRelevanceScoreList


def RankDoc(query,queryID):
    BM25ScoreList = {}
    global feedbackFlag
    for ID in range(300):
        docID = str(queryID)+'_'+str(ID)
        #print("docID",docID)
        BM25 = GetScore(query, docID, doc_dict, idf)
        BM25ScoreList[docID] = BM25
    sortedBM25Score = sorted(BM25ScoreList.items(), key=lambda x:x[1], reverse=True)
    #return sortedBM25Score
    if feedbackFlag == 1:
        return pseudoRelevanceFeedbackScores(sortedBM25Score, query,queryID)
    elif feedbackFlag == 2:
        feedbackFlag = 1
        return sortedBM25Score


query_dict = read_file(arg_topics_file)
doc_dict = read_file(arg_corpus_file)
idf = cal_idf(doc_dict=doc_dict)
# invertedIndex = generateInvertedIndex()



