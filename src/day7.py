from functools import lru_cache
from collections import namedtuple

SHINY_GOLD = ("shiny", "gold")  # The special color in the questions
MAX_COLORS = 600  # Big enough to memorize every color in input file
MustContain = namedtuple("MustContain", "count,color")


class BagRules:
    @staticmethod
    def parse_line(line):
        """Parses a line of the input file into two-word colors followed by a list of "must have" rules """
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
            inside_bags.append(MustContain(int(number), (color1, color2)))
            words = remainder

        return (outercolor1, outercolor2), inside_bags

    # dictionary that holds what each outter bag color contains as two
    # lists: a list of counts and a list of (two-word) colors
    def __init__(self, input_file="bags.txt"):
        contains = {}
        with open(input_file) as fp:
            data = fp.read().splitlines()

        for line in data:
            outer, inner = self.parse_line(line)
            contains[outer] = inner

        self.contains = contains

    @lru_cache(maxsize=MAX_COLORS)
    def can_contain_shiny_gold(self, color):
        """Return True if bag of given color must have shiny gold bag inside at some level"""
        contained_colors = [rule.color for rule in self.contains[color]]

        if SHINY_GOLD in contained_colors:
            return True
        else:
            for cocolor in contained_colors:
                if self.can_contain_shiny_gold(cocolor):
                    return True
        return False

    @lru_cache(maxsize=MAX_COLORS)
    def how_many_bags_inside(self, color):
        "Sum the bags that must be inside a bag of given color"

        total = 0
        for rule in self.contains[color]:
            inside_count = self.how_many_bags_inside(rule.color)
            total += rule.count * (inside_count + 1)  # need to count the outer bag!
        return total

    def all_colors(self):
        return list(self.contains.keys())


rules = BagRules()
# How many bag colors can eventually contain a shiny gold bag
print(sum(rules.can_contain_shiny_gold(color) for color in rules.all_colors()))

# How many bags must be inside a shiny gold bag?
print(rules.how_many_bags_inside(SHINY_GOLD))
