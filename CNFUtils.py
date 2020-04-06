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
