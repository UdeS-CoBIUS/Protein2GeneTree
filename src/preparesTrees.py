#!/usr/bin/env python
# -*-coding:utf-8 -*
"""
``init.py`` **module description**:
This module has as input a tree of species in the format newick (if it is provided as parameter, otherwise the program will use the tree of species of Ensembl Compara release 87), a directory containing a set of files Each file of which corresponds to a gene tree and the name of the output file which will contain the statistics of the use of the program.
It allows to format the data under structures easily manipulated by the rest of the program.
.. moduleauthor:: Esaie KUITCHE, Manuel Lafong and Aida Ouangraoua
Janvier 2017
Université de Sherbrooke Canada
Laboratoty CoBiUS
"""

from ete3 import Tree
from ete3 import PhyloTree
from copy import deepcopy
import pickle
import logging
import string
import glob
from os.path import basename
import os, sys


def readTreeFromFile(path):
    file = open(path, "r")
    datas = file.readlines()[0]
    return str(datas)

def lowerCase(tree):
    for node in tree.traverse("postorder"):
        if node.is_leaf():
	    oldName = node.name
            var = node.name.split("__")
            if len(var) == 1:
                node.name = node.name.lower().replace("_", "")
            else:
                node.name = var[0].lower().replace("_", "") + "__" + var[1].lower().replace("_", "")

def getTrees(file, sptree, dictSpe, ParentPath, logging):
    genesTree = readTreeFromFile(file)
    genetree = Tree(genesTree)
    lowerCase(genetree)

    for node in genetree.traverse("preorder"):
        if node.is_leaf():
            var = node.name.split("__")
            if (var[1] in dictSpe.keys()):
                node.name = dictSpe[var[1]] + "_" + var[0]
            else:
		logging.debug("There are genes that refer to species absent in the species tree : " +  node.name)
		print "There are genes that refer to species absent in the species tree"
		exit(1)

    genetree.write(format=2, outfile= ParentPath + "/geneFile/"+ basename(file).split(".")[0] + ".nw")


def initGetTrees(specieTree, genePath):
    path =  sys.path[0]
    ParentPath =  "/".join(path.split("/")[:-1])  
    LOG_FILENAME = ParentPath + '/logFile.log'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

    speciesTree = readTreeFromFile(specieTree)
    sptree = Tree(speciesTree)
    lowerCase(sptree)
    dictSpe = {}
    dictSpeInv = {}
    compt = 10
    for node in sptree.traverse("preorder"):
        if node.is_leaf():
            var = "A" + str(compt)
            compt = compt + 1
            dictSpe[node.name] = var
	    dictSpeInv[var] = node.name
            node.name = var
    sptree.write(format=9, outfile=ParentPath +"/tree/speciesTreeOK.nw")

    files =  glob.glob(genePath +"*")

    for file in files:
	logging.info(file)
        getTrees(file, sptree, dictSpe, ParentPath, logging)
    return dictSpeInv

def renameLeaf(ParentPath, dictSpeInv):
    files =  glob.glob(ParentPath + "/geneFile/*")
    for file in files:
        genesTree = readTreeFromFile(file)
        genetree = Tree(genesTree)

        for node in genetree.traverse("preorder"):
	    if node.is_leaf():
    	        var = node.name.split("_")
	        if (var[0] in dictSpeInv.keys()):
	            node.name = var[1] + "__" + dictSpeInv[var[0]]
	        else:
                    print dictSpeInv, dictOriginName, node.name 
		    logging.debug("There are genes that refer to species absent in the species tree 2: " +  node.name)
		    print "There are genes that refer to species absent in the species tree 2"
		    exit(1)
	os.remove(file)
        genetree.write(format=2, outfile= ParentPath + "/newGeneTree/"+ basename(file).split(".")[0] + ".nw")
