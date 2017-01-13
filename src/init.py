#!/usr/bin/env python
# -*-coding:utf-8 -*

"""
``init.py`` **module description**:
This module has as three inputs among which just one is required.
first (Optionnaly): species tree, if not gave, the program will use the tree of species of Ensembl Compara release 87
second,  a directory containing only a set of files, for which each file corresponds to a gene tree in newick format
and the last parameter is the name of the output file which will contain the statistics (in .CSV format) of the datatset produce by the program.
Janvier 2017
Université de Sherbrooke Canada
Laboratoty CoBiUS
for running questions email us at Esaie.Kuitche.Kamela@USherbrooke.ca
"""

import os, sys
import argparse
from proteinToGeneTree import initProtein2GeneTree
from preparesTrees import initGetTrees, renameLeaf

def build_arg_parser(parent):
    parser = argparse.ArgumentParser(description="Protein2GeneTree program parameters")
    parser.add_argument('-s', '--specieTree',  default = parent + "/tree/speciesTree.nw")
    parser.add_argument('-g', '--genePathDirectory', default =  parent  + '/geneSample/')
    parser.add_argument('-o', '--outfile', default = parent  + '/statisticFile.csv')
    return parser

def main():
    path =  sys.path[0]
    parent =  "/".join(path.split("/")[:-1])  
    parser = build_arg_parser(str(parent))
    arg = parser.parse_args()
    speciesTreeFile = arg.specieTree
    outputfile = arg.outfile
    genePathDirectory = arg.genePathDirectory
    if not(os.path.isfile(speciesTreeFile)):
	print "Species tree don't exists, program stopping...."
	exit(1)
    if not os.path.exists(genePathDirectory):
	print "Directory for the gene trees don't exists, program stopping...."
	exit(1)

    dictSpeInv = initGetTrees(speciesTreeFile, genePathDirectory)
    initProtein2GeneTree(outputfile)
    renameLeaf(parent, dictSpeInv)
    print "Program end successful \nOpen ", outputfile, " to see results \nAnd browse the ",  parent + "/newGeneTree/ to have corrected tree" 
if __name__ == "__main__":
    main()
