from functools import lru_cache

SHINY_GOLD = ("shiny", "gold")


def parse_line(line):
    # Sample input:
    # shiny teal bags contain 3 dotted chartreuse bags, 1 wavy yellow bag, 3 clear lavender bags.
    # shiny crimson bags contain 2 light plum bags, 3 shiny black bags.
    # shiny lime bags contain 1 dim turquoise bag, 4 pale fuchsia bags.
    # pale lavender bags contain 3 bright lavender bags, 5 wavy blue bags.
    # shiny purple bags contain no other bags.

    outercolor1, outercolor2, *words = line.split()
    assert words[0] == "bags"
    assert words[1] == "contain"
    words = words[2:]

    inside_bags = []
    while len(words) >= 4:
        number, color1, color2, bags, *remainder = words
        inside_bags.append((int(number), (color1, color2)))
        words = remainder

    return (outercolor1, outercolor2), inside_bags


# dictionary that holds what each outter bag color contains as two
# lists: a list of counts and a list of (two-word) colors
def load_container_rules():
    contains = {}
    with open("bags.txt") as fp:
        data = fp.read().splitlines()

    for line in data:
        outer, inner = parse_line(line)

        numbers = [i[0] for i in inner]
        colors = [i[1] for i in inner]

        contains[outer] = (numbers, colors)
    return contains


# Return True if can_contain_shiny_gold
@lru_cache(maxsize=600)  # want to memorize everything
def can_contain_shiny_gold(color):
    contained_colors = contains[color][1]

    if SHINY_GOLD in contained_colors:
        return True
    else:
        for cocolor in contained_colors:
            if can_contain_shiny_gold(cocolor):
                return True
    return False


@lru_cache(maxsize=600)
def how_many_bags_inside(color):
    contained_counts = contains[color][0]
    contained_colors = contains[color][1]

    total = 0
    for cocount, cocolor in zip(contained_counts, contained_colors):
        inside_count = how_many_bags_inside(cocolor)
        total += cocount * (inside_count + 1)  # need to count the outer bag!
    return total


contains = load_container_rules()

# How many bag colors can eventually contain a shiny gold bag
count = 0
for color in contains.keys():
    if can_contain_shiny_gold(color):
        count += 1
print(count)

# How many bags must be inside a shiny gold bag?
print(how_many_bags_inside(SHINY_GOLD))
