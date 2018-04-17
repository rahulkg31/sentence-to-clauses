import nltk
import re
from pycorenlp import *

nlp=StanfordCoreNLP("http://localhost:9000/")

# get verb phrases
# if one "VP" node has 2 or more "VP" children then
# all child "VP" while be used as verb phrases
# since a clause may have more than one verb phrases
# ex:- he plays cricket but does not play hockey
# here two verb phrases are "plays cricket" and "does not play hockey"
#                       ROOT
#                        |
#                        S
#   _____________________|____
#  |                          VP
#  |          ________________|____
#  |         |           |         VP
#  |         |           |     ____|________
#  |         VP          |    |    |        VP
#  |     ____|_____      |    |    |    ____|____
#  NP   |          NP    |    |    |   |         NP
#  |    |          |     |    |    |   |         |
# PRP  VBZ         NN    CC  VBZ   RB  VB        NN
#  |    |          |     |    |    |   |         |
#  he plays     cricket but  does not play     hockey
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
# get the position of subordinating conjunctions like after, as, before, if, since, while etc
# delete the node at these positions to get the subject
# first delete vp nodes then subordinating conjunction nodes
# ie, get the part without verb phrases
# in the above example "he" will be returned
def get_pos(t):
    vp_pos = []
    sub_conj_pos = []
    num_children = len(t)
    children = [t[i].label() for i in range(0,num_children)]

    flag = re.search(r"(S|SBAR|SBARQ|SINV|SQ)", ' '.join(children))

    if "VP" in children and not flag:
        for i in range(0, num_children):
            if t[i].label() == "VP":
                vp_pos.append(t[i].treeposition())
    elif not "VP" in children and not flag:
        for i in range(0, num_children):
            if t[i].height() > 2:
                temp1,temp2 = get_pos(t[i])
                vp_pos.extend(temp1)
                sub_conj_pos.extend(temp2)
    # comment this "else" part, if want to include subordinating conjunctions
    else:
        for i in range(0, num_children):
            if t[i].label() in ["S","SBAR","SBARQ","SINV","SQ"]:
                temp1, temp2 = get_pos(t[i])
                vp_pos.extend(temp1)
                sub_conj_pos.extend(temp2)
            else:
                sub_conj_pos.append(t[i].treeposition())

    return (vp_pos,sub_conj_pos)


# get all clauses
def get_clause_list(sent):
    parser = nlp.annotate(sent, properties={"annotators":"parse","outputFormat": "json"})
    sent_tree = nltk.tree.ParentedTree.fromstring(parser["sentences"][0]["parse"])
    clause_level_list = ["S","SBAR","SBARQ","SINV","SQ"]
    clause_list = []
    sub_trees = []
    # sent_tree.pretty_print()

    # break the tree into subtrees of clauses using
    # clause levels "S","SBAR","SBARQ","SINV","SQ"
    for sub_tree in reversed(list(sent_tree.subtrees())):
        if sub_tree.label() in clause_level_list:
            if sub_tree.parent().label() in clause_level_list:
                continue

            if (len(sub_tree) == 1 and sub_tree.label() == "S" and sub_tree[0].label() == "VP"
                and not sub_tree.parent().label() in clause_level_list):
                continue

            sub_trees.append(sub_tree)
            del sent_tree[sub_tree.treeposition()]

    # for each clause level subtree, extract relevant simple sentence
    for t in sub_trees:
        # get verb phrases from the new modified tree
        verb_phrases = get_verb_phrases(t)

        # get tree without verb phrases (mainly subject)
        # remove subordinating conjunctions
        vp_pos,sub_conj_pos = get_pos(t)
        for i in vp_pos:
            del t[i]
        for i in sub_conj_pos:
            del t[i]

        subject_phrase = ' '.join(t.leaves())

        # update the clause_list
        for i in verb_phrases:
            clause_list.append(subject_phrase + " " + i)

    return clause_list

if __name__ == "__main__":
    # sent = "he plays cricket but does not play hockey"
    # sent = re.sub(r"(\.|,|\?|\(|\)|\[|\])"," ",sent)
    # clause_list = get_clause_list(sent)
    # print(clause_list)
    while (True):
        sent = input("sentence : \n ")
        sent = re.sub(r"(\.|,|\?|\(|\)|\[|\])", " ", sent)
        print(get_clause_list(sent))