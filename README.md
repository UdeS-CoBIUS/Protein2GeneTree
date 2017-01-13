# Protein2GeneTree
Protein2GeneTree By giving a proteins trees and species tree, this program give as result a genes tree which may be differed of proteins tree
####Reconstructing protein and gene phylogenies by extending the framework of reconciliation (https://arxiv.org/abs/1610.09732)
####Esaie Kuitche, Manuel Lafond and Aïda Ouangraoua
#####for running questions email us at Esaie.Kuitche.Kamela@USherbrooke.ca

##Requirements
This is composed of a set of Python scripts. It requires the following to be available
- python (2.7 and +) 
- argparse (https://pypi.python.org/pypi/argparse)
- ete3 (https://pypi.python.org/pypi/ete3/)
- networkx (https://pypi.python.org/pypi/networkx/)

##Usage
```
python init.py [-h] [-s specieTree] [-g genePathDirectory] [-o outfile]
```
-h, --help show this help message and exit
-s, --specieTree :  The species tree
-g, --genePathDirectory : path to the directory which contains genes tree files
-o, --outfile : outPut file

##Input files
###specieTree
```
(((Drosophila_melanogaster,Caenorhabditis_elegans),((Ciona_intestinalis,Ciona_savignyi),(((((((((Taeniopygia_guttata,Ficedula_albicollis),((Meleagris_gallopavo,Gallus_gallus),Anas_platyrhynchos)),Pelodiscus_sinensis),Anolis_carolinensis),((((((Procavia_capensis,Loxodonta_africana),Echinops_telfairi),(Choloepus_hoffmanni,Dasypus_novemcinctus)),((((Oryctolagus_cuniculus,Ochotona_princeps),(((((Mus_musculus_reference,mus_spretus_spreteij),rattus_norvegicus),Dipodomys_ordii),Ictidomys_tridecemlineatus),Cavia_porcellus)),(((Microcebus_murinus,Otolemur_garnettii),(((((Papio_anubis,Macaca_mulatta),Chlorocebus_sabaeus),((((Pan_troglodytes,Homo_sapiens),Gorilla_gorilla),Pongo_abelii),Nomascus_leucogenys)),Callithrix_jacchus),Carlito_syrichta)),Tupaia_belangeri)),((Sorex_araneus,Erinaceus_europaeus),(((Pteropus_vampyrus,Myotis_lucifugus),((((Mustela_putorius_furo,Ailuropoda_melanoleuca),Canis_lupus_familiaris),Felis_catus),Equus_caballus)),((((Bos_taurus,Ovis_aries),Tursiops_truncatus),Vicugna_pacos),Sus_scrofa))))),((Macropus_eugenii,Sarcophilus_harrisii),Monodelphis_domestica)),Ornithorhynchus_anatinus)),Xenopus_tropicalis),Latimeria_chalumnae),(((Danio_rerio,Astyanax_mexicanus),(((Tetraodon_nigroviridis,Takifugu_rubripes),((((Poecilia_formosa,Xiphophorus_maculatus),Oryzias_latipes),Gasterosteus_aculeatus),Oreochromis_niloticus)),Gadus_morhua)),Lepisosteus_oculatus)),Petromyzon_marinus))),Saccharomyces_cerevisiae);
```
##genePathDirectory
```
/home/user/Document/geneTrees/
```
##example of genes tree
```
(((((WBGene00004981__Caenorhabditis_elegans,WBGene00022427__Caenorhabditis_elegans),WBGene00006418__Caenorhabditis_elegans),(ENSCING00000005500__Ciona_intestinalis,ENSCSAVG00000006881__Ciona_savignyi)),((((((((((ENSPSIG00000014185__Pelodiscus_sinensis,ENSPSIG00000008770__Pelodiscus_sinensis),(((ENSGALG00000004553__Gallus_gallus,ENSMGAG00000005166__Meleagris_gallopavo),ENSAPLG00000003637__Anas_platyrhynchos),(ENSFALG00000005493__Ficedula_albicollis,ENSTGUG00000004333__Taeniopygia_guttata))),ENSACAG00000008740__Anolis_carolinensis),((((((ENSDNOG00000040289__Dasypus_novemcinctus,ENSCHOG00000005326__Choloepus_hoffmanni),((ENSLAFG00000008044__Loxodonta_africana,ENSPCAG00000007133__Procavia_capensis),ENSETEG00000019392__Echinops_telfairi)),((((((((ENSAMEG00000017782__Ailuropoda_melanoleuca,ENSMPUG00000004200__Mustela_putorius_furo),ENSCAFG00000014100__Canis_lupus_familiaris),ENSFCAG00000001234__Felis_catus),ENSECAG00000016826__Equus_caballus),((((ENSBTAG00000009984__Bos_taurus,ENSOARG00000006286__Ovis_aries),ENSTTRG00000007575__Tursiops_truncatus),ENSSSCG00000010274__Sus_scrofa),ENSVPAG00000004494__Vicugna_pacos)),ENSEEUG00000012108__Erinaceus_europaeus),(ENSPVAG00000001674__Pteropus_vampyrus,ENSMLUG00000016063__Myotis_lucifugus)),((((ENSOCUG00000017791__Oryctolagus_cuniculus,ENSOPRG00000012672__Ochotona_princeps),ENSTBEG00000004598__Tupaia_belangeri),(((ENSSTOG00000002353__Ictidomys_tridecemlineatus,ENSDORG00000015465__Dipodomys_ordii),((ENSMUSG00000020097__Mus_musculus_reference,MGP_SPRETEiJ_G0016172__Mus_spretus_SPRETEiJ),ENSRNOG00000000565__Rattus_norvegicus)),ENSCPOG00000012699__Cavia_porcellus)),((((((((ENSPTRG00000002598__Pan_troglodytes,ENSG00000166224__Homo_sapiens),ENSGGOG00000016655__Gorilla_gorilla),ENSPPYG00000002364__Pongo_abelii),ENSNLEG00000016177__Nomascus_leucogenys),((ENSPANG00000022284__Papio_anubis,ENSCSAG00000008393__Chlorocebus_sabaeus),ENSMMUG00000009800__Macaca_mulatta)),ENSCJAG00000014777__Callithrix_jacchus),ENSTSYG00000003267__Carlito_syrichta),(ENSMICG00000015141__Microcebus_murinus,ENSOGAG00000006188__Otolemur_garnettii))))),ENSSARG00000010713__Sorex_araneus),((ENSSHAG00000008602__Sarcophilus_harrisii,ENSMEUG00000001815__Macropus_eugenii),ENSMODG00000008784__Monodelphis_domestica)),ENSOANG00000011007__Ornithorhynchus_anatinus)),ENSXETG00000008190__Xenopus_tropicalis),ENSLACG00000012214__Latimeria_chalumnae),(((ENSDARG00000061375__Danio_rerio,ENSAMXG00000004674__Astyanax_mexicanus),(((((ENSPFOG00000008462__Poecilia_formosa,ENSXMAG00000007880__Xiphophorus_maculatus),ENSONIG00000010329__Oreochromis_niloticus),((ENSTRUG00000017861__Takifugu_rubripes,ENSTNIG00000013084__Tetraodon_nigroviridis),ENSGACG00000003253__Gasterosteus_aculeatus)),ENSORLG00000014050__Oryzias_latipes),ENSGMOG00000006288__Gadus_morhua)),ENSLOCG00000011521__Lepisosteus_oculatus)),ENSPMAG00000001747__Petromyzon_marinus),(ENSCSAVG00000011808__Ciona_savignyi,ENSCING00000001222__Ciona_intestinalis)),FBgn0010591__Drosophila_melanogaster)),YDR294C__Saccharomyces_cerevisiae);
```
##NOTICE
**gene name must start by genId followed by __ and end by his species name as mentionned in species tree**
##
outfile
```
statistic.csv
```
##Running Protein2GeneTree an example
```
- python init.py --genePathDirectory "/home/user/Document/gene/" --specieTree "/home/user/Document/tree/speciesTree.nw" --outfile "statictic.csv"
or simply 
- python init.py --genePathDirectory "/home/user/Document/gene/"
if you choose to use Ensembl species tree release 87 (https://github.com/Ensembl/ensembl-compara/blob/release/87/scripts/pipeline/species_tree.ensembl.topology.nw)
```
