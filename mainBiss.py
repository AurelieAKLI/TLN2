import os

import requests
import networkx as nx
import matplotlib.pyplot as plt
import pylab
import pickle

import re
from bs4 import BeautifulSoup

#pathTermesComposes = '/home/depinfo/Documents/M2_IASD/TLN2/data/termesComposes.json'
pathTermesComposes = '/home/aurelie/Bureau/projetTLN/termesComposes.json'
#chemin = "/home/depinfo/Documents/M2_IASD/TLN2/nouvelEssai/M2-TALN-Analyseur-Semantique-main"
chemin = "home/aurelie/Bureau/projetTLN"
chemin = chemin + '/cache/'



def getNomPredicat(numPred):
    liste2 = []
    with open("numRelation.txt", "r") as f:
        data = f.read()
        data = data.split("\n")  # liste de lignes
        for line in data:
            liste2.append(line.split(";"))

        try :
            for idR, nomRelation in liste2:
                if (numPred == idR):
                    return nomRelation
        except(ValueError):
            print("")
        return ""

def getNumPredicat(namePred: str):
    liste2 = []
    with open("numRelation.txt", "r") as f:
        data = f.read()
        data = data.split("\n")  # liste de lignes
        for line in data:
            liste2.append(line.split(";"))

        for idR, nomRelation in liste2:
            if (namePred == nomRelation):
                print("idRelation getNum " + idR)
                return idR



def rechercher2(premierPos, deuxiemePos, posAAjouter, g):
    graphe=g
    liste_noeuds=list(g.nodes(data=True))
    for n,p in liste_noeuds:
            if (premierPos in p.keys() and p[premierPos]>50):
                #print("l74", n ,"\t", premierPos, "\t",p[premierPos])
                for v in g.neighbors(n):
                    if (deuxiemePos in g.nodes[v] and g.nodes[v][deuxiemePos]>50 and v!="_pas"):

                        print(n,"\t",p,"-->",v,"\t",g.nodes[v])
                        liste_arretes=list(g.edges)
                        liste_arretes_bis=list(g.edges)

                        for (e1, e2) in liste_arretes:
                            if (e2==n):
                                for (e1_bis, e2_bis) in liste_arretes_bis:
                                    if (e1_bis==v):
                                        #nouveau_noeu="_"+posAAjouter+" identifié : "+n+" "+v.replace("_","")
                                        nouveau_noeu=n+" "+v.replace("_","")
                                        print("arretes à ajouter : (",e1,"-",nouveau_noeu,")\t(",nouveau_noeu,"-",e2_bis,")")
                                        if (premierPos=='Ver' and deuxiemePos=='Ver'):
                                            if (n=="_suis" or n=="_es" or n=="_est" or n=="_sommes" or n=="_êtes" or n=="_sont" or n=="_étais" or n=="_était" or n=="_étions" or n=="_étiez" or n=="_étaient" or n=="_ai" or n=="_as" or n=="_a" or n=="_ont" or n=="_avons" or n=="_avez" or n=="_avais"or n=="_avions" or n=="_aviez" or n=="_avaient"): #A VÉRIFIER
                                                nouveau_noeu=n+" "+v.replace("_","")
                                                graphe.add_node(nouveau_noeu)
                                                graphe.nodes[nouveau_noeu]["tempsCompose"]=100
                                                graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                                graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ')
                                                print(graphe.edges)
                                        
                                        elif ("Adj" in g.nodes[v]):
                                            if (premierPos=="Det" and deuxiemePos=="Nom" and g.nodes[v]["Adj"]>50):#on a qqc comme le petit, on vérifie le 3eme noeud
                                                for w in g.neighbors(v):
                                                    if ("Nom" in g.nodes[w].keys() and g.nodes[w]["Nom"]>50 ):#ATTENTION
                                                        print("\t")
                                                    else : 
                                                        "à vérifier ATTENTION"
                                                        nouveau_noeu=n+" "+v.replace("_","")
                                                        graphe.add_node(nouveau_noeu)
                                                        graphe.nodes[nouveau_noeu][posAAjouter]=100
                                                        graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                                        graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ')
                                                        print(graphe.edges)
                        
                                            if (premierPos=="Det" and deuxiemePos=="Nom"):#on a qqc comme le petit, on vérifie le 3eme noeud
                                                nouveau_noeu=n+" "+v.replace("_","")
                                                graphe.add_node(nouveau_noeu)
                                                graphe.nodes[nouveau_noeu][posAAjouter]=100
                                                graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                                graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ')
                                                print(graphe.edges)
                        
                                        elif (n=="_de" and v=="_la"):
                                            nouveau_noeu=n+" "+v.replace("_","")
                                            graphe.add_node(nouveau_noeu)
                                            graphe.nodes[nouveau_noeu]["articlePartitif"]=100
                                            graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                            graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ')
                                            print(graphe.edges)
                                        elif (premierPos=='Ver' and deuxiemePos=='Adv'):
                                            graphe.nodes[v]["CCdeManiere"]=100
                                            nouveau_noeu=n+" "+v.replace("_","")
                                            graphe.add_node(nouveau_noeu)
                                            graphe.nodes[nouveau_noeu][posAAjouter]=100
                                            graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                            graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ')
                                            print(graphe.edges)
                                        elif (premierPos=="Pre" and deuxiemePos=="GN" and v!="_un" and v!="_une") or (premierPos=="Pre" and deuxiemePos=="Nom" and v!="_un" and v!="_une"):
                                            if (n=='_par'):
                                                nouveau_noeu=n+" "+v.replace("_","")
                                                graphe.add_node(nouveau_noeu)
                                                graphe.nodes[nouveau_noeu][posAAjouter]=100
                                                graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                                graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ')
                                                print(graphe.edges)

                                        else:
                                            graphe.add_node(nouveau_noeu)
                                            graphe.nodes[nouveau_noeu][posAAjouter]=100
                                            graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                            graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ')
                                            print(graphe.edges)


    return graphe


def rechercher3(premierPos, deuxiemePos, troisiemePos, posAAjouter, g):
    graphe=g
    liste_noeuds=list(g.nodes(data=True))
    for n,p in liste_noeuds:
            if (premierPos in p.keys() and (p[premierPos]>50 or p[premierPos]==40) ):
                for v in g.neighbors(n):
                    if (deuxiemePos in g.nodes[v] and g.nodes[v][deuxiemePos]>50 ):
                        for w in g.neighbors(v):

                            if (troisiemePos in g.nodes[w] and g.nodes[w][troisiemePos]>50 ):
                                print(n,"\t",p,"\t\t==>",v,"\t",graphe.nodes[v],"\t\t-->",w,"\t",graphe.nodes[w])
                                liste_arretes=list(g.edges)
                                liste_arretes_bis=list(g.edges)

                                for (e1, e2) in liste_arretes:
                                    if (e2==n):
                                        for (e1_bis, e2_bis) in liste_arretes_bis:
                                            if (e1_bis==w):

                                                if (premierPos=='Ver' and deuxiemePos=='Ver' ):
                                                    if (w.replace('_','')=="par" or w.replace('_','')=="avec" or w.replace('_','')=="de" or w.replace('_','')=="d'"):
                                                        nouveau_noeu=n+" "+v.replace("_","")+" "+w.replace("_","")
                                                        print("arretes à ajouter : (",e1,"-",nouveau_noeu,")\t(",nouveau_noeu,"-",e2_bis,")")
                                                        graphe.add_node(nouveau_noeu)
                                                        graphe.nodes[nouveau_noeu][posAAjouter]=100
                                                        for (e1_biss, e2_biss) in liste_arretes_bis:
                                                            #print(e1_bis,"\t", e2_bis, "repere")
                                                            graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                                            #graphe.add_edge(nouveau_noeu, e2_biss,weight=1, type='r_succ')
                                                            graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ') #erreur sur deuxieme arrete

                                                        graphe=repereComplementAgent(graphe)
                                                        print(graphe.edges)
                                                        return graphe


                                                elif ("Ver" in  g.nodes[w].keys() and "Adj" in g.nodes[v].keys() and premierPos=="Det" and deuxiemePos=="Nom" and g.nodes[v]["Adj"]>50 and g.nodes[w]["Ver"]>50):#on a qqc comme le petit, on vérifie le 3eme noeud
                                                    #La chatte allaite : chatte est bien un adj
                                                    nouveau_noeu=n+" "+v.replace("_","")
                                                    print("arretes à ajouter : (",e1,"-",nouveau_noeu,")\t(",nouveau_noeu,"-",e2_bis,")")
                                                    graphe.add_node(nouveau_noeu)
                                                    graphe.nodes[nouveau_noeu]["GN"]=100
                                                    graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                                    graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ')
                                                    #graphe.add_edge(nouveau_noeu, e2,weight=1, type='r_succ')
                                                    print(graphe.edges)
                                                elif (premierPos=='Proposition' and deuxiemePos=='Pre' and troisiemePos=="Nom"):
                                                    if(v!="_un" and v!="_une"):
                                                        nouveau_noeu=n+" "+v.replace("_","")
                                                        print("arretes à ajouter : (",e1,"-",nouveau_noeu,")\t(",nouveau_noeu,"-",e2_bis,")")
                                                        graphe.add_node(nouveau_noeu)
                                                        graphe.nodes[nouveau_noeu]["GN"]=100
                                                        graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                                        graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ')
                                                    #graphe.add_edge(nouveau_noeu, e2,weight=1, type='r_succ')
                                                    print(graphe.edges)

                                                elif (premierPos=='Det' and deuxiemePos=='Nom' and troisiemePos=="Adj"):
                                                    #if ('Adj' in graphe.nodes[w].keys() and 'Ver' in graphe.nodes[w].keys() and w!="est"):
                                                    if ('Ver' in graphe.nodes[w].keys() and w!="_est"):
                                                        temoin=False
                                                        for x in g.neighbors(w):
                                                            print("voisin de w :", x,"\t",graphe.nodes[x].keys())
                                                            if ('Adv' in graphe.nodes[x].keys() or 'Adj' in graphe.nodes[x].keys() ):
                                                                temoin=True

                                                        if (temoin==False):
                                                            nouveau_noeu=n+" "+v.replace("_","")+" "+w.replace("_","")
                                                            print("arretes à ajouter : (",e1,"-",nouveau_noeu,")\t(",nouveau_noeu,"-",e2_bis,")")
                                                            graphe.add_node(nouveau_noeu)
                                                            graphe.nodes[nouveau_noeu][posAAjouter]=100
                                                            graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                                            graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ')
                                                            print(graphe.edges)
                                                    return graphe


                                                elif (premierPos=='Det' and deuxiemePos=='Adj' and troisiemePos=="Nom"):
                                                    print("here",n,v,w)
                                                    if ('Adj' in graphe.nodes[v].keys() and w=="_est"): #Le petite court
                                                        return graphe

                                                elif (premierPos=='Det' and deuxiemePos=='Nom' and troisiemePos=="Punct"):
                                                    nouveau_noeu=n+" "+v.replace("_","") #la chatte allaite ses petits .
                                                    print("arretes à ajouter : (",e1,"-",nouveau_noeu,")\t(",nouveau_noeu,"-",e2_bis,")")
                                                    graphe.add_node(nouveau_noeu)
                                                    graphe.nodes[nouveau_noeu][posAAjouter]=100
                                                    graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                                    #graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ')
                                                    graphe.add_edge(nouveau_noeu, e2,weight=1, type='r_succ')
                                                    print(graphe.edges)

                                                elif (premierPos=='GN' and deuxiemePos=='Ver' and troisiemePos=='Adj'):
                                                    if (v!="_ai" and v!="_as" and v!="_a" and v!="_avons" and v!="_avez" and v!="_ont"): #l'idée serait de voir si v r_lemma avoir
                                                        if (w!="_sa" and w!="_son" and w!="_ses" and w!="_mon" and w!="_mes" and w!="_ma" and w!="_ton" and w!="_tes" and w!="_ta" and w!="_notre" and w!="_votre" and w!="_vos"  and w!="_nos" and w!="_leur" and w!="_leurs"):
                                                            nouveau_noeu=n+" "+v.replace("_","")+" "+w.replace("_","")
                                                            print("arretes à ajouter : (",e1,"-",nouveau_noeu,")\t(",nouveau_noeu,"-",e2_bis,")")
                                                            graphe.add_node(nouveau_noeu)
                                                            graphe.nodes[nouveau_noeu][posAAjouter]=100
                                                            graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                                            graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ')
                                                            #graphe.add_edge(nouveau_noeu, e2,weight=1, type='r_succ')
                                                            print(graphe.edges)


                                                else :
                                                    nouveau_noeu=n+" "+v.replace("_","")+" "+w.replace("_","")
                                                    print("arretes à ajouter : (",e1,"-",nouveau_noeu,")\t(",nouveau_noeu,"-",e2_bis,")")
                                                    graphe.add_node(nouveau_noeu)
                                                    graphe.nodes[nouveau_noeu][posAAjouter]=100
                                                    graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                                    graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ')
                                                    print(graphe.edges)
                                                    """
                                                        elif (w.replace('_','')!="est"):
                                                            #nouveau_noeu="_"+posAAjouter+" identifié : "+n+" "+v.replace("_","")+" "+w.replace("_","")
                                                            nouveau_noeu=n+" "+v.replace("_","")+" "+w.replace("_","")
                                                            print("arretes à ajouter : (",e1,"-",nouveau_noeu,")\t(",nouveau_noeu,"-",e2_bis,")")
                                                            graphe.add_node(nouveau_noeu)
                                                            graphe.nodes[nouveau_noeu][posAAjouter]=100
                                                            graphe.add_edge(e1, nouveau_noeu, weight=1, type='r_succ')
                                                            graphe.add_edge(nouveau_noeu, e2_bis,weight=1, type='r_succ')
                                                            print(graphe.edges)
                                                    """

    return graphe



def repereNegation(g):
    graphe=g
    graphe=rechercher3("Adv","Ver","Adv","FormeNegativeDuVerbe", graphe)
    return graphe

def repereComplementAgentBis(g):
    graphe=g
    graphe=rechercher2("TempsComposeAvecCompdAgent", "GN", "CompdAgentAprèsLeVerbe", graphe)
    return graphe    
    
    
def repereComplementAgent(g):
    graphe=g
    listeVoisins=[]

    liste_noeuds=list(graphe.nodes(data=True))
    for n,p in liste_noeuds:
            #print("n,p",n, p)
            if ("TempsComposeAvecCompdAgent" in p.keys()):
                for v in g.neighbors(n):
                    listeVoisins.append(v)
                    print("v :",v)
                print("listeVoisins ",listeVoisins, "n : ",n)
                for v in listeVoisins:
                    #print("p_bis.keys : ",g.nodes[v].keys())
                    if ("GN" in g.nodes[v].keys() or "Nom" in g.nodes[v].keys()):
                        graphe.nodes[v]["ComplementdAgent"]=100
    """
    listeArretes=list(graphe.edges(data=True))
    for a in listeArretes :
        print (a1,"\t", type(a1))
    """
    return graphe



def repereAttribut(g):#peut-être à supprimer?
    graphe=g
    rechercher3("GN","Ver","Adj","noyeau-VerbeDÉtat-Attribut",graphe)  #idée : La fille est belle
    return graphe

def repereTempsCompose(g):
    graphe=g
    graphe=rechercher3("Ver","Ver","Pre","TempsComposeAvecCompdAgent", graphe)
    graphe=rechercher2("Pre", "GN", "CompDagent", g)


    """
    graphe=repereComplementAgent(graphe)

    if (graphe!=g):
        print("diffeeeereeennnce")
        graphe=repereComplementAgentBis(graphe)
    else:
        print("")

    graphe=rechercher2("Ver","Ver","TempsCompose-2VerbesQuiSesuivent...", graphe)
    """
    return graphe

def gnAnalyse(g):
    graphe=g #ce graphe est à modifier
    graphe=rechercher2("Det","Nom","GN",g)

    graphe=rechercher3("Det","Nom","Adj","GN",graphe)
    graphe=rechercher3("Det","Adj","Nom","GN",graphe)
    graphe=rechercher3("Det","Nom","Punct","GN",graphe) #la chatte allaite ses petits .  d'où cette regle
    #graphe=rechercher3("Det","Nom","Ver","GN",graphe) #la chatte allaite : chatte est un adj aussi hors pb avec la petite est belle/ la petite boit d'où cette regle
    return graphe

def gvAnalyse(g):
    graphe=g #ce graphe est à modifier
    graphe=gnAnalyse(graphe)
    graphe=repereNegation(graphe)
    
    graphe=rechercher2("Ver","Ver","TempsCompose",graphe)


    graphe=rechercher2("Ver", "GN", "GV", graphe)

    graphe=rechercher2("Ver", "Adj", "GV?", graphe)
    graphe=rechercher2("Ver", "Adv", "GV", graphe)
    graphe=rechercher3("Ver", "Adv", "Adv", "GV", graphe)
    graphe=rechercher3("Ver", "Ver", "GN", "GV", graphe)

    graphe=rechercher2("FormeNegativeDuVerbe", "GN", "GV_formeNeg", graphe)
    graphe=rechercher2("FormeNegativeDuVerbe", "Adv", "GV_formeNeg", graphe)
    graphe=rechercher3("FormeNegativeDuVerbe", "Adv", "Adv", "GV_formeNeg", graphe)
#    graphe=rechercher2("GV","GN","GV",graphe)
    graphe=repereTempsCompose(graphe)

    return graphe

def phraseAnalyse(g):
    graphe=g #ce graphe est à modifier
    graphe=gnAnalyse(graphe)
    graphe=gvAnalyse(graphe)
    graphe=rechercher3("GN", "Ver", "GN", "Proposition", graphe)
    graphe=repereAttribut(graphe)
    graphe=rechercher2("TempsComposeAvecCompdAgent", "GN", "verbe avec son complement d agent (GN)", graphe)
    graphe=rechercher3("Proposition","Pre","GN", "Proposition", graphe)
    graphe=rechercher3("Proposition","Pre","Nom", "Proposition", graphe)
    graphe=rechercher2("Proposition", "Punct", "Phrase", graphe)

    return graphe

def traitement(term):
    term = term.replace("_", " ")
    term = term.replace(" ", "", 1)
    term = term.replace("(", "")
    term = term.replace(")", "")
    term = term.replace(",", "")
    term = term.replace("'", "")
    term = term.replace("  ", " ")
    term = term.replace("START ", "")
    term = term.replace("END", "")
    return (term)




def extraction_jdm(word: str, rel: str = '4'):
    chemin_absolu = os.path.dirname(os.path.abspath(__file__))

    if (os.path.isdir(chemin_absolu + '/cache') and os.path.isfile(
            chemin_absolu + '/cache/' + word + '.pkl')):
        fichier = open(chemin_absolu + '/cache/' + word + '.pkl', 'rb')
        categorie = pickle.load(fichier)
        fichier.close()
        return categorie

    html = requests.get(
        'http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=' + word + '&rel=' + rel)
    encoding = html.encoding if 'charset' in html.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding='iso-8859-1')
    texte_brut = soup.find_all('code')
    noeuds = re.findall('[e];[0-9]*;.*', str(texte_brut))
    relations = re.findall('[r];[0-9]*;.*', str(texte_brut))
    if ((not noeuds) and (not relations)):
        #print("le mot " + word + " n'existe pas dans jeux de mots")
        return None

    tableau_noeuds = []
    tableau_relations = []

    for noeud in noeuds:
        noeud = noeud.replace('&lt;', '<')
        noeud = noeud.replace('&gt;', '>')
        tableau_noeuds.append(noeud.split(';'))
    for relation in relations:
        relation = relation.replace('&lt;', '<')
        relation = relation.replace('&gt;', '>')
        tableau_relations.append(relation.split(';'))

    id = {}
    i = 0
    while i <= len(tableau_relations) - 1:
        if (int(tableau_relations[i][5]) >= 0):
            id[int(tableau_relations[i][3])] = int(tableau_relations[i][5])
        i += 1

    categorie = []
    for N in tableau_noeuds:
        if (int(N[1]) in id):
            if '>' in N[2] and len(N) >= 6:
                categorie.append((N[5].replace("'", ''), id[int(N[1])]))
            else:
                categorie.append((N[2].replace("'", ''), id[int(N[1])]))

    chemin_absolu = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isdir(chemin_absolu + '/cache'):
        try:
            os.mkdir(chemin_absolu + '/cache')
        except OSError:
            print('La création du dossier cache a échoué')

    fichier_cache = open(chemin_absolu + '/cache/' + word + '.pkl', 'wb')
    pickle.dump(categorie, fichier_cache)
    fichier_cache.close()

    return categorie


def get_pos(categorie):
    tabPOS = ["Adv", "Adj", "Conj", "Det", "Nom", "Pre", "Pro", "Ver", "Punct"]

    maxi = 0
    categorie_new = []
    if categorie is not None :
        for x in categorie:
            element = x[0].split(':')[0]
            if element in tabPOS:
                maxi = 0
                for cat in categorie:
                    if element in cat[0] and cat[1] > maxi:
                        maxi = cat[1]

                if element not in [y[0] for y in categorie_new]:
                    categorie_new.append((element, maxi))
                else:
                    for i in range(len(categorie_new)):
                        if element == categorie_new[i][0]:
                            categorie_new[i] = (element, maxi)


    return categorie_new


def get_pos_returnListe_Pos_Et_Mot(categorie):
    tabPOS = ["Adv", "Adj", "Conj", "Det", "Nom", "Pre", "Pro", "Ver", "Punct"]

    maxi = 0
    categorie_new = []
    for x in categorie:
        element = x[0].split(':')[0]
        if element in tabPOS:
            maxi = 0
            for cat in categorie:
                if element in cat[0] and cat[1] > maxi:
                    maxi = cat[1]

            if element not in [y[0] for y in categorie_new]:
                categorie_new.append((element, maxi))
            else:
                for i in range(len(categorie_new)):
                    if element == categorie_new[i][0]:
                        categorie_new[i] = (element, maxi)

    return categorie_new


# let's transform our text in a graph ( text_list avec chiffre str(i+1) +)
def text_to_grapheee(text, liste_mwe):
    text_list=[]
    text_list_temporaire = text.lower().split()
    print("text_list :")
    for i in range(len(text_list_temporaire)):

        x='_' + text_list_temporaire[i]
        text_list.append(x)
        nb=text_list.count(x)
        while (nb>1):
            for j in range(nb):
                text_list[i]=text_list[i]+'_'
                nb=text_list.count(text_list[i])
                print("range :",nb)


        print("text_list : ",text_list[i])


    graph = nx.DiGraph(directed=True) #on créée un graphe dirigé vide

    # Ajout des noeuds au graph
    graph.add_node('_START')
    for word in text_list:  #on ajoute des noeuds correspondant aux mots de la phrase
        graph.add_node(word)

    for mwe in liste_mwe:   #on ajoute des noeuds correspondant aux termes composés de la phrase
        graph.add_node("_" + mwe)

    graph.add_node('_END')

    # Ajout des edges to the graph
    graph.add_edge('_START', text_list[0], weight=1, type='r_succ')
    for i in range(len(text_list) - 1):   #ajout arretes entre noeuds entre mots
        graph.add_edge(text_list[i], text_list[i + 1], weight=1, type='r_succ')
    graph.add_edge(text_list[-1], '_END', weight=1, type='r_succ')

    for i in liste_mwe: #ajout arretes entre noeuds entre noeuds composés
        s = str.split(i)
        premier_mot = s[0].lower()
        dernier_mot = s[-1].lower()
        print("sssss : ",s)
        print("premier_mot à vérifier :",premier_mot)
        graph.add_edge(text_list[text_list.index("_" + premier_mot) - 1], "_" + i, weight=1, type='r_succ')
        graph.add_edge("_" + i, text_list[text_list.index("_" + dernier_mot) + 1], weight=1, type='r_succ')

    return graph


def detection_mwe(tx):
    list_mwe = []
    with open(pathTermesComposes, "r", encoding="ISO-8859-1") as f:
        data = f.read()
        data2 = data.split("\n9", 1)
        data3 = data2[1].split("\n");
        for line in data3:
            expression = line.split("\"")
            if len(expression) < 2:
                pass
            else:
                if " " + expression[1] + " " in tx and "|" not in expression[1] and ">" not in expression[1]:
                    print("nœud composé", line)
                    list_mwe.append(expression[1])
    return list_mwe



def graph_visualization(graph, verbose=False):
    if verbose:
        print(f"Nodes: {graph.nodes}")

        for edge in graph.edges:
            print(edge, graph.edges[edge[0], edge[1]]['weight'], graph.edges[edge[0], edge[1]]['type'])
            print("teeeeessssttt\t", edge[0])
    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in graph.edges(data=True)])

    r_succedges = []
    for edge in graph.edges():
        if graph.edges[edge[0], edge[1]]['type'] == 'r_succ':
            r_succedges.append(edge)

    edge_colors = ['black' if not edge in r_succedges else 'blue' for edge in graph.edges()]

    pos = nx.spring_layout(graph)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    nx.draw_networkx(graph, pos, node_size=1500, edge_color=edge_colors, edge_cmap=plt.cm.Reds)
    pylab.show()



if __name__ == '__main__':
    listeDictionnaires = []
    texte = " la religieuse entre dans la pâtisserie pour acheter une religieuse  . "
    #texte = " le petit chat n' aime pas le lait de vache . " ATTENTION : ESPACE ENTRE ' ET AIME TRÈS IMPORTANT
    #texte = " La Tour Eiffel est très belle. "
    #texte = " Je le vois boire du lait ."
    liste_mwe = detection_mwe(texte) #liste des termes composés de texte selon jdm, liste de str

    print(texte)
    print(liste_mwe)

    res = text_to_grapheee(texte, liste_mwe)

    for x in res.nodes:
        #y = x.replace("_", "")
        if (x != "_START" and x != "_END"):
            y = x.replace("_", "")
            L=get_pos(extraction_jdm(y))
            for (a,b) in L :
                res.nodes[x][a]=b
            
            listeLieux=[]
            listeLieux=extraction_jdm(y, '15')
            if (listeLieux is not None):
                for (a,b) in listeLieux:
                    if ('_'+a in res.nodes) : 
                        res.add_edge(x, "_"+a, weight=int(b), type='r_lieu')
                        print(x, "r_lieu", "_"+a)
                    
            """            
            listeLemmes=extraction_jdm(y, '19')
            for (a,b) in listeLemmes:
                if ('_'+a in res.nodes) : 
                    res.add_edge(x, "_"+a, weight=int(b), type='r_lemma')
                    print(x, "r_lemma", "_"+a)
            """
            listeActionLieu=extraction_jdm(y, '31')
            if (listeActionLieu is not None):
                for (a,b) in listeActionLieu:
                    if ('_'+a in res.nodes) : 
                        res.add_edge(x, "_"+a, weight=int(b), type='r_action_lieu')
                        print(x, "r_action_lieu", "_"+a)
                


    print("texte:\t",texte)
    print("liste_mwe:\t",liste_mwe)
    print("res", res.nodes(data=True) )
    print("res.node:\t", res)
    print("\n\nphraseAnalyse(res):\n")
    graphe=phraseAnalyse(res)
    for n in graphe.nodes(data=True):
        print(n)
    """
    for e in graphe.edges(data=True):
        print(e)
    """

