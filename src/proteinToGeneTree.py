#!/usr/bin/env python
# -*-coding:utf-8 -*
from ete3 import Tree
from ete3 import PhyloTree
from copy import deepcopy
import pickle
from sets import Set
import networkx as nx
import string
import sys
import time
import Queue
import os
import threading
import glob
from os.path import basename
import logging


def newScore(trees, sptree, proteinTrees, dicGene):
    proteinTree = deepcopy(proteinTrees)
    tree = deepcopy(trees)
    for node in tree.traverse("preorder"):
        if(node.is_leaf() and node.name=="L"):
            node.detach()
        elif(onlyLoss(node.get_leaf_names())):
            ancestorss = node.get_ancestors()
            if(len(ancestorss) > 1):
                father = ancestorss[0]
                grandFather = ancestorss[1]
                sisters1 = node.get_sisters()
                for s in sisters1:
                    grandFather.add_child(s)
                father.detach()
        else:
            children = node.children
            if(len(children) == 1):
                smallChild = children[0].children
                for s in smallChild:
                    node.add_child(s)
                node.children[0].detach()

    recon_tree, events = tree.reconcile(sptree)
    labelLost(recon_tree)
    unlabel(recon_tree)

    nbDup = numberOfDuplicationGtoS(recon_tree)
    nbLost = numberOfLostGtoS(recon_tree)

    for node in tree.traverse("postorder"):
        if node.is_leaf():
            node.name = dicGene[node.name]


    for node in proteinTree.traverse("postorder"):
        if node.is_leaf():
            var = node.name.split("_")
            node.name = dicGene[node.name] + "_" + var[1]

    testTree(proteinTree)
    testTree(tree)

    recon_tree2, events2 = proteinTree.reconcile(tree)
    labelLost(recon_tree2)
    unlabel(recon_tree2)

    nbCreat = numberOfDuplicationGtoS(recon_tree2)
    nbLost2 = numberOfLostGtoS(recon_tree2)

    return nbDup + nbLost + nbCreat + nbLost2, tree, [nbCreat, nbLost2, nbDup, nbLost]

def readTreeFromFile(path):
    file = open(path, "r")
    datas = file.readlines()[0]
    return str(datas)

def numberOfDuplicationGtoS(tree):
    ntrees, ndups, sptrees = tree.get_speciation_trees()
    return ndups

def numberOfLostGtoS(tree):
    compt = 0;
    for node in tree.traverse("preorder"):
        if(node.name == "L"):
            compt += 1
    return compt

def unlabel(tree):
    """
    permet d'étiquetter les noeuds descendents d'un noeud perdu.
    :param tree:
    :return:
    """
    for node in tree.traverse("preorder"):
        if not(node.is_leaf()):
            if(node.name == "L"):
                if(((node.children[0].name == "L") or (node.children[0].name == "HL")) and onlyLoss(node.children[0].get_leaf_names())):
                    node.children[0].name = "HL"
                if(((node.children[1].name == "L") or (node.children[1].name == "HL")) and onlyLoss(node.children[1].get_leaf_names())):
                    node.children[1].name = "HL"

def labelLost(recon_tree):
    """
    Permet de marquer "L" (lost) à l'attribut name de chaque noeud qui correspond à un noeud perdu apres la reconciliation
    :param recon_tree:
    :return:
    """
    for node in recon_tree.traverse("postorder"):
        if not(node.is_leaf()):
            leaves = node.get_leaf_names()
            if(is_theeLost(leaves)):
                childreen = node.get_children()
                childL = childreen[0]
                childR = childreen[1]
                if(not(childL.is_leaf()) and (not(childR.is_leaf()))):
                    if((childL.name == "L" and onlyLoss(childL.get_leaf_names())) or (childR.name == "L" and onlyLoss(childL.get_leaf_names()))):
                        node.name = "L"
                elif((childL.is_leaf() and is_theeLost(childL.get_leaf_names())) or ((childR.is_leaf() and is_theeLost(childR.get_leaf_names())))):
                        node.name = "L"
            else:
                pass

def is_overlap(list1, list2):
    l1 = []
    l2 = []
    for elt in list1:
        l1.append(elt.split("_")[0])
    for elt in list2:
        l2.append(elt.split("_")[0])

    return (len([val for val in l1 if val in l2]) > 0)


def is_theeLost(list):
    for elt in list:
        if(elt.count('_') == 0):
            return True
    return False

def onlyLoss(list):
    flag = True
    for elt in list:
        if(elt.count('_') != 0):
            flag = False
    return flag

def labelTree(tree):
    i = 1
    for node in tree.traverse("preorder"):
        if not(node.is_leaf()) :
            node.name = i
            i +=1
    return tree

def printTree(lTrees):
    for t in lTrees:
        t.show()

def addTree(dicTree, tree, score, nodes, lost, toMove, cost, newCost):
    global index
    dicTree[index] = [tree, nodes, lost, toMove, cost, newCost]
    index =  index + 1

def makeGraph(dicTree):
    keys = dicTree.keys()
    G = nx.Graph()
    G.add_nodes_from(keys)
    liste = []
    for i in keys:
        for j in keys[i+1:]:
            if  len([val for val in dicTree[i][1] if val in dicTree[j][1]]) == 0 :
                G.add_edge(i,j)

    cliques = [clique for clique in nx.find_cliques(G)]
    max = 0

    solutions =  dict()
    for clique in cliques:
        tmp = 0
        listeSol = []
        for i in clique:
            tmp = tmp + dicTree[i][4]
            listeSol.append(dicTree[i])
        if tmp > max:
            if max != 0:
                solutions.pop(max)
            solutions[tmp] = [listeSol]
            max = tmp
        elif tmp!= 0 and tmp == max:
            solutions[max].append(listeSol)
    return  solutions

def newGeneTree(geneTrees, dicListeClique):
    listeClique = dicListeClique[dicListeClique.keys()[0]]
    cost = [0,0,0,0]
    for cliques in listeClique:
        geneTree = deepcopy(geneTrees)
        for clique in cliques:
            cost = [cost[0] + clique[5][0], cost[1] + clique[5][1], cost[2] + clique[5][2], cost[3] + clique[5][3]]
            if len(clique[3]) > 1:
                toMove = geneTree.get_common_ancestor(list(clique[3]))
            else:
                toMove = geneTree.search_nodes(name=clique[3][0])[0]
            if len(clique[2]) > 1:
                toDelete = geneTree.get_common_ancestor(list(clique[2]))
            elif len(clique[2]) == 1:
                toDelete = geneTree.search_nodes(name=clique[2][0])[0]
            else:
                return cost

            parent = toDelete.add_child(deepcopy(toDelete))
            parent = toDelete.add_child(deepcopy(toMove))

            toMove.detach()

        return cost

def testTree(tree):
    for node in tree.traverse("preorder"):
        if len(node.children) == 2:
            pass
        elif len(node.children)==0:
            pass
        else:
            exit(os.EX_DATAERR)

def process(enode, recon_tree, genetree, sptree, dicTree, dicGene, listeSubTree):
    nodes = []
    for l in enode:
        for e in l:
            nodes.append(e)
    nodes = Set(nodes)
    node = recon_tree.get_common_ancestor(enode[0] + enode[1])  # noeud de dup
    genetree22 = genetree.get_common_ancestor(enode[0] + enode[1])  # noeud de dup


    node2 = genetree.get_common_ancestor(enode[0] + enode[1])
    nbDup = numberOfDuplicationGtoS(node)
    nbLost = numberOfLostGtoS(node)
    scoreInit = nbDup + nbLost
    bestScore = scoreInit

    children = node.children
    childL = node.children[0]
    childR = node.children[1]
    if (childL.name == "L" and childR.name != "L"):
        toMove = childL.get_leaf_names()
        leaves = childL.get_leaf_names()
        lostNode = childR.search_nodes(name="L")
        for lost in lostNode:
            if lost.name == "L":
                listLost = lost.get_leaf_names()
                fils = lost.children
                if (onlyLoss(fils[0].get_leaf_names())):
                    child = fils[0]
                else:
                    child = fils[1]
                if ((child.name == "HL" and (onlyLoss(child.get_leaf_names()))) or (child.name == "L") or (
                onlyLoss(child.get_leaf_names()))):
                    child.detach()
                    newNode = deepcopy(childL)
                    lost.add_child(newNode)
                    childL.detach()
                    score, tree, newCost = newScore(deepcopy(node), sptree, genetree22, dicGene)
                    if (score < bestScore):
                        bestScore = score
                        listeSubTree = [dicTree, tree, score, nodes, [x for x in listLost if len(x.split("_")) > 1], [x for x in toMove if len(x.split("_")) > 1], scoreInit - score, newCost]

                    lost.add_child(child)
                    newNode.detach()
                    node.add_child(childL)
    elif ((childR.name == "L" and childL.name != "L")):
        toMove = childR.get_leaf_names()
        leaves = childL.get_leaf_names()
        lostNode = childL.search_nodes(name="L")
        for lost in lostNode:
            if lost.name == "L":
                listLost = lost.get_leaf_names()
                fils = lost.children
                if (onlyLoss(fils[0].get_leaf_names())):
                    child = fils[0]
                else:
                    child = fils[1]
                if ((child.name == "HL" and (onlyLoss(child.get_leaf_names()))) or (child.name == "L") or (
                onlyLoss(child.get_leaf_names()))):
                    child.detach()
                    newNode = deepcopy(childR)
                    lost.add_child(newNode)
                    childR.detach()
                    score, tree, newCost = newScore(deepcopy(node), sptree, genetree22, dicGene)
                    if (score < bestScore):
                        bestScore = score
                        listeSubTree = [dicTree, tree, score, nodes, [x for x in listLost if len(x.split("_")) > 1], [x for x in toMove if len(x.split("_")) > 1], scoreInit - score, newCost]

                    lost.add_child(child)
                    newNode.detach()
                    node.add_child(childR)
    if (listeSubTree != []):
        addTree(listeSubTree[0], listeSubTree[1], listeSubTree[2], listeSubTree[3], listeSubTree[4], listeSubTree[5],
                listeSubTree[6], listeSubTree[7])
        listeSubTree = []


def main(file, sptree, f, q, logging, ParentPath):
    threads = []
    q = Queue.Queue()
    start_time = time.time()
    dicTree = dict()
    global index
    index = 0

    gene_tree_nw = readTreeFromFile(file)


    protein_tree_nw = gene_tree_nw #because we supposed that geneTree == proteinTree

    genetree = PhyloTree(gene_tree_nw)

    testTree(genetree)

    dicGene = {}
    indices = list(string.uppercase) + list(string.lowercase)

    cmpt = 0
    j = indices[cmpt]
    i = 10
    for node in genetree.traverse("preorder"):
        if node.is_leaf():
            var = j + str(i)
            dicGene[node.name] = var
            if i == 99:
                i = 10
                cmpt = cmpt + 1
                j = indices[cmpt]
            else:
                i = i + 1

    species = []
    geneListName = genetree.get_leaf_names()

    for s in geneListName:
	if len(s.split("_")) > 1:
	    species.append(s.split("_")[0])
	else:
	    logging.debug("There is at least on gene Badly written : " + s)
	    exit(os.EX_DATAERR)
    species = Set(species)
    if (species - Set(sptree.get_leaf_names()) == Set([])) == False:
	logging.debug("there is at least one specie which dont exist in species tree")
        exit(os.EX_DATAERR)

    recon_trees, events = genetree.reconcile(sptree) 

    labelLost(recon_trees)
    unlabel(recon_trees)

    nbDup = numberOfDuplicationGtoS(recon_trees)
    nbLost = numberOfLostGtoS(recon_trees)
    scoreInit = nbDup + nbLost
    bestScore = scoreInit

    listeSubTree = []

    nodelist = []
    for e in events:
        if e.etype == "D":
            nodelist.append([e.in_seqs, e.out_seqs])

    for enode in nodelist:
        recon_tree = deepcopy(recon_trees)


        t = threading.Thread(target=process, args=(enode, recon_tree, genetree, sptree, dicTree, dicGene, listeSubTree))

        threads.append(t)

        t.daemon = True

        t.start()

    for t in threads:
        t.join()
    while q.qsize() > 0:
        item = q.get()
        if item is None:
            break
        else:
            break

    solutions = makeGraph(dicTree)
    if solutions != {} :
        newCost = newGeneTree(genetree, solutions)
        genetree.write(format=9, outfile= ParentPath + "/newGeneTree/" + basename(file))
        f.write(basename(file).split(".")[0] + "\t" + str(len(geneListName)) +  "\t" + str(scoreInit) +  "\t" + str(solutions.keys()[0]) + "\t" + str(scoreInit - solutions.keys()[0]) +  "\t" + str(((solutions.keys()[0])*100.0)/scoreInit) +  "\t" + str(nbDup) + "\t" + str(nbLost) +  "\t" + str(time.time() - start_time)+ "\t" +  str(newCost[0]) + "\t"  +  str(newCost[1]) + "\t"+  str(newCost[2]) + "\t"+  str(newCost[3]) + "\n")
    else:
        f.write(basename(file).split(".")[0] + "\t" + str(len(geneListName)) +  "\t" +  str(scoreInit) +  "\t" + "--" +  "\t" + "0" +  "\t" + "0" +  "\t" + str(nbDup) + "\t" + str(nbLost) +  "\t" + str(time.time() - start_time)+ "\t" + '\t'.join(['0','0','0','0']) +"\n")
    q.put([f])


def initProtein2GeneTree(outputfile):
    path =  sys.path[0]
    ParentPath =  "/".join(path.split("/")[:-1]) 
    LOG_FILENAME = ParentPath + '/logFile.log'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
    threads = []
    q = Queue.Queue()

    species_tree_nw = readTreeFromFile(ParentPath + "/tree/speciesTreeOK.nw")
    sptree = PhyloTree(species_tree_nw)
    files =  glob.glob(ParentPath + "/geneFile/*")
    f = open(outputfile, 'w')
    f.write("GeneId \t Nb of leaf \t Cost of G--> S \t Réduction \t Cost P->G'->S \t % of reduction \t Nb of Dup \t Nb of Lost \t running time \t Nb of creation P->G \t Nb of Lost P -> G' \t Nb dup G'->S \t Nb Lost G'->S \n")
    f.close()
    for file in files:
        logging.info(file)
        f = open(outputfile, 'a')
        main(file, sptree, f, q, logging, ParentPath)
        f.close()

