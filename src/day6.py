from functools import reduce
import string


def n_union_yes_answers(group_answers):
    lines = [set(s) for s in group_answers.splitlines()]
    return len(reduce(lambda s1, s2: s1 | s2, lines, set()))


def n_intersect_yes_answers(group_answers):
    lines = [set(s) for s in group_answers.splitlines()]
    return len(reduce(lambda s1, s2: s1 & s2, lines, set(string.ascii_lowercase)))


if __name__ == "__main__":
    with open("customs.txt") as fp:
        data = fp.read()

    customs_forms = data.split("\n\n")
    q1_answer = sum(n_union_yes_answers(f) for f in customs_forms)
    print(q1_answer)

    q2_answer = sum(n_intersect_yes_answers(f) for f in customs_forms)
    print(q2_answer)
