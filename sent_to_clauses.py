import nltk
import re
from pycorenlp import *

nlp=StanfordCoreNLP("http://localhost:9000/")

# get verb phrases
def get_verb_phrases(t):
    verb_phrases = []
    num_children = len(t)
    num_VP = sum(1 if t[i].label() == "VP" else 0 for i in range(0, num_children))

    if t.label() != "VP":
        for i in range(0, num_children):
            if t[i].height() > 2:
                verb_phrases.extend(get_verb_phrases(t[i]))

    elif t.label() == "VP" and num_VP > 1:
        for i in range(0, num_children):
            if t[i].label() == "VP":
                if t[i].height() > 2:
                    verb_phrases.extend(get_verb_phrases(t[i]))

    else:
        verb_phrases.append(' '.join(t.leaves()))

    return verb_phrases


# get position of first node "VP" while traversing from top to bottom
def get_tree_without_verb_phrases(t):
    node_pos = []
    num_children = len(t)
    children = [t[i].label() for i in range(0,num_children)]

    if "VP" in children:
        for i in range(0, num_children):
            if t[i].label() == "VP":
                node_pos.append(t[i].treeposition())

    else:
        for i in range(0, num_children):
            node_pos.extend(get_tree_without_verb_phrases(t[i]))

    return node_pos


# get all clauses
def get_clause_list(sent):
    parser = nlp.annotate(sent, properties={"annotators":"parse","outputFormat": "json"})
    t = nltk.tree.ParentedTree.fromstring(parser["sentences"][0]["parse"])
    clause_level_list = ["S","SBAR","SBARQ","SINV","SQ"]
    clause_list = []

    # get the leaves of and delete the subtree with label S or SBAR or SBARQ or SINV or SQ
    # do nothing if subtree with label S or SBAR or SBARQ or SINV or SQ is direct child of ROOT
    for sub in reversed(list(t.subtrees())):
        if sub.label() in clause_level_list and sub.parent().label() != "ROOT":
            if sub.parent().label() in clause_level_list:
                continue

            if (len(sub) == 1 and sub.label() == "S" and sub[0].label() == "VP"
                and not sub.parent().label() in clause_level_list):
                continue

            # for i in range(0,len(sub)):
            #     if sub[i].label() in clause_list:
            #         clause_list.append(' '.join(sub[i].leaves()))
            #         continue

            del t[sub.treeposition()]
            clause_list.append(' '.join(sub.leaves()))

    # get verb phrases from the new modified tree
    verb_phrases = get_verb_phrases(t)

    # get the tree without verb phrases (mainly subject)
    for i in get_tree_without_verb_phrases(t):
        del t[i]

    other_phrase = ' '.join(t.leaves())

    # update the clause_list
    for i in verb_phrases:
        clause_list.append(other_phrase + " " + i)

    return clause_list

if __name__ == "__main__":
    sent = "she is going to fail if you don't help her"
    sent = re.sub(r"(\.|,|\?|\(|\)|\[|\])"," ",sent)
    clause_list = get_clause_list(sent)
    print(clause_list)
    # while (True):
    #     sent = input("sentence : \n ")
    #     sent = re.sub(r"(\.|,|\?|\(|\)|\[|\])", " ", sent)
    #     print(sent)
    #     print(get_clause_list(sent))