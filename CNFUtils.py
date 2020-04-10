import itertools


def parse_cnf_grammar(cnf_path):
    with open(cnf_path, "r") as f:
        single_grammar = {}
        double_grammar = {}
        for cnf in f.readlines():
            left, right = cnf.split("-->")
            left = left.strip()
            right = right.strip()
            if " " not in right:
                if right not in single_grammar:
                    single_grammar[right] = []
                single_grammar[right].append(left)
            else:
                if left not in double_grammar:
                    double_grammar[left] = []
                double_grammar[left].append(right.split(" "))
    return single_grammar, double_grammar


def pprint(table, single_grammar, words, i, j):
    print(table[(i, j)])
    for k in range(i, j):
        print(single_grammar[words[k]], end=" ")
    print("")


def traverse_table(table, words, i, j, g):
    ret = []
    for entry in table[(i, j)]:
        if entry[0] == g:
            if len(entry) == 2:
                return ["[{} {}]".format(g, words[i])]
            else:
                left = traverse_table(table, words, *entry[1])
                right = traverse_table(table, words, *entry[2])
                for l, r in list(itertools.product(left, right)):
                    ret.append("[{} {} {}]".format(g, l, r))
    return ret
