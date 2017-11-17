from parse import Lexer, Parser, Manipulateur


def compile(p, debug = False):
    
    def print_tokens(tokens):
        for t in tokens:
            print(t)

    lexer = Lexer(p)
    parser = Parser(lexer)
    tokens = parser.parse()

    handler = Manipulateur()
    
    if debug:
        print_tokens(tokens) 

    nfa_stack = []
    
    for t in tokens:
        handler.manipulateurs[t.nom](t, nfa_stack)
    
    assert len(nfa_stack) == 1
    return nfa_stack.pop() 

