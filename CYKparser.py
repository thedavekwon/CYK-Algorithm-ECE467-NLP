import argparse
import itertools

from CNFUtils import parse_cnf_grammar, traverse_table

parser = argparse.ArgumentParser(description='Constituency Parser with CYK algorithms')
parser.add_argument('--cnf', help='path of cnf grammar', type=str, required=True)
args = parser.parse_args()
CNF_PATH = args.cnf


def cyk_recognizer(words, single_grammar, double_grammar):
    print(single_grammar)
    print(double_grammar)
    N = len(words)
    table = {}
    # generate table with appropriate index (upper triangle created for optimization)
    for key in list(itertools.product(range(0, N + 1), range(0, N + 1))):
        if key[0] >= key[1]:
            continue
        table[key] = set()
    for j in range(1, N + 1):
        for g in single_grammar[words[j - 1]]:
            table[(j - 1, j)] = table[(j - 1, j)].union({g})
        for i in range(j - 2, -1, -1):
            for k in range(i + 1, j):
                for dg_key in double_grammar.keys():
                    dgs = double_grammar[dg_key]
                    for dg in dgs:
                        if dg[0] in table[(i, k)] and dg[1] in table[(k, j)]:
                            table[(i, j)] = table[(i, j)].union({dg_key})
    return 'S' in table[(0, N)]


def cyk_parser(words, single_grammar, double_grammar):
    N = len(words)
    table = {}
    # generate table with appropriate index (upper triangle created for optimization)
    for key in list(itertools.product(range(0, N + 1), range(0, N + 1))):
        if key[0] >= key[1]:
            continue
        table[key] = []
    for j in range(1, N + 1):
        for g in single_grammar[words[j - 1]]:
            table[(j - 1, j)].append([g, (j - 1, j)])
        for i in range(j - 2, -1, -1):
            for k in range(i + 1, j):
                for dg_key in double_grammar.keys():
                    dgs = double_grammar[dg_key]
                    for dg in dgs:
                        if dg[0] in list(map(lambda x: x[0], table[(i, k)])) and \
                                dg[1] in list(map(lambda x: x[0], table[(k, j)])):
                            table[(i, j)].append([dg_key, (i, k, dg[0]), (k, j, dg[1])])
    if 'S' in list(map(lambda x: x[0], table[(0, N)])):
        return traverse_table(table, words, 0, N, 'S')
    return None


if __name__ == "__main__":
    single_grammar, double_grammar = parse_cnf_grammar(CNF_PATH)
    words = input().split(" ")
    print(words)
    parsed = cyk_parser(words, single_grammar, double_grammar)
    if parsed is None:
        print("NO VALID PARSES")
    else:
        for p in parsed:
            print(p)
