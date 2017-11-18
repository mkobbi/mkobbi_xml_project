class Token:
    def __init__(self, nom, valeur):
        self.nom = nom
        self.valeur = valeur

    def __str__(self):
        return self.nom + ":" + self.valeur

class Lexer:
    def __init__(self, pattern):
        self.origine = pattern
        self.symboles = {'(':'PAREN_GAUCHE', ')':'PAREN_DROITE', '*':'ETOILE', '\x08':'CONCAT', '+':'PLUS', '?':'INTERROGATION'}
        self.actuel = 0
        self.taille = len(self.origine)
       
    def prendre_token(self): 
        if self.actuel < self.taille:
            c = self.origine[self.actuel]
            self.actuel += 1
            if c not in self.symboles.keys(): # CHAR
                token = Token('CHAR', c)
            else:
                token = Token(self.symboles[c], c)
            return token
        else:
            return Token('NONE', '')

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.lookahead = self.lexer.prendre_token()
    
    def considerer(self, nom):
        if self.lookahead.nom == nom:
            self.lookahead = self.lexer.prendre_token()

    def parse(self):
        self.term()
        return self.tokens
    
    def term(self):
        self.operateur()
        if self.lookahead.valeur not in ')':
            self.term()
            self.tokens.append(Token('CONCAT', '\x08'))
    
    def operateur(self):
        self.primary()
        if self.lookahead.nom in ['ETOILE', 'PLUS', 'INTERROGATION']:
            self.tokens.append(self.lookahead)
            self.considerer(self.lookahead.nom)

    def primary(self):
        if self.lookahead.nom == 'PAREN_GAUCHE':
            self.considerer('PAREN_GAUCHE')
            self.term()
            self.considerer('PAREN_DROITE')
        elif self.lookahead.nom == 'CHAR':
            self.tokens.append(self.lookahead)
            self.considerer('CHAR')

class Etat:
    def __init__(self, nom):
        self.epsilon = []
        self.transitions = {}
        self.nom = nom
        self.est_fin = False
    
class NFA:
    def __init__(self, debut, fin):
        self.debut = debut
        self.fin = fin
        fin.est_fin = True
    
    def ajouteretat(self, etat, ensemble_etat):
        if etat in ensemble_etat:
            return
        ensemble_etat.add(etat)
        for eps in etat.epsilon:
            self.ajouteretat(eps, ensemble_etat)
    
    def match(self,s):
        etats_actuels = set()
        self.ajouteretat(self.debut, etats_actuels)
        
        for c in s:
            prochains_etats = set()
            for etat in etats_actuels:
                if c in etat.transitions.keys():
                    etat_transitoire = etat.transitions[c]
                    self.ajouteretat(etat_transitoire, prochains_etats)
           
            etats_actuels = prochains_etats

        for s in etats_actuels:
            if s.est_fin:
                return True
        return False

class Manipulateur:
    def __init__(self):
        self.manipulateurs = {'CHAR':self.gerer_char, 'CONCAT':self.gerer_concat,
                         'ETOILE':self.gerer_rep,
                         'PLUS':self.gerer_rep, 'INTERROGATION':self.gerer_interrogation}
        self.etat_count = 0

    def creer_etat(self):
        self.etat_count += 1
        return Etat('s' + str(self.etat_count))
    
    def gerer_char(self, t, pile_nfa):
        s0 = self.creer_etat()
        s1 = self.creer_etat()
        s0.transitions[t.valeur] = s1
        nfa = NFA(s0, s1)
        pile_nfa.append(nfa)
    
    def gerer_concat(self, t, pile_nfa):
        n2 = pile_nfa.pop()
        n1 = pile_nfa.pop()
        n1.fin.est_fin = False
        n1.fin.epsilon.append(n2.debut)
        nfa = NFA(n1.debut, n2.fin)
        pile_nfa.append(nfa)
    
    def gerer_rep(self, t, pile_nfa):
        n1 = pile_nfa.pop()
        s0 = self.creer_etat()
        s1 = self.creer_etat()
        s0.epsilon = [n1.debut]
        if t.nom == 'ETOILE':
            s0.epsilon.append(s1)
        n1.fin.epsilon.extend([s1, n1.debut])
        n1.fin.est_fin = False
        nfa = NFA(s0, s1)
        pile_nfa.append(nfa)

    def gerer_interrogation(self, t, pile_nfa):
        n1 = pile_nfa.pop()
        n1.debut.epsilon.append(n1.fin)
        pile_nfa.append(n1)

