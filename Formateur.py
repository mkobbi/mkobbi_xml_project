from collections import defaultdict
from Stack import Stack

def ouvrir_xml(xml):
    with open(xml, 'r') as f:
        chaine = f.read()
    #print(chaine)
    t = chaine.split("><")
    t[0] = t[0][1]
    t[-1] = t[-1][0] + t[-1][1]
    #print(t)
    l = []
    for n in t:
        if len(n)==1:
            l.append([0, n])
        else:
            l.append([1,n[1]])
    return l

def formater_dtd(dtd):
    with open(dtd, 'r') as d:
        data = d.read()
    t = [x for x in data.replace('(#PCDATA)','').replace(',','').replace('>','').split('\n')[1:-2] if x != '']
    dictionnaire = {x.split(' ')[1]:x.split(' ')[2].replace(' ','') for x in t}
    return dictionnaire

def verifier_bien_forme(xml):
    liste = ouvrir_xml(xml)
    pile = Stack()
    noeud = {}
    liste_adj = defaultdict(list)
    continuer = True
    i = 0
    if (liste[0][1] not in ['&', '<', '>', "'", '"', '', '/']):
        pile.push([i, liste[0][1]])
        noeud[i] = liste[0][1]
    else:
        continuer = False
    for elt in range(1, len(liste)):
        if (liste[elt][1] not in ['&', '<', '>', "'", '"', '']):
            if liste[elt][0] == 0:
                if pile.isEmpty():
                    continuer = False
                    break
                parent = pile.pop()
                pile.push(parent)
                i += 1
                fils = [i, liste[elt][1]]
                noeud[fils[0]] = fils[1]
                pile.push(fils)
                # print(parent, fils)
                liste_adj[parent[0]].append(fils[0])
                # print(liste_adj)
            else:
                if liste[elt][1] != pile.peek()[1]:
                    continuer = False
                    break
                _ = pile.pop()
        else:
            continuer = False
            break
    if not pile.isEmpty():
        continuer = False
    return continuer, noeud, dict(liste_adj)

def formater_xml(xml):
    continuer, noeud, liste_adj = verifier_bien_forme(xml)
    dictionnaire = defaultdict(list)
    if not continuer:
        print('False')
    else:
        for key in liste_adj:
            dictionnaire[noeud[key]].append(''.join([noeud[n] for n in liste_adj[key]]))
    return(dict(dictionnaire))