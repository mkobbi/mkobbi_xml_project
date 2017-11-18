import Regex
from Formateur import formater_dtd, formater_xml, verifier_bien_forme
import sys

fname = sys.argv[1]
gname = sys.argv[2]

#print(fname, gname)
xml = formater_xml(fname)
#print(xml)
dtd = formater_dtd(gname)
bien_forme, _, _ = verifier_bien_forme(fname)
if bien_forme:
    print("Well-formed")
else:
    print("Not well-formed")
for key in xml:
    #print(dtd[key])
    nfa = Regex.compile(dtd[key])
    for chaine in xml[key]:
        #print(key, chaine)
        if nfa.match(chaine):
            print("valid")
        else:
            print("invalid")
