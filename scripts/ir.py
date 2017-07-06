# Name: Chuntao Fu          Date: 06/8/2017
# parse a document with format class1;class2;label="method" into multiple documents
# having the format: class2, method

import fileinput
import regex as re
from pprint import pprint
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities
import gensim
import sys
import os


fileName = sys.argv[1]
analysis_type = sys.argv[2]
topic_number = int(sys.argv[3])
print(topic_number)
topic_words = 3
lsi_query = ""
if analysis_type == "LDA":
    topic_words = int(sys.argv[4])
else:
    lsi_query = sys.argv[4]

documents = {}
process_documents = {}
id_document_map = {}
texts = []
en_stop = get_stop_words("en")
p_stemmer = PorterStemmer()

def splitWord(str):
    str = re.sub("[^A-Za-z]", "", str)
    words = re.split(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|(?<=[a-z]A)(?=[A-Z])', str, flags=re.V1)
    return words


for line in fileinput.input(fileName):
    tokens = line.rstrip('\n').split(';')
    if "dashed" not in tokens[2]:
        methodTokens = tokens[2].rstrip('"').split(':')
        if tokens[1] in documents:
            if methodTokens[1] not in documents[tokens[1]]:
                documents[tokens[1]].append(methodTokens[1])
        else:
            documents[tokens[1]] = [methodTokens[1]]


# append the key(the Class Name) to each class document
for key, value in documents.items():
    if key.lower() not in documents[key]:
        documents[key].append(key)

# split each work in the class document
for key, value in documents.items():
    for word in value:
        words = splitWord(word)
        for w in words:
            if key in process_documents:
                process_documents[key].append(w.lower())
            else:
                process_documents[key] = [w.lower()]

#pprint(documents)
#pprint(process_documents)

stoplist = set("get set a an is enabled".split())
for key, value in process_documents.items():
    stopped_tokens = [w for w in value if not w in stoplist]
    texts.append(stopped_tokens)


#Creating the term dictionary out of corpus, where every unique term is assigned an index
dictionary = corpora.Dictionary(texts)
#print(dictionary.token2id)

#Generating document term matrix
corpus = [dictionary.doc2bow(text) for text in texts]
#print(corpus)

#Create a lda transformation model
if analysis_type == "LDA":
    lda = models.LdaModel(corpus, num_topics=topic_number, id2word=dictionary)
    topics = lda.print_topics(num_topics=topic_number, num_words=topic_words)
    for topic in topics:
        print(str(topic[0]) + ":" + topic[1])
    #print(corpus[0])
    #print(lda.get_document_topics(corpus[11]))
else:
    # produce class-based doucments
    dir_path = "documents/"
    if not os.path.isdir("./" + dir_path):
        os.makedirs("documents/")

    count = 0
    for key, value in documents.items():
        id_document_map[count] = key
        with open("./documents/{}_{}.txt".format(count, key), "w") as f:
            for v in value:
                f.write(v + "\n")
            count = count + 1

    #Creat a lsi trnasformation model
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=topic_number)
    query = lsi_query
    query_bow = dictionary.doc2bow(query.lower().split())
    query_lsi = lsi[query_bow]
    index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[query_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    for sim in sims:
        if sim[0] in id_document_map:
            print(id_document_map[sim[0]] + ":" + str(sim[0]) + ":" + str(sim[1]))
