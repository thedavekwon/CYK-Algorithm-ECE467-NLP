from CNFUtils import parse_cnf_grammar
import itertools

CNF_PATH = "data/sampleGrammar.cnf"


def cyk_parser(words, single_grammar, double_grammar):
    print(single_grammar)
    print(double_grammar)
    N = len(words)
    table = {}
    # generate table with appropriate index (upper triangle created for optimization)
    for key in list(itertools.product(range(0, N+1), range(0, N+1))):
        if key[0] > key[1]:
            continue
        table[key] = set()
    for j in range(1, N+1):
        for g in single_grammar[words[j-1]]:
            table[(j-1, j)] = table[(j-1, j)].union({g})
        for i in range(j-2, -1, -1):
            for k in range(i+1, j):
                for dg_key in double_grammar.keys():
                    dgs = double_grammar[dg_key]
                    for dg in dgs:
                        if dg[0] in table[(i, k)] and dg[1] in table[(k, j)]:
                            table[(i, j)] = table[(i, j)].union({dg_key})
    return table

if __name__ == "__main__":
    single_grammar, double_grammar = parse_cnf_grammar(CNF_PATH)
    words = "i book the flight from houston".split(" ")
    cyk_parser(words, single_grammar, double_grammar)