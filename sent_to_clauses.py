import nltk
import re
from pycorenlp import *

nlp=StanfordCoreNLP("http://localhost:9000/")


def get_clause_list(sent):
    sent = "he worked hard but he still failed"
    parser = nlp.annotate(sent, properties={"annotators":"parse","outputFormat": "json"})
    t = nltk.tree.ParentedTree.fromstring(parser["sentences"][0]["parse"])
    t.pretty_print()
    #print(sent)

    clause_level_list = ["S","SBAR","SBARQ","SINV","SQ"]
    clause_list = []
    # flag = 0
    for sub in reversed(list(t.subtrees())):
        if sub.label() in clause_level_list:
            # if flag == 0:

            if sub.parent().label() in clause_level_list:
                continue
            del t[sub.treeposition()]
            clause_list.append(str(sub.flatten()))
            # else :
            #     flag = 0
            #     del t[sub.treeposition()]

    return clause_list


sent = ""
sent = re.sub('\W+', ' ', sent)
sent = sent.lower()
clause_list = get_clause_list(sent)
print(clause_list)



